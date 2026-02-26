"""
Rules Engine - Configurable automation rules for VasperaOS.

Rules define conditions and actions for automated decision-making.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

import structlog

logger = structlog.get_logger()


class RuleAction(Enum):
    """Standard rule actions."""

    PAUSE = "pause"
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    ALERT = "alert"
    RESTART = "restart"
    ROLLBACK = "rollback"
    NOTIFY = "notify"
    CREATE_TICKET = "create_ticket"
    SEND_EMAIL = "send_email"


@dataclass
class Rule:
    """A single automation rule."""

    id: str
    name: str
    description: str
    condition: Callable[[dict[str, Any]], bool]
    action: RuleAction
    action_params: dict[str, Any] | None = None
    enabled: bool = True
    priority: int = 0  # Higher = runs first

    def evaluate(self, context: dict[str, Any]) -> bool:
        """Evaluate if the rule condition is met."""
        if not self.enabled:
            return False
        try:
            return self.condition(context)
        except Exception as e:
            logger.error(
                "Rule evaluation error",
                rule_id=self.id,
                error=str(e),
            )
            return False


class RulesEngine:
    """
    Rules engine for VasperaOS.

    Evaluates rules against data and returns actions to take.
    """

    def __init__(self) -> None:
        self._rules: dict[str, list[Rule]] = {}  # domain -> rules
        self._action_handlers: dict[RuleAction, Callable] = {}

    def register_rule(self, domain: str, rule: Rule) -> None:
        """Register a rule for a domain."""
        if domain not in self._rules:
            self._rules[domain] = []
        self._rules[domain].append(rule)
        # Sort by priority (descending)
        self._rules[domain].sort(key=lambda r: r.priority, reverse=True)
        logger.info("Registered rule", domain=domain, rule_id=rule.id)

    def register_action_handler(
        self,
        action: RuleAction,
        handler: Callable[[dict[str, Any]], Any],
    ) -> None:
        """Register a handler for an action type."""
        self._action_handlers[action] = handler

    def evaluate(
        self,
        domain: str,
        context: dict[str, Any],
    ) -> list[tuple[Rule, dict[str, Any]]]:
        """
        Evaluate all rules in a domain against context.

        Returns list of (rule, action_params) for triggered rules.
        """
        triggered = []
        rules = self._rules.get(domain, [])

        for rule in rules:
            if rule.evaluate(context):
                logger.info(
                    "Rule triggered",
                    domain=domain,
                    rule_id=rule.id,
                    rule_name=rule.name,
                )
                triggered.append((rule, rule.action_params or {}))

        return triggered

    async def evaluate_and_execute(
        self,
        domain: str,
        context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Evaluate rules and execute actions for triggered rules."""
        triggered = self.evaluate(domain, context)
        results = []

        for rule, action_params in triggered:
            handler = self._action_handlers.get(rule.action)
            if handler:
                try:
                    result = handler({**context, **action_params})
                    results.append(
                        {
                            "rule_id": rule.id,
                            "action": rule.action.value,
                            "result": result,
                        }
                    )
                except Exception as e:
                    logger.error(
                        "Action execution error",
                        rule_id=rule.id,
                        action=rule.action.value,
                        error=str(e),
                    )
                    results.append(
                        {
                            "rule_id": rule.id,
                            "action": rule.action.value,
                            "error": str(e),
                        }
                    )
            else:
                logger.warning(
                    "No handler for action",
                    rule_id=rule.id,
                    action=rule.action.value,
                )

        return results

    def list_rules(self, domain: str | None = None) -> list[dict[str, Any]]:
        """List all rules, optionally filtered by domain."""
        rules = []
        domains = [domain] if domain else list(self._rules.keys())

        for d in domains:
            for rule in self._rules.get(d, []):
                rules.append(
                    {
                        "domain": d,
                        "id": rule.id,
                        "name": rule.name,
                        "description": rule.description,
                        "action": rule.action.value,
                        "enabled": rule.enabled,
                        "priority": rule.priority,
                    }
                )

        return rules
