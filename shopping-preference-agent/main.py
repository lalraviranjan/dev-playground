import uuid

from bedrock_agentcore.runtime import BedrockAgentCoreApp

from strands import Agent
from strands.models import BedrockModel

from bedrock_agentcore.memory import MemoryClient

from strands_agents import (
    SYSTEM_PROMPT,
    MODEL_ID,
    search_products,
    get_product_details,
    compare_products,
)

from strands_memory import (
    CustomerSupportMemoryHooks,
    ACTOR_ID,
)

# =========================================================
# CONFIG
# =========================================================

REGION = "us-east-1"

MEMORY_ID = "CustomerSupportMemory-MX23P53VL1"

# =========================================================
# APP
# =========================================================

app = BedrockAgentCoreApp()

# =========================================================
# ENTRYPOINT
# =========================================================

@app.entrypoint
async def invoke(payload, context=None):

    try:

        print("\n=== INVOCATION STARTED ===")

        # =================================================
        # INPUT
        # =================================================

        user_prompt = payload.get("prompt", "")

        actor_id = payload.get(
            "actor_id",
            ACTOR_ID
        )

        session_id = payload.get(
            "session_id",
            str(uuid.uuid4())
        )

        print("Prompt:", user_prompt)

        # =================================================
        # MODEL
        # =================================================

        model = BedrockModel(
            model_id=MODEL_ID
        )

        # =================================================
        # MEMORY CLIENT
        # =================================================

        memory_client = MemoryClient(
            region_name=REGION
        )

        # =================================================
        # MEMORY HOOKS
        # =================================================

        memory_hooks = CustomerSupportMemoryHooks(
            memory_id=MEMORY_ID,
            client=memory_client,
            actor_id=actor_id,
            session_id=session_id,
        )

        # =================================================
        # AGENT
        # =================================================

        agent = Agent(
            model=model,
            system_prompt=SYSTEM_PROMPT,
            tools=[
                search_products,
                get_product_details,
                compare_products,
            ],
            hooks=[memory_hooks],
        )

        # =================================================
        # INVOKE
        # =================================================

        response = agent(user_prompt)

        print("=== RESPONSE GENERATED ===")

        return {
            "response": str(response),
            "session_id": session_id,
            "actor_id": actor_id,
        }

    except Exception as e:

        print("RUNTIME ERROR:", str(e))

        return {
            "error": str(e)
        }

# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    print("Starting AgentCore Runtime...")

    app.run()