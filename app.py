import streamlit as st
import openai
import json
from typing import Dict, Any

# Set page config
st.set_page_config(page_title="AI Form Filler", page_icon="📝", layout="wide")

# Initialize session state
if 'autofilled_data' not in st.session_state:
    st.session_state.autofilled_data = {}

def call_openai_api(prompt: str, form_type: str) -> Dict[str, Any]:
    """Call OpenAI API to generate form data based on natural language prompt"""
    
    # Define expected fields for each form type
    form_schemas = {
        "Customer Info": {
            "name": "string",
            "age": "number",
            "country": "string (select from common countries)",
            "is_active": "boolean"
        },
        "Product Feedback": {
            "product_name": "string",
            "rating": "number (1-5)",
            "comments": "string"
        },
        "Support Request": {
            "issue": "string",
            "severity": "string (Low, Medium, High, Critical)",
            "preferred_contact_time": "string"
        }
    }
    
    system_prompt = f"""You are an AI assistant that helps fill out forms based on natural language descriptions.
    
    Form Type: {form_type}
    Expected Fields: {json.dumps(form_schemas[form_type], indent=2)}
    
    Based on the user's description, extract relevant information and return it as a JSON object.
    Only include fields that can be reasonably inferred from the description.
    If a field cannot be determined, omit it from the response.
    
    For the country field, use full country names (e.g., "United States", "India", "United Kingdom").
    For severity, use one of: "Low", "Medium", "High", "Critical".
    For rating, use a number between 1-5.
    For is_active, use true/false boolean values.
    
    Return only valid JSON without any additional text or formatting."""
    
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return {}

def render_customer_info_form():
    """Render Customer Info form"""
    st.subheader("Customer Information Form")
    
    # Get autofilled data if available
    autofilled = st.session_state.autofilled_data.get("Customer Info", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name", value=autofilled.get("name", ""))
        age = st.number_input("Age", min_value=0, max_value=120, value=autofilled.get("age", 0))
    
    with col2:
        countries = ["", "United States", "India", "United Kingdom", "Canada", "Australia", "Germany", "France", "Japan", "Brazil", "Other"]
        country_value = autofilled.get("country", "")
        if country_value and country_value not in countries:
            countries.append(country_value)
        country = st.selectbox("Country", countries, index=countries.index(country_value) if country_value in countries else 0)
        
        is_active = st.checkbox("Is Active Customer", value=autofilled.get("is_active", False))
    
    if st.button("Submit Customer Info", type="primary"):
        if name and age > 0 and country:
            st.success("Customer information submitted successfully!")
            st.json({
                "name": name,
                "age": age,
                "country": country,
                "is_active": is_active
            })
        else:
            st.error("Please fill in all required fields.")

def render_product_feedback_form():
    """Render Product Feedback form"""
    st.subheader("Product Feedback Form")
    
    # Get autofilled data if available
    autofilled = st.session_state.autofilled_data.get("Product Feedback", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("Product Name", value=autofilled.get("product_name", ""))
        rating = st.slider("Rating", min_value=1, max_value=5, value=autofilled.get("rating", 3))
    
    with col2:
        comments = st.text_area("Comments", value=autofilled.get("comments", ""), height=100)
    
    if st.button("Submit Product Feedback", type="primary"):
        if product_name and comments:
            st.success("Product feedback submitted successfully!")
            st.json({
                "product_name": product_name,
                "rating": rating,
                "comments": comments
            })
        else:
            st.error("Please fill in all required fields.")

def render_support_request_form():
    """Render Support Request form"""
    st.subheader("Support Request Form")
    
    # Get autofilled data if available
    autofilled = st.session_state.autofilled_data.get("Support Request", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        issue = st.text_input("Issue Description", value=autofilled.get("issue", ""))
        severity_options = ["Low", "Medium", "High", "Critical"]
        severity_value = autofilled.get("severity", "Medium")
        if severity_value not in severity_options:
            severity_value = "Medium"
        severity = st.selectbox("Severity", severity_options, index=severity_options.index(severity_value))
    
    with col2:
        preferred_contact_time = st.text_input("Preferred Contact Time", value=autofilled.get("preferred_contact_time", ""))
    
    if st.button("Submit Support Request", type="primary"):
        if issue and preferred_contact_time:
            st.success("Support request submitted successfully!")
            st.json({
                "issue": issue,
                "severity": severity,
                "preferred_contact_time": preferred_contact_time
            })
        else:
            st.error("Please fill in all required fields.")

def main():
    """Main Streamlit app"""
    st.title("🤖 AI-Powered Form Filler")
    st.markdown("Fill out forms automatically using natural language descriptions!")
    
    # Form selection
    form_options = ["Customer Info", "Product Feedback", "Support Request"]
    selected_form = st.selectbox("Select Form Type", form_options)
    
    # Auto-fill section
    st.markdown("---")
    st.subheader("Auto-fill using AI")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        prompt = st.text_area(
            "Describe the information in natural language:",
            placeholder="e.g., A 30-year-old customer from India interested in premium support",
            height=100
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        if st.button("🤖 Auto-fill using GPT", type="secondary"):
            if prompt:
                with st.spinner("Generating form data..."):
                    result = call_openai_api(prompt, selected_form)
                    if result:
                        st.session_state.autofilled_data[selected_form] = result
                        st.success("Form data generated successfully!")
                        st.json(result)
                    else:
                        st.error("Failed to generate form data. Please try again.")
            else:
                st.error("Please enter a description first.")
    
    # Display selected form
    st.markdown("---")
    
    if selected_form == "Customer Info":
        render_customer_info_form()
    elif selected_form == "Product Feedback":
        render_product_feedback_form()
    elif selected_form == "Support Request":
        render_support_request_form()

if __name__ == "__main__":
    main() 