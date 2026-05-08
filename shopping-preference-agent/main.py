import uuid
import boto3

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
# AWS / Bedrock Setup
# =========================================================

# Detect current AWS region
REGION = boto3.session.Session().region_name

# Initialize Bedrock model
model = BedrockModel(
    model_id=MODEL_ID,
)

# =========================================================
# MEMORY SETUP
# =========================================================

# Hardcoded memory ID (for now)
MEMORY_ID = "CustomerSupportMemory-MX23P53VL1"

# Create unique session ID for current terminal session
SESSION_ID = str(uuid.uuid4())

# Initialize memory client
memory_client = MemoryClient(region_name=REGION)

# Initialize memory hooks
memory_hooks = CustomerSupportMemoryHooks(
    memory_id=MEMORY_ID,
    client=memory_client,
    actor_id=ACTOR_ID,
    session_id=SESSION_ID,
)

# =========================================================
# CREATE AGENT
# =========================================================

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

# =========================================================
# TERMINAL CHAT LOOP
# =========================================================

print("\n🛍️ Shopping Preference Agent Started")
print("Type 'exit' to quit.\n")

while True:

    # Take terminal input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() in ["exit", "quit"]:
        print("\n👋 Exiting Shopping Agent...")
        break

    try:
        # Invoke agent
        response = agent(user_input)

        # Print response
        print(f"\nAssistant: {response}\n")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")