"""
Content Agent - Creates and distributes content across products.

Generates blog posts, changelogs, social media, and newsletters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

import structlog

from ..base import AgentResult, BaseAgent

logger = structlog.get_logger()


class ContentType(Enum):
    """Types of content."""

    BLOG_POST = "blog_post"
    CHANGELOG = "changelog"
    SOCIAL_POST = "social_post"
    NEWSLETTER = "newsletter"
    DOCUMENTATION = "documentation"
    ANNOUNCEMENT = "announcement"


class Platform(Enum):
    """Distribution platforms."""

    BLOG = "blog"  # Ghost, company blog
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    NEWSLETTER = "newsletter"  # Email
    GITHUB = "github"  # Release notes
    DISCORD = "discord"


@dataclass
class ContentPiece:
    """A piece of content to be created/distributed."""

    content_id: str
    product_id: str
    content_type: ContentType
    title: str
    body: str
    summary: str | None = None
    platforms: list[Platform] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    status: str = "draft"  # draft, review, approved, published
    created_at: datetime = field(default_factory=datetime.utcnow)
    published_at: datetime | None = None


@dataclass
class ContentCalendar:
    """Weekly content calendar."""

    week_start: datetime
    items: list[dict[str, Any]] = field(default_factory=list)


class ContentAgent(BaseAgent):
    """
    Content Agent - Creates and distributes content for all products.

    Responsibilities:
    - Generate blog posts from product updates
    - Create changelogs from GitHub releases
    - Draft social media posts
    - Manage content calendar
    - Submit content for human approval before publishing
    """

    def __init__(
        self,
        products_config: dict[str, dict[str, Any]],
        model: str = "claude-sonnet-4-20250514",
    ) -> None:
        super().__init__(
            agent_id="content_agent",
            name="Content Agent",
            role="Content Marketing Manager",
            goal="Create and distribute engaging content for all products",
            backstory="""You create blog posts, changelogs, social media content, and
            newsletters. You maintain each product's brand voice while driving
            engagement and organic growth.""",
            model=model,
        )

        self.products_config = products_config

        # Brand voice guidelines per product type
        self.brand_voices = {
            "saas": "Professional, helpful, technical but accessible",
            "open-source-saas": "Developer-friendly, authentic, community-focused",
            "consumer-app": "Friendly, motivational, approachable",
            "fintech": "Trustworthy, precise, professional",
        }

    def get_tools(self) -> list[Any]:
        """Return the tools available to this agent."""
        # TODO: Return actual MCP tools (Ghost, GitHub, Twitter, LinkedIn)
        return []

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """
        Execute content creation/distribution.

        Context can contain:
        - action: "create", "distribute", "calendar"
        - content_type: ContentType value
        - product_id: str
        - source_data: dict (e.g., release notes, feature info)
        """
        actions_taken = []

        try:
            action = context.get("action", "create")

            if action == "create":
                result = await self._create_content(context)
                actions_taken.append(f"created:{result['content_type']}")

            elif action == "distribute":
                result = await self._distribute_content(context)
                actions_taken.append(f"distributed:{len(result['platforms'])}_platforms")

            elif action == "calendar":
                result = await self._generate_calendar(context)
                actions_taken.append(f"calendar:{len(result['items'])}_items")

            elif action == "changelog":
                result = await self._generate_changelog(context)
                actions_taken.append(f"changelog:{result['product_id']}")

            else:
                result = {"error": f"Unknown action: {action}"}

            return AgentResult(
                agent_id=self.agent_id,
                success=True,
                output=result,
                actions_taken=actions_taken,
            )

        except Exception as e:
            self._logger.error("Content agent failed", error=str(e))
            return AgentResult(
                agent_id=self.agent_id,
                success=False,
                output=None,
                errors=[str(e)],
            )

    async def _create_content(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Create a piece of content.

        TODO: Implement actual AI content generation via Claude API.
        """
        product_id = context.get("product_id", "unknown")
        content_type = context.get("content_type", ContentType.BLOG_POST.value)
        source_data = context.get("source_data", {})

        product_config = self.products_config.get(product_id, {})
        product_name = product_config.get("name", product_id)
        product_type = product_config.get("type", "saas")
        brand_voice = self.brand_voices.get(product_type, self.brand_voices["saas"])

        # Mock content generation
        if content_type == ContentType.BLOG_POST.value:
            content = ContentPiece(
                content_id=f"blog_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                product_id=product_id,
                content_type=ContentType.BLOG_POST,
                title=f"What's New in {product_name}",
                body=f"# What's New in {product_name}\n\n"
                     f"We're excited to share the latest updates...\n\n"
                     f"## New Features\n\n"
                     f"- Feature 1: Description\n"
                     f"- Feature 2: Description\n\n"
                     f"## Getting Started\n\n"
                     f"To try these new features...",
                summary=f"Latest updates and features in {product_name}",
                platforms=[Platform.BLOG, Platform.TWITTER, Platform.LINKEDIN],
                tags=["product-update", "features", product_id],
                status="draft",
            )

        elif content_type == ContentType.SOCIAL_POST.value:
            content = ContentPiece(
                content_id=f"social_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                product_id=product_id,
                content_type=ContentType.SOCIAL_POST,
                title="",
                body=f"Exciting news from {product_name}! Check out our latest features.",
                platforms=[Platform.TWITTER, Platform.LINKEDIN],
                tags=[product_id],
                status="draft",
            )

        else:
            content = ContentPiece(
                content_id=f"content_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                product_id=product_id,
                content_type=ContentType(content_type),
                title=f"{product_name} Update",
                body="Content body placeholder",
                status="draft",
            )

        return {
            "content_id": content.content_id,
            "content_type": content.content_type.value,
            "title": content.title,
            "body": content.body,
            "status": content.status,
            "platforms": [p.value for p in content.platforms],
            "requires_approval": True,
            "brand_voice": brand_voice,
        }

    async def _distribute_content(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Distribute approved content to platforms.

        TODO: Implement actual distribution via platform APIs.
        """
        content_id = context.get("content_id", "unknown")
        platforms = context.get("platforms", [])

        # Mock distribution
        results = {}
        for platform in platforms:
            results[platform] = {
                "status": "published",
                "url": f"https://{platform}.com/post/{content_id}",
                "published_at": datetime.utcnow().isoformat(),
            }

        return {
            "content_id": content_id,
            "platforms": platforms,
            "results": results,
        }

    async def _generate_calendar(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Generate a weekly content calendar.

        Creates a schedule of content to be created and distributed.
        """
        items = []

        # For each product, plan content
        for product_id, config in self.products_config.items():
            product_name = config.get("name", product_id)

            # Weekly blog post
            items.append({
                "day": "Monday",
                "product_id": product_id,
                "content_type": ContentType.BLOG_POST.value,
                "title": f"Weekly Tips: {product_name}",
                "platforms": ["blog", "linkedin"],
            })

            # Social posts (3x per week)
            for day in ["Tuesday", "Thursday", "Saturday"]:
                items.append({
                    "day": day,
                    "product_id": product_id,
                    "content_type": ContentType.SOCIAL_POST.value,
                    "title": f"{product_name} tip of the day",
                    "platforms": ["twitter", "linkedin"],
                })

        return {
            "week_of": datetime.utcnow().isoformat(),
            "items": items,
            "total_pieces": len(items),
        }

    async def _generate_changelog(self, context: dict[str, Any]) -> dict[str, Any]:
        """
        Generate a changelog from GitHub release data.

        TODO: Implement actual GitHub API integration to fetch releases.
        """
        product_id = context.get("product_id", "unknown")
        release_data = context.get("release_data", {})

        product_config = self.products_config.get(product_id, {})
        product_name = product_config.get("name", product_id)

        # Mock changelog
        changelog = f"""# {product_name} Changelog

## v1.2.0 - {datetime.utcnow().strftime('%Y-%m-%d')}

### New Features
- Added new feature X
- Improved performance of Y

### Bug Fixes
- Fixed issue with Z
- Resolved edge case in W

### Breaking Changes
- None

---
*Full release notes available on GitHub*
"""

        return {
            "product_id": product_id,
            "version": "1.2.0",
            "changelog": changelog,
            "status": "draft",
            "requires_approval": True,
        }
