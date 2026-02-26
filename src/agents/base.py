"""
Base Agent - Foundation for all VasperaOS agents.

All agents inherit from this class and implement domain-specific logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import structlog
from crewai import Agent

logger = structlog.get_logger()


@dataclass
class AgentResult:
    """Result from an agent execution."""

    agent_id: str
    success: bool
    output: Any
    actions_taken: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    execution_time_ms: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)


class BaseAgent(ABC):
    """
    Base class for all VasperaOS agents.

    Provides common functionality for logging, error handling,
    and integration with the orchestration layer.
    """

    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        goal: str,
        backstory: str,
        model: str = "claude-sonnet-4-20250514",
    ) -> None:
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.model = model

        self._crew_agent: Agent | None = None
        self._logger = logger.bind(agent_id=agent_id, agent_name=name)

    @property
    def crew_agent(self) -> Agent:
        """Get or create the CrewAI agent."""
        if self._crew_agent is None:
            self._crew_agent = Agent(
                role=self.role,
                goal=self.goal,
                backstory=self.backstory,
                tools=self.get_tools(),
                verbose=True,
                allow_delegation=False,
            )
        return self._crew_agent

    @abstractmethod
    def get_tools(self) -> list[Any]:
        """Return the tools available to this agent."""
        pass

    @abstractmethod
    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """
        Execute the agent's main task.

        Args:
            context: Input data for the agent

        Returns:
            AgentResult with the outcome
        """
        pass

    async def run(self, context: dict[str, Any]) -> AgentResult:
        """
        Run the agent with error handling and logging.

        This is the main entry point - wraps execute() with
        logging, timing, and error handling.
        """
        start_time = datetime.utcnow()
        self._logger.info("Agent starting", context_keys=list(context.keys()))

        try:
            result = await self.execute(context)
            execution_time = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000
            )
            result.execution_time_ms = execution_time

            self._logger.info(
                "Agent completed",
                success=result.success,
                actions_taken=len(result.actions_taken),
                execution_time_ms=execution_time,
            )

            return result

        except Exception as e:
            execution_time = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000
            )
            self._logger.error("Agent failed", error=str(e))

            return AgentResult(
                agent_id=self.agent_id,
                success=False,
                output=None,
                errors=[str(e)],
                execution_time_ms=execution_time,
            )

    def log_action(self, action: str, details: dict[str, Any] | None = None) -> None:
        """Log an action taken by the agent."""
        self._logger.info("Action taken", action=action, details=details or {})

    def log_error(self, error: str, details: dict[str, Any] | None = None) -> None:
        """Log an error encountered by the agent."""
        self._logger.error("Error encountered", error=error, details=details or {})
