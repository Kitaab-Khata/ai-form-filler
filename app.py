import streamlit as st
import openai
import json
import os
from datetime import datetime, date, time
from typing import Dict, Any, List

# Set page config
st.set_page_config(
    page_title="Credit Card Program Setup", 
    page_icon="💳", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
def init_session_state():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    if 'unsupported_fields' not in st.session_state:
        st.session_state.unsupported_fields = []
    
    if 'ai_processed' not in st.session_state:
        st.session_state.ai_processed = False

# Define field schemas for all pages
FIELD_SCHEMAS = {
    "page_1": {
        "program_name": {"type": "text", "label": "Program Name"},
        "program_code": {"type": "text", "label": "Program Code"},
        "launch_date": {"type": "date", "label": "Launch Date"},
        "program_budget": {"type": "number", "label": "Program Budget ($)"},
        "program_status": {"type": "select", "label": "Program Status", "options": ["Draft", "Active", "Inactive", "Suspended"]},
        "target_audience": {"type": "multiselect", "label": "Target Audience", "options": ["New Customers", "Existing Customers", "Premium Customers", "Corporate Clients"]},
        "program_duration": {"type": "slider", "label": "Program Duration (months)", "min": 1, "max": 24},
        "auto_renewal": {"type": "checkbox", "label": "Auto Renewal Enabled"},
        "launch_time": {"type": "time", "label": "Launch Time"},
        "program_description": {"type": "textarea", "label": "Program Description"}
    },
    "page_2": {
        "product_type": {"type": "radio", "label": "Product Type", "options": ["Standard Card", "Gold Card", "Platinum Card", "Business Card"]},
        "annual_fee": {"type": "number", "label": "Annual Fee ($)"},
        "credit_limit": {"type": "select", "label": "Credit Limit", "options": ["$1,000", "$5,000", "$10,000", "$25,000", "$50,000", "Unlimited"]},
        "interest_rate": {"type": "slider", "label": "Interest Rate (%)", "min": 0.0, "max": 30.0, "step": 0.1},
        "rewards_program": {"type": "multiselect", "label": "Rewards Program", "options": ["Cash Back", "Points", "Miles", "Discounts"]},
        "card_features": {"type": "multiselect", "label": "Card Features", "options": ["Contactless", "Chip & PIN", "Mobile Wallet", "Travel Insurance", "Purchase Protection"]},
        "activation_required": {"type": "checkbox", "label": "Activation Required"},
        "card_design": {"type": "text", "label": "Card Design Theme"},
        "welcome_bonus": {"type": "number", "label": "Welcome Bonus ($)"},
        "product_notes": {"type": "textarea", "label": "Product Notes"}
    },
    "page_3": {
        "min_age": {"type": "number", "label": "Minimum Age"},
        "max_age": {"type": "number", "label": "Maximum Age"},
        "min_income": {"type": "number", "label": "Minimum Income ($)"},
        "credit_score_requirement": {"type": "select", "label": "Credit Score Requirement", "options": ["Poor (300-579)", "Fair (580-669)", "Good (670-739)", "Very Good (740-799)", "Excellent (800-850)"]},
        "employment_status": {"type": "multiselect", "label": "Employment Status", "options": ["Full-time", "Part-time", "Self-employed", "Retired", "Student"]},
        "residence_requirement": {"type": "radio", "label": "Residence Requirement", "options": ["US Citizen", "US Resident", "International"]},
        "debt_to_income_ratio": {"type": "slider", "label": "Max Debt-to-Income Ratio (%)", "min": 0, "max": 100},
        "bankruptcy_allowed": {"type": "checkbox", "label": "Allow Previous Bankruptcy"},
        "review_time": {"type": "time", "label": "Application Review Time"},
        "eligibility_notes": {"type": "textarea", "label": "Eligibility Notes"}
    }
}

# Get OpenAI API key
def get_openai_key():
    try:
        return st.secrets["OPENAI_API_KEY"]
    except:
        return os.getenv("OPENAI_API_KEY")

def call_openai_api(prompt: str) -> Dict[str, Any]:
    """Call OpenAI API to extract field values from natural language prompt"""
    
    # Create field mapping for AI understanding
    all_fields = {}
    for page_fields in FIELD_SCHEMAS.values():
        all_fields.update(page_fields)
    
    field_descriptions = {}
    for field_name, field_info in all_fields.items():
        field_descriptions[field_name] = {
            "type": field_info["type"],
            "label": field_info["label"]
        }
        if "options" in field_info:
            field_descriptions[field_name]["options"] = field_info["options"]
    
    system_prompt = f"""You are an AI assistant that extracts credit card program information from natural language descriptions.

Available fields and their types:
{json.dumps(field_descriptions, indent=2)}

Based on the user's prompt, extract relevant information and return it as a JSON object.
- Only include fields that can be reasonably inferred from the prompt
- For date fields, use YYYY-MM-DD format
- For time fields, use HH:MM:SS format
- For select/radio fields, use exact option values from the available options
- For multiselect fields, return arrays of option values
- For boolean fields (checkbox), use true/false
- If a field is mentioned but not supported, include it in a special "unsupported_fields" array

Return the response in this format:
{{
  "supported_fields": {{
    "field_name": "value",
    ...
  }},
  "unsupported_fields": ["field1", "field2", ...]
}}

Only return valid JSON without any additional text."""

    try:
        api_key = get_openai_key()
        if not api_key:
            st.error("OpenAI API key not found. Please configure it in secrets.toml")
            return {"supported_fields": {}, "unsupported_fields": []}
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return {"supported_fields": {}, "unsupported_fields": []}

def render_field(field_name: str, field_info: Dict, current_value: Any = None):
    """Render a form field based on its type"""
    
    field_type = field_info["type"]
    label = field_info["label"]
    
    if field_type == "text":
        return st.text_input(label, value=current_value or "")
    
    elif field_type == "number":
        return st.number_input(label, value=current_value or 0)
    
    elif field_type == "date":
        if current_value and isinstance(current_value, str):
            try:
                current_value = datetime.strptime(current_value, "%Y-%m-%d").date()
            except:
                current_value = date.today()
        return st.date_input(label, value=current_value or date.today())
    
    elif field_type == "time":
        if current_value and isinstance(current_value, str):
            try:
                current_value = datetime.strptime(current_value, "%H:%M:%S").time()
            except:
                current_value = time(9, 0)
        return st.time_input(label, value=current_value or time(9, 0))
    
    elif field_type == "select":
        options = field_info["options"]
        index = 0
        if current_value and current_value in options:
            index = options.index(current_value)
        return st.selectbox(label, options, index=index)
    
    elif field_type == "multiselect":
        options = field_info["options"]
        default = current_value if current_value else []
        return st.multiselect(label, options, default=default)
    
    elif field_type == "checkbox":
        return st.checkbox(label, value=current_value or False)
    
    elif field_type == "radio":
        options = field_info["options"]
        index = 0
        if current_value and current_value in options:
            index = options.index(current_value)
        return st.radio(label, options, index=index)
    
    elif field_type == "textarea":
        return st.text_area(label, value=current_value or "", height=100)
    
    elif field_type == "slider":
        min_val = field_info.get("min", 0)
        max_val = field_info.get("max", 100)
        step = field_info.get("step", 1)
        
        # Handle current_value type conversion
        if current_value is None:
            safe_value = min_val
        elif isinstance(current_value, list):
            # Convert list to tuple for range slider or take first element for regular slider
            if len(current_value) > 1:
                # Range slider - convert to tuple
                safe_value = tuple(current_value[:2])
            elif len(current_value) > 0 and isinstance(current_value[0], (int, float)):
                # Single value - take first element
                safe_value = current_value[0]
            else:
                safe_value = min_val
        elif isinstance(current_value, (int, float)):
            safe_value = current_value
        else:
            # Try to convert string to number
            try:
                safe_value = float(current_value)
            except (ValueError, TypeError):
                safe_value = min_val
        
        # Determine if we should use int or float based on whether any value contains decimal
        use_float = (isinstance(min_val, float) or isinstance(max_val, float) or 
                    isinstance(step, float) or isinstance(safe_value, float) or
                    (isinstance(safe_value, tuple) and any(isinstance(x, float) for x in safe_value)))
        
        # Cast all values to the same type
        if use_float:
            min_val = float(min_val)
            max_val = float(max_val)
            step = float(step)
            if isinstance(safe_value, tuple):
                safe_value = tuple(float(x) for x in safe_value)
            else:
                safe_value = float(safe_value)
        else:
            min_val = int(min_val)
            max_val = int(max_val)
            step = int(step)
            if isinstance(safe_value, tuple):
                safe_value = tuple(int(x) for x in safe_value)
            else:
                safe_value = int(safe_value)
        
        # Ensure safe_value is within bounds
        if isinstance(safe_value, tuple):
            safe_value = tuple(max(min_val, min(max_val, x)) for x in safe_value)
        else:
            safe_value = max(min_val, min(max_val, safe_value))
        
        return st.slider(label, min_value=min_val, max_value=max_val, value=safe_value, step=step)
    
    else:
        return st.text_input(label, value=current_value or "")

def page_1_basic_details():
    """Page 1: Basic Program Details"""
    st.header("📋 Basic Program Details")
    
    # AI Prompt Section
    st.subheader("🤖 AI-Powered Setup")
    st.write("Use AI to auto-fill form fields")
    
    ai_prompt = st.text_area(
        "Describe your credit card program setup:",
        placeholder="Example: Create a new Gold Card program ABC123, launch on Aug 1, 2025, with $50 annual fee, 15% interest rate, and target existing customers...",
        height=100
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🚀 Process with AI", type="primary"):
            if ai_prompt:
                with st.spinner("Processing with AI..."):
                    result = call_openai_api(ai_prompt)
                    
                    # Store supported fields in session state
                    if result.get("supported_fields"):
                        for field_name, value in result["supported_fields"].items():
                            st.session_state.form_data[field_name] = value
                        st.success(f"✅ Auto-filled {len(result['supported_fields'])} fields!")
                    
                    # Store unsupported fields
                    if result.get("unsupported_fields"):
                        st.session_state.unsupported_fields = result["unsupported_fields"]
                        st.warning(f"⚠️ {len(result['unsupported_fields'])} fields were mentioned but not supported")
                    
                    st.session_state.ai_processed = True
                    st.rerun()
            else:
                st.error("Please enter a prompt first")
    
    # Form Fields
    st.subheader("Program Information")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    page_1_fields = FIELD_SCHEMAS["page_1"]
    field_names = list(page_1_fields.keys())
    
    # First column - fields 1-5
    with col1:
        for field_name in field_names[:5]:
            field_info = page_1_fields[field_name]
            current_value = st.session_state.form_data.get(field_name)
            st.session_state.form_data[field_name] = render_field(field_name, field_info, current_value)
    
    # Second column - fields 6-10
    with col2:
        for field_name in field_names[5:]:
            field_info = page_1_fields[field_name]
            current_value = st.session_state.form_data.get(field_name)
            st.session_state.form_data[field_name] = render_field(field_name, field_info, current_value)

def page_2_product_configuration():
    """Page 2: Product Configuration"""
    st.header("🎯 Product Configuration")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    page_2_fields = FIELD_SCHEMAS["page_2"]
    field_names = list(page_2_fields.keys())
    
    # First column - fields 1-5
    with col1:
        for field_name in field_names[:5]:
            field_info = page_2_fields[field_name]
            current_value = st.session_state.form_data.get(field_name)
            st.session_state.form_data[field_name] = render_field(field_name, field_info, current_value)
    
    # Second column - fields 6-10
    with col2:
        for field_name in field_names[5:]:
            field_info = page_2_fields[field_name]
            current_value = st.session_state.form_data.get(field_name)
            st.session_state.form_data[field_name] = render_field(field_name, field_info, current_value)

def page_3_eligibility_rules():
    """Page 3: Eligibility and Rules"""
    st.header("✅ Eligibility and Rules")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    page_3_fields = FIELD_SCHEMAS["page_3"]
    field_names = list(page_3_fields.keys())
    
    # First column - fields 1-5
    with col1:
        for field_name in field_names[:5]:
            field_info = page_3_fields[field_name]
            current_value = st.session_state.form_data.get(field_name)
            st.session_state.form_data[field_name] = render_field(field_name, field_info, current_value)
    
    # Second column - fields 6-10
    with col2:
        for field_name in field_names[5:]:
            field_info = page_3_fields[field_name]
            current_value = st.session_state.form_data.get(field_name)
            st.session_state.form_data[field_name] = render_field(field_name, field_info, current_value)

def review_page():
    """Review Page: Show all entered data"""
    st.header("📊 Review & Submit")
    
    # Show unsupported fields warning if any
    if st.session_state.unsupported_fields:
        st.warning(
            f"⚠️ **Unsupported Fields:** The following fields were mentioned in the AI prompt but are not supported: "
            f"`{'`, `'.join(st.session_state.unsupported_fields)}`"
        )
    
    # Group data by pages
    pages = [
        ("📋 Basic Program Details", "page_1"),
        ("🎯 Product Configuration", "page_2"),
        ("✅ Eligibility and Rules", "page_3")
    ]
    
    for page_title, page_key in pages:
        st.subheader(page_title)
        
        page_fields = FIELD_SCHEMAS[page_key]
        has_data = False
        
        # Create a container for this page's data
        with st.container():
            col1, col2 = st.columns(2)
            field_names = list(page_fields.keys())
            
            with col1:
                for field_name in field_names[:5]:
                    field_info = page_fields[field_name]
                    value = st.session_state.form_data.get(field_name)
                    if value:
                        has_data = True
                        if isinstance(value, list):
                            value = ", ".join(value)
                        st.write(f"**{field_info['label']}:** {value}")
            
            with col2:
                for field_name in field_names[5:]:
                    field_info = page_fields[field_name]
                    value = st.session_state.form_data.get(field_name)
                    if value:
                        has_data = True
                        if isinstance(value, list):
                            value = ", ".join(value)
                        st.write(f"**{field_info['label']}:** {value}")
        
        if not has_data:
            st.write("*No data entered for this section*")
        
        st.divider()
    
    # Submit button
    if st.button("🚀 Submit Program", type="primary", use_container_width=True):
        st.success("✅ Credit Card Program submitted successfully!")
        
        # Show final summary
        st.subheader("📋 Submission Summary")
        total_fields = sum(len(fields) for fields in FIELD_SCHEMAS.values())
        filled_fields = sum(1 for value in st.session_state.form_data.values() if value)
        
        st.write(f"**Total Fields:** {total_fields}")
        st.write(f"**Filled Fields:** {filled_fields}")
        st.write(f"**Completion Rate:** {(filled_fields/total_fields)*100:.1f}%")
        
        if st.session_state.unsupported_fields:
            st.write(f"**Unsupported Fields:** {len(st.session_state.unsupported_fields)}")

def render_progress_indicator():
    """Render progress indicator at the top"""
    pages = ["Basic Details", "Product Config", "Eligibility", "Review"]
    current_page = st.session_state.current_page
    
    # Progress indicator
    progress = (current_page + 1) / len(pages)
    st.progress(progress)
    
    # Page indicator
    st.write(f"Step {current_page + 1} of {len(pages)}: {pages[current_page]}")

def render_navigation_buttons():
    """Render navigation buttons at the bottom"""
    pages = ["Basic Details", "Product Config", "Eligibility", "Review"]
    current_page = st.session_state.current_page
    
    # Add spacing before navigation buttons
    st.markdown("---")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_page > 0:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()
    
    with col3:
        if current_page < len(pages) - 1:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.current_page += 1
                st.rerun()

def main():
    """Main application logic"""
    init_session_state()
    
    st.title("💳 Credit Card Program Setup")
    st.markdown("*Internal tool for implementation team*")
    
    # Render progress indicator at the top
    render_progress_indicator()
    
    st.markdown("---")
    
    # Render current page
    current_page = st.session_state.current_page
    
    if current_page == 0:
        page_1_basic_details()
    elif current_page == 1:
        page_2_product_configuration()
    elif current_page == 2:
        page_3_eligibility_rules()
    elif current_page == 3:
        review_page()
    
    # Render navigation buttons at the bottom
    render_navigation_buttons()

if __name__ == "__main__":
    main() 