import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key = st.secrets["api_key"],
)

# function to call llm for dispute classification
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

def assign_priority(dispute_category):
    priority = {
        "Unauthorized Transaction": "High",  
        "Duplicate Transaction": "Medium",   
        "Amount Error": "Low",               
        "Product Not Received": "Medium"     
    }
    return priority.get(dispute_category, "Low") 

def is_high_risk(dispute_category, dispute_description):
    if dispute_category == "Unauthorized Transaction":
        return True
    if "large amount" in dispute_description.lower():
        return True
    return False

# recommended action based on dispute classification
def get_recommended_action(dispute_category, priority_level):
    actions = {
        "High": "Urgently investigate and reverse the transaction. Contact the customer directly to confirm the issue.",
        "Medium": "Review the dispute details and verify transaction data. Reach out to the customer if necessary.",
        "Low": "Check the details and provide the customer with a clear explanation or refund if appropriate."
    }
    return actions.get(priority_level, "Further review is required.")

# Streamlit app 
st.title("Banking Dispute Classification and Management")

st.header("Please enter the details of your dispute")

# Input field
dispute_description = st.text_area("Describe your dispute:", height=150)

# Submit button 
if st.button("Submit Dispute"):
    if dispute_description:
        dispute_category = classify_dispute(dispute_description)
        priority_level = assign_priority(dispute_category)
        high_risk_flag = is_high_risk(dispute_category, dispute_description)
        recommended_action = get_recommended_action(dispute_category, priority_level)

        # Display the results
        st.write(f"### Dispute Category: {dispute_category}")
        st.write(f"### Assigned Priority Level: {priority_level}")
        st.write(f"### High-Risk: {'Yes' if high_risk_flag else 'No'}")
        st.write(f"### Recommended Action: {recommended_action}")
    else:
        st.warning("Please enter the details of your dispute.")
