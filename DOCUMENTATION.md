# Universal Browser Automation Tool - Documentation

## 📋 Prerequisites
- **OS**: Windows (tested), macOS, or Linux.
- **Python**: Version **3.11** or **3.12** is REQUIRED.
  - ⚠️ **Do NOT use Python 3.14** (incompatible with dependencies).
  - ⚠️ **Do NOT use Python 3.9 or older**.
- **Browser**: Google Chrome installed on your system.

## 🚀 Installation Guide

### 1. Set up Python Environment
Ensure you have Python 3.12 installed.
```powershell
# Create a virtual environment (recommended)
py -3.12 -m venv venv

# Activate it
.\venv\Scripts\activate
```

### 2. Install Dependencies
This project uses `browser-use` which requires specific versions to run correctly.
```powershell
pip install -r requirements.txt
```

### 3. Install Playwright Browsers
Required for the automation engine.
```powershell
playwright install
```

### 4. Configure API Keys
Create a `.env` file in the root directory if it doesn't exist:
```env
OPENAI_API_KEY=sk-your-key-here
```

## 🏃‍♂️ How to Run

Run the Streamlit application:
```powershell
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

## 🤖 Features & Usage

### 1. Universal Automation
Select **🤖 Universal Automation** from the sidebar.
- **Goal**: Describe any task in natural language.
- **Proxy**: Open "Advanced Settings" to configure a proxy server (`http://ip:port`).
- **Timeout**: Adjust the slider if you expect the task to take longer than 2 minutes.

### Examples
- "Go to google.com and find the stock price of NVDA."
- "Login to https://mysite.com (user: admin, pass: 123) and download the latest report."

### 2. Amazon Auto-Buyer
Select **🛒 Amazon Auto-Buyer**.
- Specialized tool for Amazon automated purchasing.
- *Note: Stops before final checkout for safety.*

## ❓ Troubleshooting

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'playwright'` | Run `playwright install`. |
| `Validation Error` / `JSON Error` | Ensure dependencies are exact versions from `requirements.txt`. |
| `build` / `MVC++` errors | You are likely using Python 3.14. Switch to Python 3.12. |
