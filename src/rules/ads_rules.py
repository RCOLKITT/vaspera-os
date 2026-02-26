"""
Ads Rules - Automation rules for paid advertising.

Implements industry-standard rules like 3x Kill Rule, 20% Scale Rule.
"""

from __future__ import annotations

from .engine import Rule, RuleAction, RulesEngine


class AdsRules:
    """
    Standard advertising automation rules.

    Based on industry best practices for PPC management.
    """

    @staticmethod
    def three_x_kill_rule(target_cpa: float) -> Rule:
        """
        3x Kill Rule: Pause if spend > 3x target CPA with 0 conversions.

        This prevents throwing money at non-converting campaigns.
        """
        return Rule(
            id="ads_3x_kill",
            name="3x Kill Rule",
            description=f"Pause if spend > 3x target CPA (${target_cpa * 3:.2f}) with 0 conversions",
            condition=lambda ctx: (
                ctx.get("spend", 0) > target_cpa * 3
                and ctx.get("conversions", 0) == 0
            ),
            action=RuleAction.PAUSE,
            action_params={"reason": "3x Kill Rule - no conversions"},
            priority=100,  # High priority - run first
        )

    @staticmethod
    def scale_winner_rule(target_cpa: float, threshold: float = 0.8) -> Rule:
        """
        20% Scale Rule: Increase budget by 20% if CPA is 20% below target.

        Only scale if we have enough conversion data (>= 10 conversions).
        """
        return Rule(
            id="ads_scale_winner",
            name="Scale Winner Rule",
            description=f"Scale 20% if CPA < ${target_cpa * threshold:.2f} and conversions >= 10",
            condition=lambda ctx: (
                ctx.get("cpa", float("inf")) < target_cpa * threshold
                and ctx.get("conversions", 0) >= 10
                and not ctx.get("in_learning_phase", False)
            ),
            action=RuleAction.SCALE_UP,
            action_params={"increase_percent": 20},
            priority=50,
        )

    @staticmethod
    def creative_fatigue_rule(frequency_threshold: float = 4.0) -> Rule:
        """
        Creative Fatigue Rule: Alert when frequency exceeds threshold.

        High frequency indicates audience saturation - time for new creative.
        """
        return Rule(
            id="ads_creative_fatigue",
            name="Creative Fatigue Alert",
            description=f"Alert when frequency > {frequency_threshold}",
            condition=lambda ctx: ctx.get("frequency", 0) > frequency_threshold,
            action=RuleAction.ALERT,
            action_params={
                "alert_type": "creative_fatigue",
                "message": "Creative fatigue detected - consider refreshing ad creative",
            },
            priority=30,
        )

    @staticmethod
    def budget_pacing_rule(daily_budget: float) -> Rule:
        """
        Budget Pacing Rule: Alert when spend exceeds 80% of daily budget.

        Helps prevent overspend and allows for adjustments.
        """
        return Rule(
            id="ads_budget_pacing",
            name="Budget Pacing Alert",
            description=f"Alert when spend > 80% of daily budget (${daily_budget * 0.8:.2f})",
            condition=lambda ctx: ctx.get("spend_today", 0) > daily_budget * 0.8,
            action=RuleAction.ALERT,
            action_params={
                "alert_type": "budget_pacing",
                "message": "Approaching daily budget limit",
            },
            priority=20,
        )

    @staticmethod
    def ctr_drop_rule(min_ctr: float = 0.01) -> Rule:
        """
        CTR Drop Rule: Alert when CTR falls below minimum threshold.

        Low CTR indicates poor ad relevance or creative issues.
        """
        return Rule(
            id="ads_ctr_drop",
            name="Low CTR Alert",
            description=f"Alert when CTR < {min_ctr * 100:.1f}%",
            condition=lambda ctx: (
                ctx.get("ctr", 1.0) < min_ctr
                and ctx.get("impressions", 0) >= 1000  # Need enough data
            ),
            action=RuleAction.ALERT,
            action_params={
                "alert_type": "low_ctr",
                "message": "CTR below minimum threshold - review ad creative",
            },
            priority=25,
        )

    @staticmethod
    def learning_phase_protection_rule() -> Rule:
        """
        Learning Phase Protection: Prevent changes during learning phase.

        Making changes during learning resets the algorithm and hurts performance.
        """
        return Rule(
            id="ads_learning_protection",
            name="Learning Phase Protection",
            description="Block modifications during learning phase",
            condition=lambda ctx: ctx.get("in_learning_phase", False),
            action=RuleAction.ALERT,
            action_params={
                "alert_type": "learning_phase",
                "message": "Campaign in learning phase - changes blocked",
                "block_changes": True,
            },
            priority=200,  # Highest priority
        )

    @staticmethod
    def roas_threshold_rule(min_roas: float = 1.0) -> Rule:
        """
        ROAS Threshold Rule: Alert when ROAS falls below breakeven.

        For e-commerce campaigns with trackable revenue.
        """
        return Rule(
            id="ads_roas_threshold",
            name="Low ROAS Alert",
            description=f"Alert when ROAS < {min_roas:.1f}",
            condition=lambda ctx: (
                ctx.get("roas", float("inf")) < min_roas
                and ctx.get("spend", 0) >= 100  # Minimum spend for significance
            ),
            action=RuleAction.ALERT,
            action_params={
                "alert_type": "low_roas",
                "message": "ROAS below breakeven - review campaign",
            },
            priority=40,
        )


def setup_ads_rules(engine: RulesEngine, target_cpa: float, daily_budget: float) -> None:
    """
    Set up standard ads rules for a product.

    Args:
        engine: The rules engine to register rules with
        target_cpa: Target cost per acquisition
        daily_budget: Daily ad budget
    """
    rules = [
        AdsRules.learning_phase_protection_rule(),
        AdsRules.three_x_kill_rule(target_cpa),
        AdsRules.scale_winner_rule(target_cpa),
        AdsRules.creative_fatigue_rule(),
        AdsRules.budget_pacing_rule(daily_budget),
        AdsRules.ctr_drop_rule(),
        AdsRules.roas_threshold_rule(),
    ]

    for rule in rules:
        engine.register_rule("ads", rule)
