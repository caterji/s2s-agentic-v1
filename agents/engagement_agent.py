
import json
from utils.llm_utils import call_llm

def generate_engagement_followups(customer_profile, last_script):
    prompt = f"""You are EngageAgent, responsible for creating follow-up messages (SMS, Email, WhatsApp) 
based on the last interaction between a sales consultant and a customer.

Use the customer's tone preference, contact channel, and loyalty status.

Here is the customer profile:
{json.dumps(customer_profile, indent=2)}

Here is the last message from ScriptAgent:
"{last_script}"

Respond in JSON format with the following keys:
- "sms": a short SMS message under 160 characters
- "email": a polite email follow-up message (2–3 lines)
- "whatsapp": a conversational WhatsApp message (1–2 lines)
"""

    response = call_llm(prompt, backend='openai')

    try:
        parsed = json.loads(response.strip().split("```json")[-1].replace("```", "").strip()) if "```json" in response else json.loads(response)
        return parsed
    except json.JSONDecodeError:
        return {
            "sms": "LLM could not parse SMS response.",
            "email": "LLM could not parse Email response.",
            "whatsapp": "LLM could not parse WhatsApp response.",
            "raw_output": response
        }
