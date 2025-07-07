# AI-Powered Form Filler

A Streamlit application that uses OpenAI's GPT-4 to automatically fill out forms based on natural language descriptions.

## Features

- **Three Form Types**: Customer Info, Product Feedback, and Support Request
- **AI Auto-fill**: Uses GPT-4 to parse natural language and fill form fields
- **Dynamic Forms**: Each form has appropriate input types (text, number, select, checkbox, slider, textarea)
- **Session State**: Maintains autofilled data between app reruns
- **Form Validation**: Ensures required fields are filled before submission

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

You need to configure your OpenAI API key. You can do this in one of two ways:

#### Option A: Using Streamlit Secrets (Recommended)

1. Create a `.streamlit` directory in your project root:
   ```bash
   mkdir .streamlit
   ```

2. Create a `secrets.toml` file inside the `.streamlit` directory:
   ```bash
   touch .streamlit/secrets.toml
   ```

3. Add your OpenAI API key to the `secrets.toml` file:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key-here"
   ```

#### Option B: Using Environment Variables

Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## How to Use

1. **Select Form Type**: Choose from Customer Info, Product Feedback, or Support Request
2. **Enter Natural Language Description**: Describe the information you want to fill in the form
3. **Auto-fill**: Click "Auto-fill using GPT" to generate form data
4. **Review and Edit**: Check the autofilled data and make any necessary adjustments
5. **Submit**: Click the submit button to complete the form

## Example Prompts

- **Customer Info**: "A 30-year-old customer from India who is active and interested in premium support"
- **Product Feedback**: "Customer loves the new smartphone app, rates it 5 stars, says it's intuitive and fast"
- **Support Request**: "Critical login issue, user can't access account, prefers to be contacted in the evening"

## Form Fields

### Customer Info
- Name (text input)
- Age (number input)
- Country (select dropdown)
- Is Active Customer (checkbox)

### Product Feedback
- Product Name (text input)
- Rating (slider 1-5)
- Comments (textarea)

### Support Request
- Issue Description (text input)
- Severity (select: Low, Medium, High, Critical)
- Preferred Contact Time (text input)

## Technical Details

- Built with Streamlit for the web interface
- Uses OpenAI's GPT-4 model for natural language processing
- Maintains form state using `st.session_state`
- Includes error handling and validation
- Modern, responsive UI with proper spacing and layout 