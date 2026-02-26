"""
Event Bus - Central event routing for VasperaOS.

Events flow through here to trigger agents.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

import structlog

logger = structlog.get_logger()


@dataclass
class Event:
    """A single event in the system."""

    type: str
    payload: dict[str, Any]
    source: str
    product_id: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)


EventHandler = Callable[[Event], Any]


class EventBus:
    """
    Central event bus for VasperaOS.

    Routes events to registered handlers (agents).
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}
        self._queue: asyncio.Queue[Event] = asyncio.Queue()
        self._running = False

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Subscribe a handler to an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.info("Subscribed handler", event_type=event_type)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        """Unsubscribe a handler from an event type."""
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)

    async def publish(self, event: Event) -> None:
        """Publish an event to the bus."""
        await self._queue.put(event)
        logger.info(
            "Event published",
            event_id=event.id,
            event_type=event.type,
            source=event.source,
        )

    async def publish_sync(
        self,
        event_type: str,
        payload: dict[str, Any],
        source: str,
        product_id: str | None = None,
    ) -> list[Any]:
        """Publish an event and wait for all handlers to complete."""
        event = Event(
            type=event_type,
            payload=payload,
            source=source,
            product_id=product_id,
        )

        results = []
        handlers = self._handlers.get(event_type, [])
        handlers.extend(self._handlers.get("*", []))  # Wildcard handlers

        for handler in handlers:
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    result = await result
                results.append(result)
            except Exception as e:
                logger.error(
                    "Handler error",
                    event_type=event_type,
                    error=str(e),
                )
                results.append({"error": str(e)})

        return results

    async def start(self) -> None:
        """Start processing events from the queue."""
        self._running = True
        logger.info("Event bus started")

        while self._running:
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                await self._process_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error("Event processing error", error=str(e))

    async def stop(self) -> None:
        """Stop processing events."""
        self._running = False
        logger.info("Event bus stopped")

    async def _process_event(self, event: Event) -> None:
        """Process a single event."""
        handlers = self._handlers.get(event.type, [])
        handlers.extend(self._handlers.get("*", []))  # Wildcard handlers

        logger.info(
            "Processing event",
            event_id=event.id,
            event_type=event.type,
            handler_count=len(handlers),
        )

        for handler in handlers:
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.error(
                    "Handler error",
                    event_id=event.id,
                    event_type=event.type,
                    error=str(e),
                )


# Common event types
class EventTypes:
    """Standard event types in VasperaOS."""

    # GitHub events
    GITHUB_ISSUE_CREATED = "github.issue.created"
    GITHUB_ISSUE_UPDATED = "github.issue.updated"
    GITHUB_PR_OPENED = "github.pr.opened"
    GITHUB_PR_MERGED = "github.pr.merged"
    GITHUB_RELEASE = "github.release"

    # Monitoring events
    ERROR_SPIKE = "monitoring.error_spike"
    LATENCY_SPIKE = "monitoring.latency_spike"
    DOWNTIME = "monitoring.downtime"

    # Support events
    CHAT_MESSAGE = "support.chat_message"
    TICKET_CREATED = "support.ticket_created"
    ESCALATION = "support.escalation"

    # Revenue events
    SIGNUP = "revenue.signup"
    SUBSCRIPTION_CREATED = "revenue.subscription_created"
    SUBSCRIPTION_CANCELLED = "revenue.subscription_cancelled"
    PAYMENT_RECEIVED = "revenue.payment_received"

    # Marketing events
    AD_THRESHOLD = "marketing.ad_threshold"
    CONTENT_PUBLISHED = "marketing.content_published"

    # Scheduled events
    SCHEDULE_DAILY = "schedule.daily"
    SCHEDULE_WEEKLY = "schedule.weekly"
    SCHEDULE_HOURLY = "schedule.hourly"


# Singleton instance
_event_bus: EventBus | None = None


def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus
