import json
import os

# File path (assuming customer_data.json is in the root folder)
DATA_FILE = os.path.join(os.path.dirname(__file__), '../customer_data.json')

def load_all_customers():
    """Returns the full list of customer profiles."""
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def get_customer_by_id(customer_id):
    """Returns a single customer profile by ID."""
    customers = load_all_customers()
    for customer in customers:
        if customer['customer_id'] == customer_id:
            return customer
    return None