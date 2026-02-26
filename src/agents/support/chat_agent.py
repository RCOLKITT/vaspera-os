"""
Chat Agent - Handles customer support conversations.

Uses AI to answer questions, with escalation to humans when needed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

import structlog

from ..base import AgentResult, BaseAgent

logger = structlog.get_logger()


class MessageType(Enum):
    """Types of support messages."""

    QUESTION = "question"
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    BILLING = "billing"
    COMPLAINT = "complaint"
    FEEDBACK = "feedback"
    OTHER = "other"


class EscalationReason(Enum):
    """Reasons for escalating to human."""

    BILLING_ISSUE = "billing_issue"
    REFUND_REQUEST = "refund_request"
    COMPLEX_TECHNICAL = "complex_technical"
    ANGRY_CUSTOMER = "angry_customer"
    LEGAL_COMPLIANCE = "legal_compliance"
    CANNOT_RESOLVE = "cannot_resolve"
    HUMAN_REQUESTED = "human_requested"


@dataclass
class Conversation:
    """A support conversation."""

    conversation_id: str
    product_id: str
    user_id: str
    user_email: str
    messages: list[dict[str, Any]] = field(default_factory=list)
    message_type: MessageType = MessageType.OTHER
    resolved: bool = False
    escalated: bool = False
    escalation_reason: EscalationReason | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ChatResponse:
    """Response from the chat agent."""

    message: str
    resolved: bool
    escalate: bool
    escalation_reason: EscalationReason | None = None
    suggested_actions: list[str] = field(default_factory=list)
    confidence: float = 1.0


class ChatAgent(BaseAgent):
    """
    Chat Agent - Handles customer support conversations.

    Responsibilities:
    - Answer common questions using product documentation
    - Classify message types (question, bug, billing, etc.)
    - Resolve simple issues automatically
    - Escalate complex issues to humans
    - Track conversation context via VasperaMemory
    """

    def __init__(
        self,
        products_config: dict[str, dict[str, Any]],
        model: str = "claude-haiku-4-20250514",
    ) -> None:
        super().__init__(
            agent_id="chat_agent",
            name="Chat Agent",
            role="Customer Support Representative",
            goal="Answer customer questions accurately and quickly",
            backstory="""You are the frontline of customer support. You have full context
            of all products and can answer most questions instantly. You are friendly,
            helpful, and know when to escalate to humans.""",
            model=model,
        )

        self.products_config = products_config
        self.escalation_triggers = {
            "billing", "refund", "cancel", "lawsuit", "lawyer",
            "angry", "furious", "unacceptable", "speak to human",
            "talk to someone", "manager", "supervisor"
        }

    def get_tools(self) -> list[Any]:
        """Return the tools available to this agent."""
        # TODO: Return actual MCP tools (Chatwoot, VasperaMemory, docs search)
        return []

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """
        Process a support conversation.

        Context should contain:
        - conversation_id: str
        - product_id: str
        - user_message: str
        - user_id: str
        - user_email: str
        - conversation_history: list (optional)
        """
        actions_taken = []

        try:
            # Extract context
            conversation_id = context.get("conversation_id", "unknown")
            product_id = context.get("product_id", "unknown")
            user_message = context.get("user_message", "")
            user_id = context.get("user_id", "unknown")
            user_email = context.get("user_email", "")
            history = context.get("conversation_history", [])

            # Classify the message
            message_type = self._classify_message(user_message)
            actions_taken.append(f"classified:{message_type.value}")

            # Check for escalation triggers
            needs_escalation, escalation_reason = self._check_escalation(
                user_message, message_type
            )

            if needs_escalation:
                response = ChatResponse(
                    message=self._get_escalation_message(escalation_reason),
                    resolved=False,
                    escalate=True,
                    escalation_reason=escalation_reason,
                )
                actions_taken.append(f"escalated:{escalation_reason.value}")
            else:
                # Generate AI response
                response = await self._generate_response(
                    product_id=product_id,
                    user_message=user_message,
                    message_type=message_type,
                    history=history,
                )
                actions_taken.append(f"responded:confidence={response.confidence:.2f}")

            return AgentResult(
                agent_id=self.agent_id,
                success=True,
                output={
                    "conversation_id": conversation_id,
                    "response": response.message,
                    "resolved": response.resolved,
                    "escalated": response.escalate,
                    "escalation_reason": response.escalation_reason.value if response.escalation_reason else None,
                    "message_type": message_type.value,
                    "suggested_actions": response.suggested_actions,
                },
                actions_taken=actions_taken,
            )

        except Exception as e:
            self._logger.error("Chat agent failed", error=str(e))
            return AgentResult(
                agent_id=self.agent_id,
                success=False,
                output=None,
                errors=[str(e)],
            )

    def _classify_message(self, message: str) -> MessageType:
        """Classify the type of support message."""
        message_lower = message.lower()

        if any(word in message_lower for word in ["bug", "error", "broken", "doesn't work", "crash"]):
            return MessageType.BUG_REPORT

        if any(word in message_lower for word in ["feature", "add", "would be nice", "suggestion"]):
            return MessageType.FEATURE_REQUEST

        if any(word in message_lower for word in ["bill", "charge", "payment", "invoice", "subscription", "refund"]):
            return MessageType.BILLING

        if any(word in message_lower for word in ["terrible", "awful", "worst", "hate", "disappointed"]):
            return MessageType.COMPLAINT

        if any(word in message_lower for word in ["love", "great", "thanks", "awesome", "feedback"]):
            return MessageType.FEEDBACK

        if any(word in message_lower for word in ["how", "what", "why", "where", "can i", "is it possible"]):
            return MessageType.QUESTION

        return MessageType.OTHER

    def _check_escalation(
        self, message: str, message_type: MessageType
    ) -> tuple[bool, EscalationReason | None]:
        """Check if message should be escalated to human."""
        message_lower = message.lower()

        # Always escalate billing issues
        if message_type == MessageType.BILLING:
            return True, EscalationReason.BILLING_ISSUE

        # Check for refund requests
        if "refund" in message_lower:
            return True, EscalationReason.REFUND_REQUEST

        # Check for angry customers
        if any(word in message_lower for word in ["angry", "furious", "unacceptable", "lawsuit", "lawyer"]):
            return True, EscalationReason.ANGRY_CUSTOMER

        # Check for explicit human request
        if any(phrase in message_lower for phrase in ["speak to human", "talk to someone", "real person", "manager"]):
            return True, EscalationReason.HUMAN_REQUESTED

        return False, None

    def _get_escalation_message(self, reason: EscalationReason) -> str:
        """Get the message to send when escalating."""
        messages = {
            EscalationReason.BILLING_ISSUE: (
                "I understand you have a billing question. Let me connect you with our "
                "billing team who can help you directly. Someone will be with you shortly."
            ),
            EscalationReason.REFUND_REQUEST: (
                "I see you're requesting a refund. I'm connecting you with our support team "
                "who can process this for you. Please hold on."
            ),
            EscalationReason.ANGRY_CUSTOMER: (
                "I'm sorry you're having a frustrating experience. Let me connect you with "
                "a senior support representative who can help resolve this right away."
            ),
            EscalationReason.HUMAN_REQUESTED: (
                "Of course! I'm connecting you with a human support representative now. "
                "Someone will be with you shortly."
            ),
            EscalationReason.COMPLEX_TECHNICAL: (
                "This looks like a complex technical issue. Let me connect you with our "
                "engineering support team for specialized assistance."
            ),
            EscalationReason.CANNOT_RESOLVE: (
                "I want to make sure you get the best help possible. Let me connect you "
                "with a human representative who can assist further."
            ),
        }
        return messages.get(reason, messages[EscalationReason.CANNOT_RESOLVE])

    async def _generate_response(
        self,
        product_id: str,
        user_message: str,
        message_type: MessageType,
        history: list[dict[str, Any]],
    ) -> ChatResponse:
        """
        Generate an AI response to the user.

        TODO: Implement actual AI response generation via Claude API
        with product documentation context from VasperaMemory.
        """
        # Mock response for now
        product_name = self.products_config.get(product_id, {}).get("name", product_id)

        if message_type == MessageType.QUESTION:
            return ChatResponse(
                message=(
                    f"Thanks for reaching out about {product_name}! "
                    f"I'd be happy to help answer your question. "
                    f"Based on our documentation, here's what I found..."
                ),
                resolved=False,
                escalate=False,
                confidence=0.85,
            )

        if message_type == MessageType.BUG_REPORT:
            return ChatResponse(
                message=(
                    f"Thank you for reporting this issue with {product_name}. "
                    f"I've logged this as a bug report for our engineering team. "
                    f"Can you provide any additional details like error messages or steps to reproduce?"
                ),
                resolved=False,
                escalate=False,
                suggested_actions=["Create GitHub issue", "Request more details"],
                confidence=0.9,
            )

        if message_type == MessageType.FEATURE_REQUEST:
            return ChatResponse(
                message=(
                    f"Thanks for the feature suggestion for {product_name}! "
                    f"I've added this to our feedback board. Our product team reviews "
                    f"all suggestions regularly."
                ),
                resolved=True,
                escalate=False,
                suggested_actions=["Add to feature backlog"],
                confidence=0.95,
            )

        if message_type == MessageType.FEEDBACK:
            return ChatResponse(
                message=(
                    f"Thank you so much for your feedback about {product_name}! "
                    f"We really appreciate you taking the time to share this with us."
                ),
                resolved=True,
                escalate=False,
                confidence=0.95,
            )

        # Default response
        return ChatResponse(
            message=(
                f"Thanks for contacting {product_name} support! "
                f"I'm here to help. Could you tell me more about what you need?"
            ),
            resolved=False,
            escalate=False,
            confidence=0.7,
        )
