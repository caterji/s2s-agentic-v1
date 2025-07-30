import streamlit as st
st.write("Streamlit is working!")

import sys
import os
import json

# Add project root to path for Streamlit Cloud compatibility
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Import all required modules
from utils.customer_helper import load_all_customers
from agents.prospect_agent import evaluate_prospect_with_llm
from agents.insight_agent import generate_insight_with_llm
from agents.finance_agent import generate_finance_offer_with_llm
from agents.script_agent import generate_initial_script
from agents.engagement_agent import generate_engagement_followups
from utils.llm_utils import call_llm

# Descriptions of each agent’s objective
AGENT_DESCRIPTIONS = {
    "ProspectAgent": "(Qualifies the customer for upgrade pitches)",
    "InsightAgent": "(Identifies key usage or service-based hook)",
    "FinanceAgent": "(Suggests relevant offers based on budget, loyalty)",
    "ScriptAgent": "(Orchestrates the final sales message using Prospect, Insight, and Finance agents)",
    "EngageAgent": "(Creates SMS/email/WhatsApp follow-up messages)"
}

# Load customer data
customers = load_all_customers()
customer_names = [f"{c['customer_id']} - {c['first_name']}" for c in customers]
selected = st.selectbox("Select a customer", customer_names)

if selected:
    customer_id = selected.split(" - ")[0]
    customer = next(c for c in customers if c['customer_id'] == customer_id)
    st.session_state['customer'] = customer

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("👤 Customer Profile")
        st.image(f"images/{customer['customer_image']}", width=150, caption="Customer Photo")
        st.image(f"images/{customer['vehicle_image']}", width=150, caption="Vehicle Photo")
        st.markdown(f"**Name:** {customer['first_name']}")
        st.markdown(f"**Location:** {customer['location']}")
        st.markdown(f"**Vehicle:** {customer['vehicle']['model']} ({customer['vehicle']['year']})")
        st.markdown(f"**Mileage:** {customer['vehicle']['current_mileage']} mi")
        st.markdown(f"**Loyalty:** {customer['financial_profile']['loyalty_status']}")
        st.markdown(f"**Tone Preference:** {customer['contact_preferences']['tone_preference']}")

    with col2:
        st.subheader("🧠 ScriptAgent Sales Copilot")

        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        if st.button("🎯 Generate Initial Sales Script"):
            with st.spinner("Running agents..."):
                prospect = evaluate_prospect_with_llm(customer)
                insight = generate_insight_with_llm(customer)
                finance = generate_finance_offer_with_llm(customer)
                script_response = generate_initial_script(customer['customer_id'])

            st.session_state['chat_history'].append({
                "role": "assistant",
                "text": script_response["script"],
                "log": {
                    "ProspectAgent": prospect,
                    "InsightAgent": insight,
                    "FinanceAgent": finance,
                    "ScriptAgent": {
                        "role": "Orchestrator",
                        "objective": "Composes the final sales message by synthesizing insights from ProspectAgent, InsightAgent, and FinanceAgent.",
                        "used_agents": ["ProspectAgent", "InsightAgent", "FinanceAgent"],
                        "response_style": f"Tuned to customer's tone preference ({customer['contact_preferences']['tone_preference']})",
                        "script_output": script_response["script"]
                    }
                }
            })

        st.markdown("### 💬 Conversation Thread")
        for chat in st.session_state['chat_history']:
            if chat['role'] == 'user':
                st.markdown(f"**🧑 Consultant:** {chat['text']}")
            else:
                st.markdown(f"**🤖 ScriptAgent:** {chat['text']}")
                with st.expander("🧩 Agent Log"):
                    for agent, output in chat['log'].items():
                        desc = AGENT_DESCRIPTIONS.get(agent, "")
                        st.markdown(f"**{agent}** {desc}")
                        st.json(output)

        user_input = st.text_input("Type customer reply or internal note...", key="input")

        if st.button("🔁 Generate Follow-up"):
            if user_input:
                st.session_state['chat_history'].append({
                    "role": "user",
                    "text": user_input
                })

                previous_script = [msg for msg in reversed(st.session_state['chat_history']) if msg['role'] == 'assistant'][0]["text"]

                followup_prompt = f"""You are ScriptAgent continuing a conversation with a customer.

The last assistant message was:
\"{previous_script}\"

The sales consultant replied:
\"{user_input}\"

Use the customer profile below to generate a persuasive follow-up message:

Customer profile:
{json.dumps(customer, indent=2)}

Respond only with the reply string.
"""
                response = call_llm(followup_prompt, backend='openai')
                script_text = response.strip()

                st.session_state['chat_history'].append({
                    "role": "assistant",
                    "text": script_text,
                    "log": {
                        "ScriptAgent": {
                            "contextual_followup": True,
                            "based_on": previous_script,
                            "reaction_to": user_input,
                            "response_style": f"Tuned to {customer['contact_preferences']['tone_preference']} tone"
                        }
                    }
                })

        # ---------- ENGAGEMENT PANEL ----------
        st.markdown("---")
        st.subheader("📩 Follow-up Engagement Panel")

        if st.button("📬 Generate Engagement Messages"):
            last_script = [msg for msg in reversed(st.session_state['chat_history']) if msg['role'] == 'assistant'][0]["text"]
            engagement = generate_engagement_followups(customer, last_script)

            st.session_state['engagement_messages'] = engagement

        if 'engagement_messages' in st.session_state:
            for channel in ['sms', 'email', 'whatsapp']:
                st.markdown(f"**{channel.upper()} Preview:**")
                st.code(st.session_state['engagement_messages'][channel], language="text")
                if st.button(f"✅ Send {channel.upper()}"):
                    st.success(f"{channel.upper()} sent!")