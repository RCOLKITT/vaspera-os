#!/usr/bin/env python3
"""
VasperaOS Agent Runner

Starts the agent orchestrator and begins processing events.
"""

import asyncio
import signal
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer(),
    ]
)

logger = structlog.get_logger()


async def main() -> None:
    """Main entry point."""
    from src.core.orchestrator import get_orchestrator
    from src.core.events import get_event_bus
    from src.core.scheduler import Scheduler, setup_default_schedules

    logger.info("Starting VasperaOS...")

    # Initialize components
    orchestrator = get_orchestrator()
    event_bus = get_event_bus()
    scheduler = Scheduler()

    # Set up default schedules
    setup_default_schedules(scheduler)

    # Register event handlers
    async def handle_event(event):
        await orchestrator.handle_event(event.type, event.payload)

    event_bus.subscribe("*", handle_event)

    # Start components
    scheduler.start()
    event_bus_task = asyncio.create_task(event_bus.start())

    logger.info(
        "VasperaOS started",
        products=orchestrator.list_products(),
        agents=orchestrator.list_agents(),
    )

    # Handle shutdown
    shutdown_event = asyncio.Event()

    def signal_handler(sig, frame):
        logger.info("Shutdown signal received")
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Wait for shutdown
    await shutdown_event.wait()

    # Cleanup
    logger.info("Shutting down...")
    await event_bus.stop()
    scheduler.stop()
    event_bus_task.cancel()

    logger.info("VasperaOS stopped")


if __name__ == "__main__":
    asyncio.run(main())
