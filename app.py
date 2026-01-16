"""
Browser Automation Tools - Main Application (LOCAL - FREE)
A modern UI for Amazon Auto-Buyer and Claim Search tools using local browser-use library
"""

import streamlit as st
import os
import asyncio
import sys
from dotenv import load_dotenv
from amazon_tool import AmazonAutoBuyer
from claim_search_tool import ClaimSearchTool

# Fix for Windows asyncio loop policy to allow subprocesses (Playwright)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Browser Automation Tools",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .tool-card {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Browser Automation Tools</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Check API Key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("⚠️ Please set OPENAI_API_KEY in your .env file")
        st.info("Get your API key from: https://platform.openai.com/api-keys")
        st.info("💡 You can also use DeepSeek, Anthropic, or other compatible LLM APIs")
        st.code("OPENAI_API_KEY=sk_your_api_key_here", language="bash")
        st.markdown("""
        ### Supported LLM Providers:
        - **OpenAI** (GPT-4, GPT-3.5)
        - **DeepSeek** (Cost-effective alternative)
        - **Anthropic Claude** (if supported)
        - **Local models** via Ollama (if configured)
        """)
        return
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    tool_choice = st.sidebar.radio(
        "Select Tool",
        ["🏠 Home", "🛒 Amazon Auto-Buyer", "🔍 Claim Search Tool"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Powered by Local Browser-Use (FREE)")
    
    # Model selection in sidebar
    st.sidebar.subheader("⚙️ Settings")
    model_choice = st.sidebar.selectbox(
        "LLM Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"],
        index=0,
        help="Choose the model. gpt-4o-mini is cost-effective for most tasks."
    )
    
    # Main content based on selection
    if tool_choice == "🏠 Home":
        show_home()
    elif tool_choice == "🛒 Amazon Auto-Buyer":
        show_amazon_tool(openai_api_key, model_choice)
    elif tool_choice == "🔍 Claim Search Tool":
        show_claim_tool(openai_api_key, model_choice)

def show_home():
    """Display home page with tool descriptions"""
    st.markdown("""
    ## Welcome to Browser Automation Tools! 🎉
    
    This application provides powerful browser automation capabilities using the **local browser-use library** (100% FREE).
    Choose a tool from the sidebar to get started.
    
    ### Available Tools:
    
    #### 🛒 Amazon Auto-Buyer
    - Automate Amazon purchases with your credentials
    - Input product details and payment information
    - Complete checkout automatically (stops before final payment for safety)
    
    #### 🔍 Claim Search Tool
    - Login to specific websites
    - Search for claims or specific information
    - Retrieve structured results
    
    ### Getting Started:
    1. Make sure you have your **OpenAI API key** (or compatible LLM) set in `.env` file
    2. Select a tool from the sidebar
    3. Fill in the required information
    4. Click the action button to execute
    
    ### 💡 Features:
    - ✅ **100% FREE** - No paid cloud services
    - ✅ **Local Execution** - Runs on your machine
    - ✅ **Privacy First** - Your credentials stay local
    - ✅ **Modern UI** - Beautiful Streamlit interface
    """)

def show_amazon_tool(api_key: str, model: str):
    """Display Amazon Auto-Buyer tool interface"""
    st.header("🛒 Amazon Auto-Buyer")
    st.markdown("Automate your Amazon purchases with ease!")
    st.info("⚠️ **Safety Feature**: The tool will stop before final payment confirmation. Please review manually before completing.")
    
    with st.form("amazon_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔐 Amazon Credentials")
            amazon_email = st.text_input("Email", type="default", help="Your Amazon account email")
            amazon_password = st.text_input("Password", type="password", help="Your Amazon account password")
            
            st.subheader("💳 Payment Information")
            credit_card = st.text_input("Credit Card Number", help="Last 4 digits or full number")
            gift_card_code = st.text_input("Gift Card Code (Optional)", help="Amazon gift card code if applicable")
        
        with col2:
            st.subheader("📦 Product Details")
            product_url = st.text_input("Product URL or ASIN", help="Amazon product URL or ASIN")
            quantity = st.number_input("Quantity", min_value=1, max_value=10, value=1)
            
            st.subheader("🚚 Shipping")
            shipping_speed = st.selectbox(
                "Shipping Speed",
                ["Standard", "Expedited", "Priority", "Same Day"]
            )
        
        submitted = st.form_submit_button("🛒 Buy Now", use_container_width=True)
        
        if submitted:
            if not amazon_email or not amazon_password or not product_url:
                st.error("❌ Please fill in all required fields (Email, Password, Product URL)")
            else:
                with st.spinner("🔄 Processing your purchase..."):
                    try:
                        # API key now loaded from .env automatically
                        tool = AmazonAutoBuyer(model=model)
                        # Run async function
                        result = asyncio.run(tool.purchase(
                            email=amazon_email,
                            password=amazon_password,
                            product_url=product_url,
                            quantity=quantity,
                            credit_card=credit_card,
                            gift_card_code=gift_card_code if gift_card_code else None,
                            shipping_speed=shipping_speed
                        ))
                        
                        if result.get("success"):
                            st.success("✅ Purchase process completed!")
                            st.json(result)
                            
                            if result.get("result", {}).get("warning"):
                                st.warning(result["result"]["warning"])
                        else:
                            st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        st.info("💡 Make sure browser-use is properly installed and you have a valid API key")

def show_claim_tool(api_key: str, model: str):
    """Display Claim Search tool interface"""
    st.header("🔍 Claim Search Tool")
    st.markdown("**Simple & Flexible**: Just describe what you want to do in natural language!")
    
    # Example instructions
    with st.expander("📝 Example Instructions", expanded=False):
        st.markdown("""
        **Example 1 - Search Claims:**
        ```
        Go to https://example.com, login with email user@example.com and password mypass123, 
        then search for all insurance claims from 2024 and return them as JSON with claim ID, 
        status, date, and amount.
        ```
        
        **Example 2 - Get Specific Claim:**
        ```
        Login to https://claims.example.com with username john@email.com and password pass123, 
        find claim number CLM-2024-001 and return all its details including status history.
        ```
        
        **Example 3 - Search with Filters:**
        ```
        Go to https://portal.example.com, login with email test@test.com and password test123, 
        navigate to claims section, filter claims from January 2024 to December 2024, 
        and return all pending claims with their details.
        ```
        """)
    
    with st.form("claim_form"):
        st.subheader("📋 Enter Your Task Instructions")
        
        instruction = st.text_area(
            "What do you want to do?",
            height=150,
            placeholder="Example: Go to https://example.com, login with email user@example.com and password mypass123, then search for all claims from 2024 and return them as JSON...",
            help="Describe your task in natural language. Include website URL, login credentials, and what you want to search/find."
        )
        
        submitted = st.form_submit_button("🚀 Execute Task", use_container_width=True)
        
        if submitted:
            if not instruction or len(instruction.strip()) < 20:
                st.error("❌ Please provide detailed instructions (at least 20 characters)")
                st.info("💡 Include: Website URL, login credentials, and what you want to do")
            else:
                with st.spinner("🔄 Executing your task... This may take a minute."):
                    try:
                        # API key now loaded from .env automatically
                        tool = ClaimSearchTool(model=model)
                        # Run async function with execute_task method
                        result = asyncio.run(tool.execute_task(instruction=instruction.strip()))
                        
                        if result.get("success"):
                            st.success("✅ Task completed successfully!")
                            
                            # Display results
                            result_data = result.get("result", {})
                            
                            # If claims found, display them nicely
                            if isinstance(result_data, dict) and "claims" in result_data:
                                claims = result_data.get("claims", [])
                                if claims:
                                    st.subheader(f"📋 Found {len(claims)} Claim(s):")
                                    for i, claim in enumerate(claims, 1):
                                        with st.expander(f"Claim #{i}: {claim.get('id', 'N/A')}", expanded=False):
                                            st.json(claim)
                                else:
                                    st.info("No claims found")
                            
                            # Show full JSON result
                            with st.expander("📄 Full Result (JSON)", expanded=False):
                                st.json(result)
                            
                            # Show raw output if available
                            if result.get("raw_output"):
                                with st.expander("🔍 Raw Output", expanded=False):
                                    st.text(result["raw_output"])
                        else:
                            st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                            if result.get("message"):
                                st.info(f"ℹ️ {result['message']}")
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        st.info("💡 Make sure browser-use is properly installed and you have a valid API key")
                        st.info("💡 Check that your instructions are clear and include all necessary details")

if __name__ == "__main__":
    main()
