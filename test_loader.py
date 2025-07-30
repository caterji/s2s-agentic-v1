import json
from utils.customer_helper import get_customer_by_id
from agents.prospect_agent import evaluate_prospect_with_llm
from agents.insight_agent import generate_insight_with_llm
from agents.finance_agent import generate_finance_offer_with_llm
from agents.script_agent import generate_initial_script

# Load Jason (C001)
customer = get_customer_by_id("C003")

# Run agents
prospect = evaluate_prospect_with_llm(customer)
insight = generate_insight_with_llm(customer)
finance = generate_finance_offer_with_llm(customer)

# Generate script
script = generate_initial_script(customer['customer_id'])

# Print everything
print("=" * 60)
print("SCRIPT AGENT RESPONSE")
print(json.dumps(script, indent=2))
print("=" * 60)