import json
from agents.prospect_agent import evaluate_prospect_with_llm
from agents.insight_agent import generate_insight_with_llm
from agents.finance_agent import generate_finance_offer_with_llm
from utils.customer_helper import get_customer_by_id
from utils.llm_utils import call_llm


def generate_initial_script(customer_id):
    customer = get_customer_by_id(customer_id)

    # Run sub-agents
    prospect_result = evaluate_prospect_with_llm(customer)
    insight_result = generate_insight_with_llm(customer)
    finance_result = generate_finance_offer_with_llm(customer)

    # Construct agent log
    agent_log = [
        {
            "agent": "ProspectAgent",
            "objective": "Evaluate if this customer is a qualified upgrade prospect based on profile.",
            "output": prospect_result
        },
        {
            "agent": "InsightAgent",
            "objective": "Identify the right sales hook or entry point based on behavior or attributes.",
            "output": insight_result
        },
        {
            "agent": "FinanceAgent",
            "objective": "Recommend relevant upgrade plans/offers based on customer's financing preference.",
            "output": finance_result
        }
    ]

    # Compose the LLM prompt
    system_prompt = f"""
You are ScriptAgent, an expert assistant for car sales consultants.

You will now compose a personalized sales script based on:
- Customer Profile
- Prospect evaluation
- Sales Insight
- Financing Recommendation

Be friendly, concise, and value-oriented. Mention any special offers or upgrade paths if relevant.
Avoid sounding robotic or overly pushy. Write in a tone that builds trust.

### Customer Profile
{json.dumps(customer, indent=2)}

### Prospect Evaluation
{json.dumps(prospect_result, indent=2)}

### Insight
{json.dumps(insight_result, indent=2)}

### Finance Recommendation
{json.dumps(finance_result, indent=2)}

Respond with only the final script message the consultant will say to the customer.
Guidelines:
- Keep the tone aligned with the customer's tone preference (e.g., empathetic, professional, enthusiastic).
- Be clear, concise, and purpose-driven — avoid repeating generic benefits or over-explaining features.
- Mention upgrade packages or recommendations based on the customer’s profile.
- If pricing is included, show a specific price range clearly.
- Always aim to generate curiosity and prompt further discussion.
- Limit response to **1–2 crisp paragraphs**, max 150–180 words.

"""

    script_response = call_llm(system_prompt, backend='openai')

    # Add ScriptAgent to the agent log
    agent_log.append({
        "agent": "ScriptAgent",
        "objective": "Combine all agent outputs to generate a natural, persuasive sales message.",
        "output": script_response
    })

    return {
        "script": script_response,
        "agent_log": agent_log
    }


def generate_followup_script(customer, user_input):
    # 👇 New concise follow-up prompt
    followup_prompt = f"""
You are ScriptAgent, continuing a conversation with a customer who just asked a follow-up question.
The customer is considering an upgrade and just said:
"{user_input}"

Below is the customer profile:
{json.dumps(customer, indent=2)}

Respond concisely and directly, using the customer's profile, tone preference, and past conversation context.

Guidelines:
- Avoid repeating what’s already been said in the initial script.
- Focus only on the follow-up question asked.
- Keep the tone natural and friendly.
- Use simple, benefit-oriented language.
- Stay within 100–120 words.

"""

    followup_response = call_llm(followup_prompt, backend='openai')

    return {
        "followup_message": followup_response
    }