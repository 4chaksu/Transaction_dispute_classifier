import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key = st.secrets["api_key"],
)

# Define function to call OpenAI GPT model for dispute classification
def classify_dispute(dispute_description):
    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Classify the following customer dispute into one of these categories: Unauthorized Transaction, Duplicate Transaction, Amount Error, Product Not Received."
        },
        {
            "role": "user",
            "content": f"Dispute: {dispute_description}\n\nCategory:"
        }
    ],
    model="gpt-4o-mini",
    temperature=1,
    max_tokens=4096,
    top_p=1
)

    return response.choices[0].message.content

# Define function to assign a priority level based on the dispute category
def assign_priority(dispute_category):
    # Assign high, medium, low priority based on the dispute type
    priority = {
        "Unauthorized Transaction": "High",  # High priority for security issues
        "Duplicate Transaction": "Medium",   # Medium priority for account errors
        "Amount Error": "Low",               # Low priority for pricing errors
        "Product Not Received": "Medium"     # Medium priority for non-receipt issues
    }
    return priority.get(dispute_category, "Low")  # Default to low priority if category is unknown

# Define function to flag high-risk disputes
def is_high_risk(dispute_category, dispute_description):
    # High-risk is typically flagged for unauthorized transactions or large amounts
    if dispute_category == "Unauthorized Transaction":
        return True
    if "large amount" in dispute_description.lower():
        return True
    return False

# Define function to return recommended action based on dispute classification
def get_recommended_action(dispute_category, priority_level):
    # Depending on the dispute type and priority level, suggest actions
    actions = {
        "High": "Urgently investigate and reverse the transaction. Contact the customer directly to confirm the issue.",
        "Medium": "Review the dispute details and verify transaction data. Reach out to the customer if necessary.",
        "Low": "Check the details and provide the customer with a clear explanation or refund if appropriate."
    }
    return actions.get(priority_level, "Further review is required.")

# Streamlit app layout
st.title("Banking Dispute Classification and Management")

st.header("Please enter the details of your dispute")

# Input field for user to describe the dispute
dispute_description = st.text_area("Describe your dispute:", height=150)

# Submit button to process the dispute
if st.button("Submit Dispute"):
    if dispute_description:
        # Step 1: Classify the dispute using AI (GPT model)
        dispute_category = classify_dispute(dispute_description)

        # Step 2: Assign a priority level based on the category
        priority_level = assign_priority(dispute_category)

        # Step 3: Flag high-risk disputes
        high_risk_flag = is_high_risk(dispute_category, dispute_description)

        # Step 4: Return the recommended action based on dispute classification and priority level
        recommended_action = get_recommended_action(dispute_category, priority_level)

        # Display the results
        st.write(f"### Dispute Category: {dispute_category}")
        st.write(f"### Assigned Priority Level: {priority_level}")
        st.write(f"### High-Risk: {'Yes' if high_risk_flag else 'No'}")
        st.write(f"### Recommended Action: {recommended_action}")
    else:
        st.warning("Please enter the details of your dispute.")
