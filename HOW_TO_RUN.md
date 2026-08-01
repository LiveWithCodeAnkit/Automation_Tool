# How to Run This Project

## What you need

- **Windows 10/11**
- **Python 3.11 or 3.12** (recommended: 3.12). Do not use Python 3.14.
- **Google Chrome** installed
- An **OpenAI API key** in a `.env` file
- **PowerShell** or **Command Prompt**

---

## Windows (PowerShell)

Open PowerShell, go to the project folder, then run each step.

### 1. Go to the project folder

```powershell
cd C:\Users\Ankit\Desktop\Projects\Automation_Tool
```

### 2. Create a virtual environment

```powershell
py -3.12 -m venv venv312
```

If `py -3.12` fails, try:

```powershell
python -m venv venv312
```

### 3. Activate the virtual environment

**PowerShell:**

```powershell
.\venv312\Scripts\Activate.ps1
```

If you get an execution policy error, run this once, then activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\venv312\Scripts\Activate.ps1
```

**Command Prompt (CMD):**

```cmd
venv312\Scripts\activate.bat
```

You should see `(venv312)` at the start of the prompt.

### 4. Install dependencies

```powershell
pip install -r requirements.txt
playwright install
```

### 5. Add your API key

Create a file named `.env` in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
```

Or run:

```powershell
python setup_env.py
```

Then edit `.env` and put in your real key.

### 6. Start the app

```powershell
streamlit run app.py
```

The UI opens at **http://localhost:8501**.

### 7. Stop the app

Press `Ctrl + C` in the same terminal.

---

## Using the tools

In the sidebar, pick:

1. **Amazon Auto-Buyer** — login, find a product, go through checkout (stops before final payment for safety)
2. **Universal Automation** — describe any browser task in plain English (search, login, scrape, etc.)

Choose a model in the sidebar (e.g. `gpt-4o-mini` for lower cost).

---

## Optional: run Amazon tool alone (no UI)

With the venv still activated:

```powershell
python amazon_tool.py
```

---

## Common Windows issues

| Problem | Fix |
|--------|-----|
| `py` / `python` not found | Install Python 3.12 from [python.org](https://www.python.org/downloads/) and tick **Add python.exe to PATH** |
| `Activate.ps1` cannot be loaded | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `ModuleNotFoundError: playwright` | Activate venv, then run `playwright install` |
| Build / MVC++ errors | Use Python 3.12, not 3.14 |
| API key errors | Check `.env` is in the project root with `OPENAI_API_KEY=...` |
| Browser fails / empty page | A visible Chrome window should open; solve CAPTCHA there if shown |

---

## macOS / Linux (optional)

```bash
cd /path/to/Automation_Tool
python3.12 -m venv venv312
source venv312/bin/activate
pip install -r requirements.txt
playwright install
streamlit run app.py
```
