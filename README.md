# 🚀 Browser Automation Tools (FREE - Local)

A modern Python application with a beautiful UI for automating browser tasks using the **local browser-use library** (100% FREE, no paid services).

This project includes two powerful tools:

1. **🛒 Amazon Auto-Buyer** - Automate Amazon purchases
2. **🔍 Claim Search Tool** - Login and search for claims on websites

## ✨ Features

- **100% FREE** - Uses local browser-use library, no paid cloud services
- **Privacy First** - All automation runs locally on your machine
- **Modern Streamlit UI** - Beautiful, responsive interface
- **Open Source** - Built with open-source tools
- **Structured Output** - JSON-formatted results
- **Error Handling** - Comprehensive error messages and validation
- **Safety Features** - Stops before final payment for manual review

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (or compatible LLM like DeepSeek, Anthropic, etc.)
  - Get OpenAI key: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
  - Or use DeepSeek (cost-effective): [https://platform.deepseek.com](https://platform.deepseek.com)

## 🛠️ Installation

1. **Clone or download this project**

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```
.\venv312\Scripts\pip install playwright
5. **Set up environment variables**:
   - Create a `.env` file in the project root
   - Add your OpenAI API key (or compatible LLM):
   ```
   OPENAI_API_KEY=sk_your_api_key_here
   ```
   
   **Note**: You can use:
   - OpenAI (GPT-4, GPT-3.5)
   - DeepSeek (cost-effective alternative)
   - Anthropic Claude (if supported)
   - Local models via Ollama (if configured)

## 🚀 Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Tool Descriptions

### 🛒 Amazon Auto-Buyer

Automate your Amazon purchases by providing:
- Amazon account credentials
- Product URL or ASIN
- Quantity and shipping preferences
- Payment information (credit card or gift card)

**Features:**
- Automatic login
- Product selection
- Cart management
- Checkout automation
- **Safety**: Stops before final payment for manual review

**Important**: The tool will stop before completing the final payment. Always review the order before manually confirming the purchase.

### 🔍 Claim Search Tool

Login to websites and search for claims or information:
- Website URL and login credentials
- Search query or specific claim ID
- Date range filtering (optional)
- Structured results extraction

**Features:**
- Automatic login
- Claim search functionality
- Date filtering
- Structured JSON output
- Detailed claim information

## 📁 Project Structure

```
.
├── app.py                 # Main Streamlit application
├── amazon_tool.py         # Amazon Auto-Buyer module
├── claim_search_tool.py   # Claim Search Tool module
├── requirements.txt       # Python dependencies
├── setup_env.py          # Environment setup helper
├── .env                  # Your API keys (not in git)
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🔒 Security Notes

- **Never commit your `.env` file** - It contains sensitive API keys
- **Use environment variables** for all sensitive information
- **Be cautious** when automating purchases - Always verify before completing transactions
- **Check Terms of Service** - Ensure automation is allowed on target websites
- **Your credentials stay local** - All automation runs on your machine

## 💰 Cost Considerations

- **browser-use library**: FREE (open source)
- **LLM API costs**: 
  - GPT-4o-mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
  - GPT-3.5-turbo: ~$0.50 per 1M input tokens, ~$1.50 per 1M output tokens
  - DeepSeek: Much cheaper alternative
- **No cloud service fees** - Everything runs locally

## 🐛 Troubleshooting

### API Key Issues
- Make sure your `.env` file is in the project root
- Verify your API key is correct and active
- Check that `OPENAI_API_KEY` is set correctly
- Ensure you have credits/balance in your OpenAI account

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python version (3.8+)
- Try: `pip install --upgrade browser-use langchain-openai`

### Browser Automation Issues
- Some websites may have anti-automation measures
- Increase wait times if pages load slowly
- Check that Playwright browsers are installed (browser-use will install them automatically)

### Async/Await Errors
- Make sure you're using Python 3.8+ (async/await support)
- Check that asyncio is working properly

## 📚 Documentation

- [Browser-Use Library](https://github.com/browser-use/browser-use)
- [LangChain OpenAI](https://python.langchain.com/docs/integrations/chat/openai)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Python-dotenv Documentation](https://pypi.org/project/python-dotenv/)

## ⚠️ Disclaimer

This tool is for educational and personal use only. Always:
- Respect website Terms of Service
- Use responsibly and ethically
- Verify all automated actions before completion
- Never share your credentials or API keys
- Be aware that some websites may block automation

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📝 License

This project is open source and available for personal and educational use.

---

Made with ❤️ using browser-use (FREE) and Streamlit
