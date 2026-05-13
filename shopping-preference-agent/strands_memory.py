#!/usr/bin/python

import logging
import uuid

from bedrock_agentcore.memory import MemoryClient

from strands.hooks import (
    AfterInvocationEvent,
    HookProvider,
    HookRegistry,
    MessageAddedEvent,
)

# =========================================================
# CONFIG
# =========================================================

REGION = "us-east-1"

logger = logging.getLogger(__name__)

ACTOR_ID = "customer_001"

SESSION_ID = str(uuid.uuid4())

# =========================================================
# MEMORY HOOKS
# =========================================================

class CustomerSupportMemoryHooks(HookProvider):

    def __init__(
        self,
        memory_id: str,
        client: MemoryClient,
        actor_id: str,
        session_id: str,
    ):

        self.memory_id = memory_id
        self.client = client
        self.actor_id = actor_id
        self.session_id = session_id

        # LAZY LOAD
        self.namespaces = None

    # =====================================================
    # LAZY LOAD MEMORY STRATEGIES
    # =====================================================

    def load_namespaces(self):

        if self.namespaces is None:

            print("Loading memory namespaces...")

            strategies = self.client.get_memory_strategies(
                self.memory_id
            )

            self.namespaces = {
                i["type"]: i["namespaces"][0]
                for i in strategies
            }

    # =====================================================
    # RETRIEVE MEMORY
    # =====================================================

    def retrieve_customer_context(self, event: MessageAddedEvent):

        try:

            self.load_namespaces()

            messages = event.agent.messages

            if (
                messages[-1]["role"] == "user"
                and "toolResult" not in messages[-1]["content"][0]
            ):

                user_query = messages[-1]["content"][0]["text"]

                all_context = []

                for context_type, namespace in self.namespaces.items():

                    memories = self.client.retrieve_memories(
                        memory_id=self.memory_id,
                        namespace=namespace.format(
                            actorId=self.actor_id
                        ),
                        query=user_query,
                        top_k=3,
                    )

                    for memory in memories:

                        if isinstance(memory, dict):

                            content = memory.get("content", {})

                            if isinstance(content, dict):

                                text = content.get(
                                    "text",
                                    ""
                                ).strip()

                                if text:

                                    all_context.append(
                                        f"[{context_type.upper()}] {text}"
                                    )

                # Inject memory context
                if all_context:

                    context_text = "\n".join(all_context)

                    original_text = messages[-1]["content"][0]["text"]

                    messages[-1]["content"][0]["text"] = (
                        f"Customer Context:\n"
                        f"{context_text}\n\n"
                        f"{original_text}"
                    )

        except Exception as e:

            logger.error(
                f"Failed retrieving memory: {e}"
            )

    # =====================================================
    # SAVE MEMORY
    # =====================================================

    def save_support_interaction(
        self,
        event: AfterInvocationEvent
    ):

        try:

            messages = event.agent.messages

            if (
                len(messages) >= 2
                and messages[-1]["role"] == "assistant"
            ):

                customer_query = None
                agent_response = None

                for msg in reversed(messages):

                    if (
                        msg["role"] == "assistant"
                        and not agent_response
                    ):

                        agent_response = msg["content"][0]["text"]

                    elif (
                        msg["role"] == "user"
                        and not customer_query
                        and "toolResult" not in msg["content"][0]
                    ):

                        customer_query = msg["content"][0]["text"]

                        break

                if customer_query and agent_response:

                    self.client.create_event(
                        memory_id=self.memory_id,
                        actor_id=self.actor_id,
                        session_id=self.session_id,
                        messages=[
                            (customer_query, "USER"),
                            (agent_response, "ASSISTANT"),
                        ],
                    )

                    print("Memory saved successfully")

        except Exception as e:

            logger.error(
                f"Failed saving memory: {e}"
            )

    # =====================================================
    # REGISTER HOOKS
    # =====================================================

    def register_hooks(self, registry: HookRegistry):

        registry.add_callback(
            MessageAddedEvent,
            self.retrieve_customer_context
        )

        registry.add_callback(
            AfterInvocationEvent,
            self.save_support_interaction
        )