"""
Ads Agent - Manages paid advertising across all platforms.

Implements automated optimization rules and generates reports.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import structlog

from ..base import AgentResult, BaseAgent
from ...rules.ads_rules import AdsRules, setup_ads_rules
from ...rules.engine import RulesEngine

logger = structlog.get_logger()


@dataclass
class CampaignMetrics:
    """Metrics for a single campaign."""

    campaign_id: str
    campaign_name: str
    platform: str
    product_id: str
    spend: float
    impressions: int
    clicks: int
    conversions: int
    revenue: float = 0.0

    @property
    def ctr(self) -> float:
        """Click-through rate."""
        return self.clicks / self.impressions if self.impressions > 0 else 0.0

    @property
    def cpc(self) -> float:
        """Cost per click."""
        return self.spend / self.clicks if self.clicks > 0 else 0.0

    @property
    def cpa(self) -> float:
        """Cost per acquisition."""
        return self.spend / self.conversions if self.conversions > 0 else float("inf")

    @property
    def roas(self) -> float:
        """Return on ad spend."""
        return self.revenue / self.spend if self.spend > 0 else 0.0

    @property
    def frequency(self) -> float:
        """Ad frequency (impressions per user). Placeholder."""
        # This would come from the platform API
        return 0.0


class AdsAgent(BaseAgent):
    """
    Ads Agent - Manages paid advertising across all platforms.

    Responsibilities:
    - Fetch campaign data from all ad platforms
    - Evaluate campaigns against rules (3x Kill, Scale, etc.)
    - Execute optimization actions (pause, scale, alert)
    - Generate performance reports
    """

    def __init__(
        self,
        products_config: dict[str, dict[str, Any]],
        model: str = "claude-sonnet-4-20250514",
    ) -> None:
        super().__init__(
            agent_id="ads_agent",
            name="Ads Agent",
            role="Performance Marketing Manager",
            goal="Maximize ROAS across all ad platforms for all products",
            backstory="""You are an expert performance marketer managing campaigns across
            Google, Meta, LinkedIn, TikTok, and Reddit. You apply data-driven
            optimizations and follow strict rules to prevent wasted spend.""",
            model=model,
        )

        self.products_config = products_config
        self.rules_engine = RulesEngine()
        self._setup_rules()

    def _setup_rules(self) -> None:
        """Set up rules for each product."""
        for product_id, config in self.products_config.items():
            target_cpa = config.get("target_cpa", 50)
            daily_budget = config.get("monthly_ad_budget", 1000) / 30

            setup_ads_rules(self.rules_engine, target_cpa, daily_budget)
            self._logger.info(
                "Rules configured for product",
                product_id=product_id,
                target_cpa=target_cpa,
            )

    def get_tools(self) -> list[Any]:
        """Return the tools available to this agent."""
        # TODO: Return actual MCP tools
        return []

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """
        Execute the ads optimization cycle.

        1. Fetch campaign data from all platforms
        2. Evaluate each campaign against rules
        3. Execute triggered actions
        4. Generate summary report
        """
        actions_taken = []
        errors = []

        try:
            # Fetch campaigns (mock for now)
            campaigns = await self._fetch_campaigns()

            # Evaluate each campaign
            for campaign in campaigns:
                campaign_context = {
                    "campaign_id": campaign.campaign_id,
                    "campaign_name": campaign.campaign_name,
                    "platform": campaign.platform,
                    "product_id": campaign.product_id,
                    "spend": campaign.spend,
                    "impressions": campaign.impressions,
                    "clicks": campaign.clicks,
                    "conversions": campaign.conversions,
                    "ctr": campaign.ctr,
                    "cpc": campaign.cpc,
                    "cpa": campaign.cpa,
                    "roas": campaign.roas,
                    "frequency": campaign.frequency,
                    "in_learning_phase": False,  # TODO: Get from platform
                }

                triggered_rules = self.rules_engine.evaluate("ads", campaign_context)

                for rule, params in triggered_rules:
                    action = await self._execute_action(campaign, rule, params)
                    actions_taken.append(action)

            # Generate report
            report = self._generate_report(campaigns, actions_taken)

            return AgentResult(
                agent_id=self.agent_id,
                success=True,
                output=report,
                actions_taken=actions_taken,
                errors=errors,
            )

        except Exception as e:
            self._logger.error("Ads agent execution failed", error=str(e))
            return AgentResult(
                agent_id=self.agent_id,
                success=False,
                output=None,
                errors=[str(e)],
            )

    async def _fetch_campaigns(self) -> list[CampaignMetrics]:
        """
        Fetch campaign data from all platforms.

        TODO: Implement actual API calls via MCP servers.
        """
        # Mock data for now
        return [
            CampaignMetrics(
                campaign_id="goog_1",
                campaign_name="VasperaMemory - AI Memory Tools",
                platform="google",
                product_id="vaspera-memory",
                spend=150.0,
                impressions=10000,
                clicks=500,
                conversions=5,
            ),
            CampaignMetrics(
                campaign_id="meta_1",
                campaign_name="NutriFitAI - Fitness App",
                platform="meta",
                product_id="nutrifit-ai",
                spend=200.0,
                impressions=25000,
                clicks=750,
                conversions=0,  # This should trigger 3x Kill Rule
            ),
        ]

    async def _execute_action(
        self,
        campaign: CampaignMetrics,
        rule: Any,
        params: dict[str, Any],
    ) -> str:
        """Execute an action based on a triggered rule."""
        action_str = f"{rule.action.value}:{campaign.campaign_id}:{rule.id}"

        self._logger.info(
            "Executing action",
            campaign_id=campaign.campaign_id,
            rule_id=rule.id,
            action=rule.action.value,
        )

        # TODO: Actually execute via platform APIs
        # For now, just log what we would do

        return action_str

    def _generate_report(
        self,
        campaigns: list[CampaignMetrics],
        actions_taken: list[str],
    ) -> dict[str, Any]:
        """Generate a summary report."""
        total_spend = sum(c.spend for c in campaigns)
        total_conversions = sum(c.conversions for c in campaigns)
        total_revenue = sum(c.revenue for c in campaigns)

        return {
            "summary": {
                "total_campaigns": len(campaigns),
                "total_spend": total_spend,
                "total_conversions": total_conversions,
                "total_revenue": total_revenue,
                "overall_cpa": total_spend / total_conversions if total_conversions > 0 else 0,
                "overall_roas": total_revenue / total_spend if total_spend > 0 else 0,
            },
            "actions_taken": actions_taken,
            "campaigns_by_platform": {
                platform: len([c for c in campaigns if c.platform == platform])
                for platform in set(c.platform for c in campaigns)
            },
        }
