import uuid
import re
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel
from bedrock_agentcore.memory import MemoryClient
from strands_memory import create_session_manager

from strands_agents import (
    SYSTEM_PROMPT,
    MODEL_ID,
    search_products,
    get_product_details,
    compare_products,
)

# from strands_memory import (
#     CustomerSupportMemoryHooks,
#     ACTOR_ID,
# )

# =========================================================
# CONFIG
# =========================================================

REGION = "us-east-1"
MEMORY_ID = "CustomerSupportMemory-l258dZFBS4"
# SESSION_ID = str(uuid.uuid4())

def _sanitize(value: str) -> str:
    """
    AgentCore Memory only allows [A-Za-z0-9_-]
    """

    cleaned = re.sub(
        r"[^A-Za-z0-9_-]",
        "-",
        str(value)
    ).strip("-")

    return cleaned or "anonymous"

# =========================================================
# APP
# =========================================================

app = BedrockAgentCoreApp()

# =========================================================
# ENTRYPOINT
# =========================================================

@app.entrypoint
def invoke(payload: dict, context) -> dict:

    try:

        print("\n=== INVOCATION STARTED ===")

        # =================================================
        # INPUT
        # =================================================

        user_prompt = payload.get("prompt", "")

        actor_id = _sanitize(
            payload.get("actor_id") or "anonymous"
        )
        
        session_id = _sanitize(
            payload.get("session_id")
            or getattr(context, "session_id", None)
            or f"{actor_id}-{uuid.uuid4()}"
        )

        print("Prompt:", user_prompt)

        # =================================================
        # MODEL
        # =================================================

        model = BedrockModel(
            model_id=MODEL_ID,
            region_name=REGION
        )

        # =================================================
        # MEMORY CLIENT
        # =================================================

        # memory_client = MemoryClient(
        #     region_name=REGION
        # )

        # =================================================
        # MEMORY HOOKS
        # =================================================

        # memory_hooks = CustomerSupportMemoryHooks(
        #     memory_id=MEMORY_ID,
        #     client=memory_client,
        #     actor_id=actor_id,
        #     session_id=session_id,
        # )
        
        # =================================================
        # Session manager
        # =================================================
        
        session_manager = create_session_manager(
            memory_id=MEMORY_ID,
            actor_id=actor_id,
            session_id=session_id,
            region=REGION
        )

        # =================================================
        # AGENT
        # =================================================

        agent = Agent(
            model=model,
            session_manager= session_manager,
            system_prompt=SYSTEM_PROMPT,
            tools=[
                search_products,
                get_product_details,
                compare_products,
            ],
            # hooks=[memory_hooks],
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