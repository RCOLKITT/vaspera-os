"""
Scheduler - Cron-like scheduling for VasperaOS agents.

Triggers agents based on time-based schedules.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from .events import Event, get_event_bus

logger = structlog.get_logger()


class Scheduler:
    """
    Scheduler for VasperaOS.

    Manages time-based triggers for agents using APScheduler.
    """

    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler()
        self._event_bus = get_event_bus()

    def add_interval_job(
        self,
        job_id: str,
        event_type: str,
        interval_minutes: int,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Add a job that runs at fixed intervals."""
        self._scheduler.add_job(
            self._emit_event,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id=job_id,
            kwargs={
                "event_type": event_type,
                "payload": payload or {},
                "source": f"scheduler:{job_id}",
            },
            replace_existing=True,
        )
        logger.info(
            "Added interval job",
            job_id=job_id,
            interval_minutes=interval_minutes,
        )

    def add_cron_job(
        self,
        job_id: str,
        event_type: str,
        cron_expression: str,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Add a job that runs on a cron schedule."""
        # Parse cron expression (minute hour day month day_of_week)
        parts = cron_expression.split()
        trigger = CronTrigger(
            minute=parts[0] if len(parts) > 0 else "*",
            hour=parts[1] if len(parts) > 1 else "*",
            day=parts[2] if len(parts) > 2 else "*",
            month=parts[3] if len(parts) > 3 else "*",
            day_of_week=parts[4] if len(parts) > 4 else "*",
        )

        self._scheduler.add_job(
            self._emit_event,
            trigger=trigger,
            id=job_id,
            kwargs={
                "event_type": event_type,
                "payload": payload or {},
                "source": f"scheduler:{job_id}",
            },
            replace_existing=True,
        )
        logger.info(
            "Added cron job",
            job_id=job_id,
            cron=cron_expression,
        )

    def add_daily_job(
        self,
        job_id: str,
        event_type: str,
        hour: int = 9,
        minute: int = 0,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Add a job that runs daily at a specific time."""
        self._scheduler.add_job(
            self._emit_event,
            trigger=CronTrigger(hour=hour, minute=minute),
            id=job_id,
            kwargs={
                "event_type": event_type,
                "payload": payload or {},
                "source": f"scheduler:{job_id}",
            },
            replace_existing=True,
        )
        logger.info(
            "Added daily job",
            job_id=job_id,
            time=f"{hour:02d}:{minute:02d}",
        )

    def add_weekly_job(
        self,
        job_id: str,
        event_type: str,
        day_of_week: str = "mon",
        hour: int = 9,
        minute: int = 0,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Add a job that runs weekly on a specific day."""
        self._scheduler.add_job(
            self._emit_event,
            trigger=CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute),
            id=job_id,
            kwargs={
                "event_type": event_type,
                "payload": payload or {},
                "source": f"scheduler:{job_id}",
            },
            replace_existing=True,
        )
        logger.info(
            "Added weekly job",
            job_id=job_id,
            day=day_of_week,
            time=f"{hour:02d}:{minute:02d}",
        )

    async def _emit_event(
        self,
        event_type: str,
        payload: dict[str, Any],
        source: str,
    ) -> None:
        """Emit an event to the event bus."""
        event = Event(
            type=event_type,
            payload={**payload, "scheduled_at": datetime.utcnow().isoformat()},
            source=source,
        )
        await self._event_bus.publish(event)

    def start(self) -> None:
        """Start the scheduler."""
        self._scheduler.start()
        logger.info("Scheduler started")

    def stop(self) -> None:
        """Stop the scheduler."""
        self._scheduler.shutdown()
        logger.info("Scheduler stopped")

    def list_jobs(self) -> list[dict[str, Any]]:
        """List all scheduled jobs."""
        jobs = []
        for job in self._scheduler.get_jobs():
            jobs.append(
                {
                    "id": job.id,
                    "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                    "trigger": str(job.trigger),
                }
            )
        return jobs


def setup_default_schedules(scheduler: Scheduler) -> None:
    """Set up default schedules for VasperaOS."""
    # Monitor agent - every 5 minutes
    scheduler.add_interval_job(
        job_id="monitor_health_check",
        event_type="schedule.health_check",
        interval_minutes=5,
    )

    # Ads agent - every 6 hours
    scheduler.add_interval_job(
        job_id="ads_optimization",
        event_type="schedule.ads_optimization",
        interval_minutes=360,
    )

    # Daily revenue report - 9 AM
    scheduler.add_daily_job(
        job_id="daily_revenue_report",
        event_type="schedule.daily_revenue",
        hour=9,
        minute=0,
    )

    # Weekly content calendar - Monday 9 AM
    scheduler.add_weekly_job(
        job_id="weekly_content_calendar",
        event_type="schedule.weekly_content",
        day_of_week="mon",
        hour=9,
        minute=0,
    )

    # Weekly SEO audit - Tuesday 10 AM
    scheduler.add_weekly_job(
        job_id="weekly_seo_audit",
        event_type="schedule.weekly_seo",
        day_of_week="tue",
        hour=10,
        minute=0,
    )

    logger.info("Default schedules configured")
