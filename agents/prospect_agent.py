import json
from utils.llm_utils import call_llm

def evaluate_prospect_with_llm(customer_profile):
    prompt = f"""
You are ProspectAgent, a qualification agent for service-to-sales conversion.
Your job is to assess whether a customer is a good candidate for an upgrade pitch based on their vehicle, usage, and engagement history.

Here is the customer's profile in JSON format:
{json.dumps(customer_profile, indent=2)}

Based on this, respond with a valid JSON object containing:
- "is_qualified": true or false
- "reasons": a list of 2–3 short bullet points that explain your judgment

Be concise and professional. Avoid fluff.
Only output the JSON response.
    """

    response = call_llm(prompt, backend='openai')

    try:
        # Try to extract JSON from response
        parsed = json.loads(response.strip().split("```json")[-1].replace("```", "").strip()) if "```json" in response else json.loads(response)
        return parsed
    except json.JSONDecodeError:
        return {"is_qualified": False, "reasons": ["LLM response could not be parsed. Raw output:", response]}