# Amazon Auto-Buyer Tool with Browser-Use (Local/Free Potential)

This tool automates Amazon purchasing and product checking using the `browser-use` library and OpenAI's LLM. It controls a real browser to navigate, login, and add items to cart.

## 📋 Prerequisites

1.  **Python 3.11+** installed.
2.  **OpenAI API Key**: You need a valid key from [platform.openai.com](https://platform.openai.com).
3.  **Git** (optional, for cloning).

## 🛠️ Installation

1.  **Install Python Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

2.  **Install Playwright Browsers**:
    This downloads the actual browser binaries (Chromium, Firefox, etc.) used by the automation.
    ```powershell
    playwright install
    ```

3.  **Configure Environment**:
    The project uses a `.env` file to store secrets. I have already created one for you.
    Ensure `d:\New folder\.env` exists and contains:
    ```
    OPENAI_API_KEY=sk-proj-...
    ```

## 🚀 How to Run

1.  **Activate Virtual Environment** (if using one):
    ```powershell
    .\venv\Scripts\activate
    ```

2.  **Run the Tool**:
    ```powershell
    python amazon_tool.py
    ```

    - The tool will launch a **visible browser window**.
    - It will navigate to the product URL.
    - It will attempt to extract price and availability.
    - Watch the terminal for progress logs.

## 🔧 Troubleshooting & Fixes Applied

If you encounter issues, here is what has been fixed/configured:

### 1. `ImportError` / `AttributeError`
- **Issue**: `browser-use` library requires a specific LLM wrapper, not the standard LangChain one.
- **Fix**: Code updated to import from `browser_use.llm.openai.chat`.

### 2. Bot Detection / Empty Page
- **Issue**: Amazon blocks headless browsers (browsers without a UI).
- **Fix**: We enabled **Headful Mode** (`headless=False`) in the code. You will now see the browser open. This significantly reduces bot detection.

### 3. Missing `playwright`
- **Issue**: `playwright` command not found.
- **Fix**: Manually installed via pip and ran `playwright install`.

## ⚠️ Notes
- **Bot Protection**: Amazon has very strong anti-bot protections. If the tool fails to load the page ("dog page" or empty), try running it again or manually solving the CAPTCHA if one appears in the visible window.
- **Cost**: This uses OpenAI's GPT-4o-mini, which is very cheap but not free. To make it 100% free, you would need to install **Ollama** locally and switch the code to use `ChatOllama`.
