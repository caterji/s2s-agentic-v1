import json
from utils.llm_utils import call_llm

def generate_insight_with_llm(customer_profile):
    prompt = f"""
You are InsightAgent, a vehicle insight expert helping personalize upgrade offers.
Your job is to find 1 key insight (hook) based on the customer's profile, especially focusing on vehicle usage, service gaps, and engagement.

Here is the customer's profile in JSON:
{json.dumps(customer_profile, indent=2)}

Output a JSON response with:
- "insight": a short one-line insight
- "insight_type": one of ["usage_trigger", "upgrade_history", "loyalty_hook", "eco_hook", "default"]

The insight must be relevant and usable as a conversation starter for a service-to-sales offer.
Only output the JSON.
"""
    response = call_llm(prompt, backend='openai')

    try:
        parsed = json.loads(response.strip().split("```json")[-1].replace("```", "").strip()) if "```json" in response else json.loads(response)
        return parsed
    except json.JSONDecodeError:
        return {"insight": "LLM output error", "insight_type": "default", "raw_output": response}