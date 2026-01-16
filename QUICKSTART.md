# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This will install:
- `browser-use` - Local browser automation (FREE)
- `streamlit` - Web UI framework
- `langchain-openai` - LLM integration
- Other dependencies

## Step 2: Set Up API Key

### Option A: Manual Setup
1. Create a `.env` file in the project root
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk_your_api_key_here
   ```

### Option B: Use Setup Script
```bash
python setup_env.py
```
Then edit the `.env` file with your actual API key.

**Get your API key:**
- **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **DeepSeek** (cheaper): [https://platform.deepseek.com](https://platform.deepseek.com)

## Step 3: Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 🎯 Using the Tools

### Amazon Auto-Buyer
1. Select "🛒 Amazon Auto-Buyer" from the sidebar
2. Choose your LLM model (gpt-4o-mini recommended for cost)
3. Fill in:
   - Your Amazon email and password
   - Product URL or ASIN
   - Quantity and shipping preferences
   - Payment information
4. Click "🛒 Buy Now"
5. **Review the order** before manually completing payment

### Claim Search Tool
1. Select "🔍 Claim Search Tool" from the sidebar
2. Choose your LLM model
3. Fill in:
   - Website URL
   - Login credentials
   - Search query or claim ID
   - Optional date filters
4. Click "🔍 Search Claims"

## 💡 Tips

- **Model Selection**: Use `gpt-4o-mini` for most tasks (cost-effective)
- **Cost Management**: Monitor your API usage on OpenAI dashboard
- **Safety**: Always verify purchases before completing payment
- **Wait Times**: Increase wait time slider if pages load slowly
- **Privacy**: All automation runs locally on your machine

## 🆘 Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Visit [Browser-Use GitHub](https://github.com/browser-use/browser-use)
- Ensure your API key is valid and has credits
- Check that all dependencies are installed correctly

## 💰 Cost Estimate

- **browser-use**: FREE
- **GPT-4o-mini**: ~$0.15-0.60 per task (very affordable)
- **GPT-3.5-turbo**: ~$0.50-1.50 per task
- **DeepSeek**: Even cheaper alternative

**Total**: Only pay for LLM API calls, no subscription fees!

Happy automating! 🎉
