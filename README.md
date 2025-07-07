# Credit Card Program Setup Tool

A multi-page Streamlit application for creating and editing credit card programs and promotions. This is a POC (Proof of Concept) for an internal tool used by the implementation team.

## Features

- **Multi-page Flow**: 4-page workflow for comprehensive program setup
- **AI-Powered Auto-fill**: Uses GPT-4 to extract field values from natural language descriptions
- **Comprehensive Form Fields**: 30 different fields across 3 setup pages covering all input types
- **Session State Management**: Maintains data persistence across pages
- **Navigation System**: Back/Next buttons with progress indicator
- **Review & Submit**: Final review page with validation and submission

## Application Flow

### 1. Basic Program Details (Page 1)
- **AI Prompt Integration**: Natural language input to auto-fill fields
- **10 Fields**: Program name, code, dates, budget, status, audience, etc.
- **Field Types**: Text, number, date, select, multiselect, slider, checkbox, time, textarea

### 2. Product Configuration (Page 2)
- **10 Fields**: Product type, fees, limits, interest rates, rewards, features, etc.
- **Field Types**: Radio, number, select, slider, multiselect, checkbox, text, textarea

### 3. Eligibility and Rules (Page 3)
- **10 Fields**: Age limits, income requirements, credit scores, employment, etc.
- **Field Types**: Number, select, multiselect, radio, slider, checkbox, time, textarea

### 4. Review & Submit (Page 4)
- **Data Summary**: All entered information grouped by page
- **Unsupported Fields Warning**: Shows fields mentioned in AI prompt but not supported
- **Submission**: Final program submission with completion statistics

## AI Integration

The application includes intelligent form filling using OpenAI's GPT-4:

### Example Prompts:
- "Create a new Gold Card program ABC123, launch on Aug 1, 2025, with $50 annual fee, 15% interest rate, and target existing customers"
- "Make changes to program XYZ789, change product type to Platinum Card, set credit limit to $25,000, enable travel insurance"

### AI Capabilities:
- **Field Extraction**: Automatically maps natural language to form fields
- **Multi-page Population**: Fills relevant fields across all 3 pages
- **Unsupported Field Detection**: Identifies mentioned fields not available in the form
- **Smart Validation**: Ensures data types and formats match field requirements

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

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

1. **Start Setup**: Begin with Basic Program Details page
2. **Use AI (Optional)**: Enter natural language description and click "Process with AI"
3. **Fill Forms**: Complete fields manually or review AI-filled data
4. **Navigate**: Use Back/Next buttons to move between pages
5. **Review**: Check all entered data on the Review page
6. **Submit**: Complete the program setup

## Form Field Types

The application demonstrates all major Streamlit input types:

- **Text Input**: Program names, codes, descriptions
- **Number Input**: Budgets, fees, age limits, income
- **Date Picker**: Launch dates, effective dates
- **Time Input**: Launch times, review times
- **Select Box**: Status, credit limits, requirements
- **Multi-Select**: Target audiences, features, employment types
- **Radio Buttons**: Product types, residence requirements
- **Checkboxes**: Auto-renewal, activation, bankruptcy allowance
- **Sliders**: Duration, interest rates, debt ratios
- **Text Areas**: Descriptions, notes, detailed information

## Technical Details

- **Framework**: Streamlit for web interface
- **AI Integration**: OpenAI GPT-4 for natural language processing
- **State Management**: Session state for multi-page persistence
- **Navigation**: Custom navigation system with progress tracking
- **Field Validation**: Comprehensive form validation and error handling
- **Responsive Design**: Clean, modern UI with proper spacing and layout

## File Structure

```
credit-card-program-setup/
├── app.py                     # Main application
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .streamlit/
│   ├── secrets.toml          # API keys (not in git)
│   └── secrets.toml.example  # Template for secrets
├── PROJECT_REPORT.md         # Detailed project documentation
└── DEPLOYMENT_GUIDE.md       # Deployment instructions
```

## Development Notes

- **Modular Design**: Each page is implemented as a separate function
- **Clean Code**: Well-structured with proper separation of concerns
- **Error Handling**: Comprehensive error handling for AI integration
- **Debug Mode**: Debug information panel for development
- **Session Management**: Proper state management across page transitions

## Future Enhancements

- **Database Integration**: Store programs in persistent database
- **User Authentication**: Role-based access control
- **Approval Workflow**: Multi-step approval process
- **Export Functionality**: Export program details to PDF/Excel
- **Template System**: Pre-defined program templates
- **Audit Trail**: Track all changes and approvals
- **Bulk Operations**: Handle multiple programs simultaneously

## Support

For questions or issues:
- Check the deployment guide for setup help
- Review the project report for technical details
- Ensure OpenAI API key is properly configured
- Verify all dependencies are installed correctly 