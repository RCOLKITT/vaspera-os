"""
Monitor Agent - Watches health metrics across all products.

Detects anomalies, tracks performance, and triggers alerts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

import structlog

from ..base import AgentResult, BaseAgent

logger = structlog.get_logger()


class HealthStatus(Enum):
    """Health status levels."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class ProductHealth:
    """Health metrics for a single product."""

    product_id: str
    status: HealthStatus
    error_rate: float  # Percentage (0-100)
    response_time_p95: float  # Milliseconds
    uptime: float  # Percentage (0-100)
    active_users: int
    last_deploy: datetime | None
    open_incidents: int
    checked_at: datetime

    @property
    def is_healthy(self) -> bool:
        """Check if product is healthy."""
        return (
            self.error_rate < 1.0
            and self.response_time_p95 < 2000
            and self.uptime >= 99.9
            and self.open_incidents == 0
        )


@dataclass
class Alert:
    """An alert triggered by the monitor."""

    product_id: str
    severity: str  # critical, warning, info
    title: str
    message: str
    metric: str
    current_value: float
    threshold: float
    created_at: datetime


class MonitorAgent(BaseAgent):
    """
    Monitor Agent - Watches health metrics across all products.

    Responsibilities:
    - Poll health metrics from Sentry, Vercel, PostHog
    - Detect anomalies and threshold violations
    - Trigger alerts and escalations
    - Generate health reports
    """

    def __init__(
        self,
        products_config: dict[str, dict[str, Any]],
        thresholds: dict[str, Any] | None = None,
        model: str = "claude-haiku-4-20250514",
    ) -> None:
        super().__init__(
            agent_id="monitor_agent",
            name="Monitor Agent",
            role="Site Reliability Engineer",
            goal="Keep all products healthy and performant",
            backstory="""You watch over all Vaspera products 24/7. You detect anomalies,
            track performance metrics, and escalate issues before they impact users.""",
            model=model,
        )

        self.products_config = products_config
        self.thresholds = thresholds or {
            "error_rate": 1.0,  # 1% error rate triggers warning
            "error_rate_critical": 5.0,  # 5% triggers critical
            "response_time_p95": 2000,  # 2s p95 triggers warning
            "response_time_critical": 5000,  # 5s triggers critical
            "uptime": 99.9,  # 99.9% minimum uptime
        }

    def get_tools(self) -> list[Any]:
        """Return the tools available to this agent."""
        # TODO: Return actual MCP tools (Sentry, Vercel, PostHog)
        return []

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """
        Execute the monitoring cycle.

        1. Fetch health metrics from all products
        2. Evaluate against thresholds
        3. Generate alerts for violations
        4. Return health summary
        """
        actions_taken = []
        alerts: list[Alert] = []

        try:
            # Fetch health for all products
            health_reports: list[ProductHealth] = []
            for product_id in self.products_config.keys():
                health = await self._fetch_product_health(product_id)
                health_reports.append(health)

                # Check thresholds and generate alerts
                product_alerts = self._evaluate_thresholds(health)
                alerts.extend(product_alerts)

                if product_alerts:
                    actions_taken.append(
                        f"alert:{product_id}:{len(product_alerts)}_issues"
                    )

            # Generate summary
            summary = self._generate_summary(health_reports, alerts)

            # Send alerts if any critical issues
            if any(a.severity == "critical" for a in alerts):
                await self._send_alerts(alerts)
                actions_taken.append("sent_critical_alerts")

            return AgentResult(
                agent_id=self.agent_id,
                success=True,
                output=summary,
                actions_taken=actions_taken,
            )

        except Exception as e:
            self._logger.error("Monitor agent failed", error=str(e))
            return AgentResult(
                agent_id=self.agent_id,
                success=False,
                output=None,
                errors=[str(e)],
            )

    async def _fetch_product_health(self, product_id: str) -> ProductHealth:
        """
        Fetch health metrics for a product.

        TODO: Implement actual API calls via MCP servers:
        - Sentry for error rates
        - Vercel for deployment status and response times
        - PostHog for active users
        """
        # Mock data for now
        return ProductHealth(
            product_id=product_id,
            status=HealthStatus.HEALTHY,
            error_rate=0.5,
            response_time_p95=450,
            uptime=99.99,
            active_users=150,
            last_deploy=datetime.utcnow() - timedelta(hours=6),
            open_incidents=0,
            checked_at=datetime.utcnow(),
        )

    def _evaluate_thresholds(self, health: ProductHealth) -> list[Alert]:
        """Evaluate health metrics against thresholds."""
        alerts = []
        now = datetime.utcnow()

        # Error rate check
        if health.error_rate >= self.thresholds["error_rate_critical"]:
            alerts.append(
                Alert(
                    product_id=health.product_id,
                    severity="critical",
                    title=f"Critical error rate: {health.product_id}",
                    message=f"Error rate is {health.error_rate:.2f}%, above critical threshold",
                    metric="error_rate",
                    current_value=health.error_rate,
                    threshold=self.thresholds["error_rate_critical"],
                    created_at=now,
                )
            )
        elif health.error_rate >= self.thresholds["error_rate"]:
            alerts.append(
                Alert(
                    product_id=health.product_id,
                    severity="warning",
                    title=f"Elevated error rate: {health.product_id}",
                    message=f"Error rate is {health.error_rate:.2f}%, above warning threshold",
                    metric="error_rate",
                    current_value=health.error_rate,
                    threshold=self.thresholds["error_rate"],
                    created_at=now,
                )
            )

        # Response time check
        if health.response_time_p95 >= self.thresholds["response_time_critical"]:
            alerts.append(
                Alert(
                    product_id=health.product_id,
                    severity="critical",
                    title=f"Critical latency: {health.product_id}",
                    message=f"P95 response time is {health.response_time_p95:.0f}ms",
                    metric="response_time_p95",
                    current_value=health.response_time_p95,
                    threshold=self.thresholds["response_time_critical"],
                    created_at=now,
                )
            )
        elif health.response_time_p95 >= self.thresholds["response_time_p95"]:
            alerts.append(
                Alert(
                    product_id=health.product_id,
                    severity="warning",
                    title=f"Elevated latency: {health.product_id}",
                    message=f"P95 response time is {health.response_time_p95:.0f}ms",
                    metric="response_time_p95",
                    current_value=health.response_time_p95,
                    threshold=self.thresholds["response_time_p95"],
                    created_at=now,
                )
            )

        # Uptime check
        if health.uptime < self.thresholds["uptime"]:
            alerts.append(
                Alert(
                    product_id=health.product_id,
                    severity="critical",
                    title=f"Uptime below SLA: {health.product_id}",
                    message=f"Uptime is {health.uptime:.2f}%, below {self.thresholds['uptime']}% SLA",
                    metric="uptime",
                    current_value=health.uptime,
                    threshold=self.thresholds["uptime"],
                    created_at=now,
                )
            )

        return alerts

    def _generate_summary(
        self,
        health_reports: list[ProductHealth],
        alerts: list[Alert],
    ) -> dict[str, Any]:
        """Generate a health summary."""
        healthy_count = sum(1 for h in health_reports if h.is_healthy)
        total_count = len(health_reports)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": "healthy" if healthy_count == total_count else "degraded",
            "products": {
                "total": total_count,
                "healthy": healthy_count,
                "degraded": total_count - healthy_count,
            },
            "alerts": {
                "total": len(alerts),
                "critical": sum(1 for a in alerts if a.severity == "critical"),
                "warning": sum(1 for a in alerts if a.severity == "warning"),
            },
            "health_by_product": {
                h.product_id: {
                    "status": h.status.value,
                    "error_rate": h.error_rate,
                    "response_time_p95": h.response_time_p95,
                    "uptime": h.uptime,
                    "active_users": h.active_users,
                }
                for h in health_reports
            },
        }

    async def _send_alerts(self, alerts: list[Alert]) -> None:
        """
        Send alerts via configured channels.

        TODO: Implement via Slack MCP, email, PagerDuty
        """
        for alert in alerts:
            if alert.severity == "critical":
                self._logger.critical(
                    "CRITICAL ALERT",
                    product_id=alert.product_id,
                    title=alert.title,
                    message=alert.message,
                )
            else:
                self._logger.warning(
                    "Alert",
                    product_id=alert.product_id,
                    title=alert.title,
                    message=alert.message,
                )
