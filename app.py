"""
Browser Automation Tools - Main Application (LOCAL - FREE)
A modern UI for Amazon Auto-Buyer and Claim Search tools using local browser-use library
"""

import streamlit as st
import os
import asyncio
import sys
import warnings

# Suppress warnings usually seen on Windows with ProactorEventLoop
if sys.platform == 'win32':
    warnings.filterwarnings("ignore", category=ResourceWarning)
    # Optional: Suppress the specific unclosed transport warning if needed
    # logging.getLogger('asyncio').setLevel(logging.ERROR)

from dotenv import load_dotenv
from amazon_tool import AmazonAutoBuyer
from universal_browser_tool import UniversalBrowserTool

# Fix for Windows asyncio loop policy and suppress cleanup errors
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

class StderrFilter:
    """Filter specific noise from stderr (asyncio connection cleanup on Windows)"""
    def __init__(self, original_stderr):
        self.original_stderr = original_stderr
    
    def write(self, s):
        # Filter out the specific "closed pipe" and "Task was destroyed" noise
        if "I/O operation on closed pipe" in s or \
           "Task was destroyed but it is pending" in s or \
           "unclosed transport" in s or \
           "Exception ignored in:" in s:
            return
        self.original_stderr.write(s)
        
    def flush(self):
        self.original_stderr.flush()

# Apply the filter globally
sys.stderr = StderrFilter(sys.stderr)

def custom_exception_handler(loop, context):
    # Keep the custom handler as a second layer of defense
    pass

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
        ["🏠 Home", "🛒 Amazon Auto-Buyer", "🤖 Universal Automation"],
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
    elif tool_choice == "🤖 Universal Automation":
        show_universal_tool(openai_api_key, model_choice)

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
    
    #### 🤖 Universal Automation
    - **Upgraded & Powerful**: Do almost anything on the web!
    - Login, Search, Scrape, Extract Data
    - Full Proxy & Timeout Support
    - Handle complex multi-step workflows
    
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
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.set_exception_handler(custom_exception_handler)
                        result = loop.run_until_complete(tool.purchase(
                            email=amazon_email,
                            password=amazon_password,
                            product_url=product_url,
                            quantity=quantity,
                            credit_card=credit_card,
                            gift_card_code=gift_card_code if gift_card_code else None,
                            shipping_speed=shipping_speed
                        ))
                        loop.close()
                        
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

def show_universal_tool(api_key: str, model: str):
    """Display Universal Automation tool interface"""
    st.header("🤖 Universal Browser Automation")
    st.markdown("**Power Limitless**: Describe any web task, and I'll do it!")
    
    # Advanced Settings
    with st.expander("⚙️ Advanced Settings (Proxy & Timeout)", expanded=False):
        col_proxy1, col_proxy2 = st.columns(2)
        with col_proxy1:
            proxy_server = st.text_input("Proxy Server (Optional)", placeholder="http://1.2.3.4:8080")
            timeout = st.slider("Timeout (Seconds)", min_value=30, max_value=600, value=120, step=30)
            headless = st.checkbox("Headless Mode (Faster)", value=False)
        with col_proxy2:
            proxy_user = st.text_input("Proxy Username (Optional)")
            proxy_pass = st.text_input("Proxy Password (Optional)", type="password")
            
    # Example instructions
    with st.expander("📝 Example Instructions", expanded=False):
        st.markdown("""
        **Example 1 - General Search:**
        ```
        Go to google.com, search for 'latest AI trends 2024', 
        click on the first 3 non-ad results, and summarize them.
        ```
        
        **Example 2 - Claim Search (Legacy):**
        ```
        Go to https://example.com/login, login with user 'test' and pass '123', 
        navigate to claims, find claim #12345, and extract status.
        ```
        
        **Example 3 - Data Extraction:**
        ```
        Go to amazon.com, search for 'gaming laptop', 
        extract the price and rating of the first 5 items into JSON.
        ```
        """)
    
    with st.form("universal_form"):
        st.subheader("📋 Task Instructions")
        
        instruction = st.text_area(
            "What do you want to do?",
            height=150,
            placeholder="Describe your task in natural language...",
            help="Be specific! Include URLs, credentials, and desired output format."
        )
        
        submitted = st.form_submit_button("🚀 Execute Task", use_container_width=True)
        
        if submitted:
            if not instruction or len(instruction.strip()) < 10:
                st.error("❌ Please provide instructions")
            else:
                with st.spinner("🔄 Executing task..."):
                    try:
                        # Initialize tool
                        tool = UniversalBrowserTool(model=model)
                        
                        # run async
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.set_exception_handler(custom_exception_handler)
                        result = loop.run_until_complete(tool.execute_task(
                            instruction=instruction.strip(),
                            proxy_server=proxy_server if proxy_server else None,
                            proxy_username=proxy_user if proxy_user else None,
                            proxy_password=proxy_pass if proxy_pass else None,
                            timeout=timeout,
                            headless=headless
                        ))
                        loop.close()
                        
                        if result.get("success"):
                            st.success("✅ Task Completed!")
                            
                            # Show structured result
                            if result.get("result"):
                                st.subheader("📊 Output")
                                st.json(result["result"])
                            
                            # Show raw output
                            with st.expander("🔍 Raw Agent Output", expanded=False):
                                st.text(result.get("raw_output", ""))
                        else:
                            st.error(f"❌ Error: {result.get('error')}")
                            st.warning(result.get("message"))
                            
                    except Exception as e:
                        st.error(f"❌ Critical Error: {str(e)}")
                        st.info("Check your settings and try again.")

if __name__ == "__main__":
    main()
