"""
Agent Orchestrator - Coordinates all VasperaOS agents.

Built on CrewAI for multi-agent coordination.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import structlog
import yaml
from crewai import Agent, Crew, Task
from pydantic import BaseModel

logger = structlog.get_logger()


class AgentConfig(BaseModel):
    """Configuration for a single agent."""

    name: str
    role: str
    goal: str
    backstory: str
    tools: list[str]
    model: str = "claude-sonnet-4-20250514"
    triggers: list[dict[str, Any]] = []
    approval_required: bool = False


class ProductConfig(BaseModel):
    """Configuration for a single product."""

    name: str
    description: str
    repo: str
    domain: str
    type: str
    ad_platforms: list[str] = []
    target_cpa: float = 50.0
    monthly_ad_budget: float = 1000.0


class AgentOrchestrator:
    """
    Orchestrates all VasperaOS agents across multiple products.

    Responsibilities:
    - Load agent configurations
    - Initialize agents with appropriate tools
    - Route events to agents based on triggers
    - Manage agent execution and results
    """

    def __init__(
        self,
        config_dir: Path = Path("config"),
        secrets_path: Path | None = None,
    ) -> None:
        self.config_dir = config_dir
        self.secrets_path = secrets_path or config_dir / "secrets.yaml"

        self.agents: dict[str, Agent] = {}
        self.products: dict[str, ProductConfig] = {}
        self.crews: dict[str, Crew] = {}

        self._load_configs()

    def _load_configs(self) -> None:
        """Load all configuration files."""
        # Load products
        products_path = self.config_dir / "products.yaml"
        if products_path.exists():
            with open(products_path) as f:
                data = yaml.safe_load(f)
                for product_id, product_data in data.get("products", {}).items():
                    self.products[product_id] = ProductConfig(**product_data)
            logger.info("Loaded products", count=len(self.products))

        # Load agents
        agents_path = self.config_dir / "agents.yaml"
        if agents_path.exists():
            with open(agents_path) as f:
                data = yaml.safe_load(f)
                for agent_id, agent_data in data.get("agents", {}).items():
                    self._initialize_agent(agent_id, AgentConfig(**agent_data))
            logger.info("Loaded agents", count=len(self.agents))

    def _initialize_agent(self, agent_id: str, config: AgentConfig) -> None:
        """Initialize a single agent from config."""
        # TODO: Load actual MCP tools based on config.tools
        tools = []

        agent = Agent(
            role=config.role,
            goal=config.goal,
            backstory=config.backstory,
            tools=tools,
            verbose=True,
            allow_delegation=False,
        )

        self.agents[agent_id] = agent
        logger.info("Initialized agent", agent_id=agent_id, role=config.role)

    async def handle_event(self, event_type: str, payload: dict[str, Any]) -> None:
        """
        Route an event to the appropriate agent(s).

        Args:
            event_type: Type of event (e.g., "github_issue", "schedule")
            payload: Event data
        """
        logger.info("Handling event", event_type=event_type)

        # Find agents triggered by this event
        agents_path = self.config_dir / "agents.yaml"
        with open(agents_path) as f:
            data = yaml.safe_load(f)

        for agent_id, agent_data in data.get("agents", {}).items():
            config = AgentConfig(**agent_data)
            for trigger in config.triggers:
                if trigger.get("type") == event_type:
                    await self._execute_agent(agent_id, payload)

    async def _execute_agent(
        self, agent_id: str, context: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute a single agent with given context."""
        if agent_id not in self.agents:
            logger.error("Agent not found", agent_id=agent_id)
            return {"error": f"Agent {agent_id} not found"}

        agent = self.agents[agent_id]
        logger.info("Executing agent", agent_id=agent_id)

        # Create a task for the agent
        task = Task(
            description=f"Process event: {context}",
            agent=agent,
            expected_output="Action taken and result",
        )

        # Create a crew with just this agent
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True,
        )

        # Execute
        result = crew.kickoff()
        logger.info("Agent completed", agent_id=agent_id, result=str(result)[:100])

        return {"agent_id": agent_id, "result": str(result)}

    async def run_scheduled_agents(self) -> None:
        """Run all agents that have schedule triggers."""
        # TODO: Implement scheduler integration
        pass

    def get_product(self, product_id: str) -> ProductConfig | None:
        """Get a product by ID."""
        return self.products.get(product_id)

    def list_products(self) -> list[str]:
        """List all product IDs."""
        return list(self.products.keys())

    def list_agents(self) -> list[str]:
        """List all agent IDs."""
        return list(self.agents.keys())


# Singleton instance
_orchestrator: AgentOrchestrator | None = None


def get_orchestrator() -> AgentOrchestrator:
    """Get the global orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator
