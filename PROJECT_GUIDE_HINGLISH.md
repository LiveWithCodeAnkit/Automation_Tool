## 🧠 Project Overview (Hinglish)

Yeh project ek **browser automation toolkit** hai jo tumhare normal PC par chalta hai (local), aur **Streamlit UI** ke through 2 main tools deta hai:

- **🛒 Amazon Auto-Buyer** – Amazon par login karke product dekhna, cart mein daalna, checkout tak le jaana (final payment se pehle rukta hai).
- **🤖 Universal Browser Automation** – Kisi bhi website par “human jaise” steps follow karke kaam karwa sakte ho (search, login, scrape, data nikalna, etc.).

Backend mein yeh tools **`browser-use` library + LLM (jaise OpenAI GPT-4o-mini)** use karte hain jo natural language instructions ko browser actions mein convert karta hai (click, type, navigate, wait, etc.).

---

## 🏗 High-Level Architecture (Simple Flow)

1. **User** browser se `http://localhost:8501` open karta hai  
2. `streamlit` **`app.py`** run karta hai → UI load hoti hai  
3. User ek tool select karta hai:
   - Amazon Auto-Buyer → class `AmazonAutoBuyer` (`amazon_tool.py`)
   - Universal Automation → class `UniversalBrowserTool` (`universal_browser_tool.py`)
4. Tum form mein details / instructions bharte ho  
5. App ek **task description** banata hai (plain English text)  
6. LLM (OpenAI GPT-4o-mini) ko yeh task + page context diya jata hai  
7. `browser-use` real browser open karke LLM ke plan follow karta hai:
   - pages open karna
   - login form bharna
   - buttons click karna
   - data nikalna
8. Result ko LLM se **JSON format** mein mangwaya jata hai  
9. Streamlit UI us JSON ko tumhe nicely show karti hai (success / error ke saath).

---

## 🗂 Important Files and Unka Role

- **`app.py`**
  - Main Streamlit app
  - Sidebar navigation:
    - 🏠 Home
    - 🛒 Amazon Auto-Buyer
    - 🤖 Universal Automation
  - `.env` se `OPENAI_API_KEY` load karta hai
  - Har tool ke liye Streamlit forms banata hai
  - Async functions (`AmazonAutoBuyer.purchase`, `UniversalBrowserTool.execute_task`) ko event loop se run karata hai
  - Windows-specific asyncio noise / warnings ko filter karta hai.

- **`amazon_tool.py`**
  - Class: **`AmazonAutoBuyer`**
  - Do main kaam:
    1. **`purchase(...)`** – Amazon pe purchase flow automate karna  
    2. **`check_product_availability(...)`** – Product details nikalna (price, rating, availability, etc.)
  - `browser-use` ka `Browser` headless=False mode mein use karta hai → real browser dikhai deta hai.
  - LLM ko detailed instructions deta hai:
    - login steps
    - quantity, shipping speed
    - gift card / credit card info
    - **IMPORTANT**: “Final ‘Place Order’ button se pehle RUKO”
  - LLM se JSON output mangta hai → helper `_parse_json_output` se parse karta hai.

- **`universal_browser_tool.py`**
  - Class: **`UniversalBrowserTool`**
  - Generic tool jahan tum koi bhi **natural language instructions** doge:
    - “Jaao google.com, yeh search karo, pehle 3 result ke summary nikaalo”
    - “Is site pe login karo, claims list nikaalo, status batao”
  - Support:
    - **Headless / Headful mode**
    - **Proxy** (server + optional username/password)
    - **Timeout** (agar task bohot long hai)
  - Instructions se ek `task_description` banta hai, phir:
    - `BrowserConfig` banata hai (headless, proxy etc.)
    - `Agent` run karta hai (`agent.run()` with timeout)
    - Output ko JSON mein parse karta hai.

- **`README.md`**
  - Project ka polished English overview
  - Installation, features, tools overview, security, cost, troubleshooting.

- **`QUICKSTART.md`**
  - “5 minute mein shuru kaise karein” type short guide:
    - `pip install -r requirements.txt`
    - `.env` setup
    - `streamlit run app.py`

- **`DOCUMENTATION.md`**
  - Universal tool ke liye thoda zyada technical docs (Python version, errors, etc.)

- **`AY.md`**
  - Amazon Auto-Buyer ke liye dedicated doc (requirements, Playwright install, notes, fixes).

- **`.env`**
  - Yahan tumhara **`OPENAI_API_KEY`** rehta hai
  - **Git mein commit nahi karna**.

---

## 🔄 Detailed Flow – Amazon Auto-Buyer

### 1. User Input (UI side)

In `app.py` → `show_amazon_tool()`:
- Tum form mein yeh details bharte ho:
  - Amazon Email + Password
  - Product URL / ASIN
  - Quantity
  - Shipping Speed
  - Credit Card (last 4 digits ya pura)
  - Optional Gift Card code
- Button: **“🛒 Buy Now”** dabate ho

### 2. Backend Call

Button submit hone par:
- `AmazonAutoBuyer(model=model)` instance banta hai
- Event loop create hota hai
- `buyer.purchase(...)` async function run hota hai

### 3. Inside `AmazonAutoBuyer.purchase`

1. **Task description** string banti hai:
   - “Go to {product_url}”
   - “Login with email/password”
   - “Add {quantity} to cart”
   - “Select shipping speed”
   - Optional: gift card / credit card info
   - ⚠ “STOP before final Place Order”
   - Output JSON structure example (product_title, order_total, delivery_date, status)
2. `Browser(headless=False)` banaya jata hai → real browser open hota hai
3. `Agent(task, llm, browser)` ban ke `await agent.run()` chalta hai
4. Agent pura flow complete karke final text result deta hai
5. `_parse_json_output`:
   - Direct JSON parse try karta hai
   - Nahi hua to regex se `{ ... }` block nikal ke parse karta hai
6. Function dict return karta hai:
   - `{"success": True, "result": parsed_result}`
   - Ya error ke case mein:
     - `{"success": False, "error": "...", "message": "..."}`

### 4. Result UI par

`app.py` mein:
- Agar `success` hai:
  - `st.success("✅ Purchase process completed!")`
  - `st.json(result)`
  - Agar warning ho, to `st.warning(...)`
- Agar `success=False`:
  - `st.error("❌ Error: ...")`

---

## 🔄 Detailed Flow – Universal Automation Tool

### 1. User Input (UI side)

In `app.py` → `show_universal_tool()`:
- Advanced settings expander:
  - Proxy server / user / pass
  - Timeout (slider)
  - Headless mode checkbox
- Main form:
  - **Instruction text area** – tum plain English / Hinglish instructions likhte ho:
    - Example: “Go to google.com, search ‘latest AI trends 2024’, pehle 3 result ka summary JSON mein de do.”
- Button: **“🚀 Execute Task”**

### 2. Backend Call

Submit pe:
- `UniversalBrowserTool(model=model)` banaya jata hai
- Async `execute_task(...)` run hota hai with:
  - `instruction`
  - `proxy_*`
  - `timeout`
  - `headless`

### 3. Inside `UniversalBrowserTool.execute_task`

1. Proxy string format karta hai (agar diya ho)
2. `task_description` text banata hai:
   - Tumhare instruction
   - Saath me note: “Return results as structured JSON”
3. `BrowserConfig` prepare:
   - `headless`
   - optional `proxy={"server": proxy_url}`
4. `Browser(config=BrowserConfig(...))` + `Agent(task, llm, browser)` banata hai
5. `asyncio.wait_for(agent.run(), timeout=timeout)`:
   - Agar time limit se pehle ho gaya → `history` milta hai
   - Varna `TimeoutError` → friendly error dict return
6. `history.final_result()` se text nikalta hai
7. `_parse_json_output` se JSON parse:
   - Direct `json.loads`
   - Ya regex fallback
8. Return:
   - `{"success": True, "result": parsed, "raw_output": text}`
   - Ya error dict.

### 4. Result UI par

`app.py` mein:
- Success pe:
  - `st.success("✅ Task Completed!")`
  - `st.json(result["result"])`
  - Raw output expander mein text
- Error pe:
  - `st.error(...)` + optional warning/info.

---

## 🧪 Typical Use Cases (Developer View)

- Quickly script:
  - Amazon product checks for price changes
  - Competitor website scraping (public info)
  - Dashboard se reports download
  - Login-required internal tools se data nikalna
- Without manually writing Playwright steps:
  - Sirf instructions likho, LLM + browser-use steps generate kar leta hai.

---

## 🧑‍💻 Developer Notes (Tech Stack)

- **Language**: Python
- **Frontend**: Streamlit
- **Automation**: `browser-use` (Playwright-based)
- **LLM Integration**: `langchain-openai.ChatOpenAI`
- **Config / Secrets**: `.env` + `python-dotenv`
- **Async**: `asyncio` with custom Windows loop policy
- **OS Target**: Primarily Windows, but code Linux/macOS pe bhi chal sakta hai (Python + Playwright supported hon to).

**Important Constraints:**
- Recommended Python version: **3.11 / 3.12**
- Python 3.14 par kuch libraries warning / errors de sakti hain (already logs mein dekh chuke ho).

---

## 🙋 Non-Coder Friendly Explanation

Yeh section un logon ke liye hai jo coding nahi jaante, bas tool use karna chahte hain.

### Yeh project actually karta kya hai?

Socho tum kisi dost ko bolte ho:

> “Yaar, Amazon kholo, yeh product search karo, price check karo, cart mein daalo, aur mujhe details bata do.”

Iss project mein **computer tumhara dost ban jata hai**:

- Tum normal language mein instructions likhte ho
- System ek **real browser** kholta hai (Chrome jaisa)
- Screen pe woh aise hi click/type karta hai jaise koi aadmi kar raha ho
- Kaam hone ke baad result tumko text / table / JSON ki form mein dikha deta hai.

### Tumhe kya karna hota hai?

1. Ek baar Python + dependencies install karni padti hain (ye usually developer/senior kar dega).
2. Tum sirf ye steps follow karte ho:
   - Terminal / PowerShell mein:
     - `streamlit run app.py`
   - Browser mein:
     - Page open ho jayega `http://localhost:8501`
3. UI par:
   - Left side se tool select karo:
     - **Amazon Auto-Buyer**
     - **Universal Automation**
   - Form bhar do:
     - Amazon ke liye:
       - Email, Password, Product URL, Quantity, Shipping, Payment info
     - Universal ke liye:
       - Instructions: “kya karwana hai”
   - Button dabao (Buy Now / Execute Task)

### Kya risk / dhyaan rakhna hai?

- **Credentials**:
  - Amazon ya kisi website ka username/password tum apne local machine pe daal rahe ho
  - Yeh kahin server pe nahi ja raha (code local hai), lekin phir bhi:
    - Sirf trusted machines par use karo
    - Kisi aur ko `.env` ya code mat bhejo jisme tumhari keys likhi ho

- **Payment**:
  - Amazon tool **final “Place Order” se pehle ruk jata hai**  
  - Tumhe manually check karna hai:
    - Address sahi hai?
    - Price / quantity theek hai?
    - Payment method sahi hai?
  - Fir chaaho to tum khud “Place Order” click kar sakte ho.

- **API Key Cost**:
  - Jo “AI dimag” use ho raha hai (OpenAI / DeepSeek), uska thoda sa cost hota hai
  - Usually bohot low hota hai, lekin:
    - Agar bohot zyada runs karoge to bill badh sakta hai
    - OpenAI dashboard par usage dekh sakte ho.

### Non-coder ke liye simple summary

- Tum isko ek **smart assistant** samjho jo:
  - Tumhari bat samajhta hai (English / Hinglish instructions)
  - Tumhare browser mein kaam karta hai (jaise ek virtual intern)
  - Result neatly screen par dikha deta hai
- Tumhe **code samajhne ki zarurat nahi**, bas:
  - App kaise chalani hai
  - Konsa form kis kaam ke liye hai
  - Aur apni sensitive cheezein (password, card info, API key) kahan rakhni hain, ye pata hona chahiye.

---

## ✅ How to Study This Project (Step-by-Step)

Agar tum developer ho aur project deeply samajhna chahte ho:

1. **Pehle yeh doc padh lo** (jo tum abhi padh rahe ho 👀).
2. `app.py` open karo:
   - Dekho UI kaise bani hai
   - Dekho kaun se functions kis button se call ho rahe hain.
3. `amazon_tool.py` padho:
   - `AmazonAutoBuyer` class
   - `purchase()` ka task description
   - `check_product_availability()` ka JSON output.
4. `universal_browser_tool.py` padho:
   - Proxy, timeout, headless options
   - Generic instruction → task_description.
5. `README.md`, `QUICKSTART.md`, `DOCUMENTATION.md`, `AY.md` quickly skim karo:
   - Environment setup
   - Python version constraints
   - Playwright install.

Iske baad tum easily code modify karke:
- apni custom tools bana sakte ho,
- nayi websites ke liye specialized flows add kar sakte ho,
- ya automation ko aur smart bana sakte ho.

