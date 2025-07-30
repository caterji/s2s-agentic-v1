import json
from utils.llm_utils import call_llm

def generate_finance_offer_with_llm(customer_profile):
    prompt = f"""
You are FinanceAgent, responsible for suggesting a relevant upgrade package offer for an automotive customer.

Your job is to recommend:
- a suitable offer based on their budget bracket and loyalty level,
- an estimated price range,
- and any available loyalty benefits.

Here is the customer's profile in JSON:
{json.dumps(customer_profile, indent=2)}

Respond ONLY with a JSON object like:
- "suggested_offer": short name of the package (e.g. "Power Upgrade Bundle")
- "price_range": e.g. "$299–$399"
- "loyalty_discount": true/false
- "financial_context": a short sentence explaining why this offer makes sense

Only output the JSON.
"""
    response = call_llm(prompt, backend='openai')

    try:
        parsed = json.loads(response.strip().split("```json")[-1].replace("```", "").strip()) if "```json" in response else json.loads(response)
        return parsed
    except json.JSONDecodeError:
        return {
            "suggested_offer": "N/A",
            "price_range": "N/A",
            "loyalty_discount": False,
            "financial_context": "LLM output error",
            "raw_output": response
        }