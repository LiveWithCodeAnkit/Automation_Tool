## 🤖 Universal Browser Tool – Deep Dive (Hinglish)

Yeh document sirf **`universal_browser_tool.py`** ke liye hai – andar kya ho raha hai, kaun se objects bante hain, Agent ka flow kya hai, timeout/proxy kaise kaam karte hain, sab detail mein.

File ka main class:
- `UniversalBrowserTool`

---

## 🧩 High-Level Idea

Simple language mein:

- Tum UI mein ek **natural language instruction** likhte ho:  
  > "Google jaa, yeh search kar, pehle 3 result ka summary JSON mein de."

- `UniversalBrowserTool` is instruction ko:
  1. Thoda **wrap** karta hai (JSON return ka instruction add karke),
  2. `browser-use` ka **`Browser` + `Agent`** banata hai,
  3. `Agent.run()` se **real browser automation** chalata hai,
  4. LLM se jo final text aata hai usme se **JSON extract** karke tumhe return karta hai.

Isme 3 core cheezein important hain:

1. **LLM** – `ChatOpenAI` (OpenAI ke model jaise `gpt-4o-mini`)  
2. **Browser** – `browser_use.browser.browser.Browser` (Playwright based)  
3. **Agent** – `browser_use.Agent` (jo LLM + Browser ko jodta hai)

---

## 🧱 UniversalBrowserTool – Class Structure

Code ka skeleton (conceptual):

```python
class UniversalBrowserTool:
    def __init__(self, model="gpt-4o-mini"):
        self.output_model = model
        self.llm = ChatOpenAI(model=model, temperature=0)

    async def execute_task(...):
        # proxy config build karo
        # task_description banao
        # BrowserConfig + Browser + Agent banao
        # agent.run() timeout ke saath chalao
        # result se JSON parse karo
```

### `__init__`

- `model` argument:  
  - UI se aata hai (Streamlit sidebar se: `gpt-4o-mini`, `gpt-4o`, etc.)
- `self.llm = ChatOpenAI(...)`:
  - `langchain_openai.ChatOpenAI` wrapper use ho raha hai.
  - Ye internally OpenAI API ko call karega (`OPENAI_API_KEY` `.env` se).
  - `temperature=0` → deterministic / predictable answers.

---

## 🔁 `execute_task()` – Step by Step

Signature:

```python
async def execute_task(
    self,
    instruction: str,
    proxy_server: Optional[str] = None,
    proxy_username: Optional[str] = None,
    proxy_password: Optional[str] = None,
    timeout: int = 120,
    headless: bool = False
) -> Dict[str, Any]:
```

Yeh function **poora universal automation** sambhalta hai. Chalo line-by-line flow dekhte hain.

### 1. Proxy Config Banana

```python
proxy_config = None
if proxy_server:
    if proxy_username and proxy_password:
        proxy_parts = proxy_server.split("://")
        protocol = proxy_parts[0] if len(proxy_parts) > 1 else "http"
        host = proxy_parts[-1]
        proxy_config = f"{protocol}://{proxy_username}:{proxy_password}@{host}"
    else:
        proxy_config = proxy_server
```

Hinglish:

- Agar tumne UI se **proxy server** diya (jaise `http://1.2.3.4:8080`):
  - Agar user+pass bhi diye:
    - To string ko is format mein convert karta hai:  
      `http://user:pass@1.2.3.4:8080`
  - Agar sirf server diya:
    - To wahi string as-is use hoti hai.

Ye `proxy_config` baad mein `BrowserConfig` mein jaata hai.

### 2. Task Description Banana

```python
task_description = f"""
{instruction}

IMPORTANT: Return the results as structured JSON format with all the information you found.
"""
```

Yahan 2 cheezein hoti hain:

- Tumhara **raw instruction** direct embed hota hai (full trust).
- Saath mein ek extra line add hoti hai:
  - “Results structured JSON format mein wapas do.”

Iska matlab:

- LLM ko clearly bola ja raha hai ke end mein woh JSON return kare,
- Taaki hum baad mein directly `json.loads` se parse kar sakein.

### 3. BrowserConfig + Browser Banana

```python
from browser_use.browser.browser import Browser, BrowserConfig

config_args = {
    "headless": headless,
}

if proxy_config:
   config_args["proxy"] = {"server": proxy_config}

browser = Browser(config=BrowserConfig(**config_args))
```

Yahan:

- `BrowserConfig` ko dynamic args diye ja rahe hain:
  - `headless`:  
    - `False` → visible browser (window dikhegi)  
    - `True` → headless (background mein, zyada fast/lekin kabhi-kabhi sites detect kar leti hain)
  - `proxy`:  
    - Agar diya gaya, to `{"server": "http://user:pass@host:port"}` jaisa dict.

- `Browser(config=...)` call se:
  - Internal Playwright browser instance create hota hai.
  - Yeh wahi browser hai jisme tumne object marking / steps wagaira dekhe honge.

### 4. Agent Banana

```python
agent = Agent(
    task=task_description,
    llm=self.llm,
    browser=browser,
)
```

`Agent` ka kaam:

- Tumhara **task** (natural language + JSON instruction) leta hai,
- `llm` se plan banwata hai:
  - kis URL pe jaana hai,
  - kaun se elements par click / type karna hai,
  - kaise scroll / wait karna hai,
- `browser` object ke through actual actions perform karta hai.

Yahi woh jagah hai jahan:

- **Object markings**,  
- **Step-wise logs**,  
- **Agent history**,  
ye sab bante hain (jo tumne run karte waqt dekha).

Snapshot:

- Har step par LLM decide karta hai:
  - Next action: `click`, `fill`, `wait_for_selector`, etc.
  - Browser execute karta hai.
  - Page ka naya state LLM ko wapas diya jaata hai.

### 5. Agent Run with Timeout

```python
try:
    history = await asyncio.wait_for(agent.run(), timeout=timeout)
except asyncio.TimeoutError:
    return {
        "success": False,
        "error": f"Task timed out after {timeout} seconds",
        "message": "The automation took too long to complete."
    }
```

Important points:

- `agent.run()` ek **async coroutine** hai jo:
  - Pura interactive session run karta hai,
  - End mein ek **history / result object** deta hai.
- `asyncio.wait_for(..., timeout=timeout)`:
  - Agar task `timeout` seconds se pehle complete ho gaya → `history` mil jata hai.
  - Agar nahi hua → `TimeoutError` throw hota hai, jise catch karke friendly error dict return hoti hai.

Yeh **timeout** UI se tum slider se control karte ho.

### 6. Final Result Extract karna

```python
result_text = history.final_result() if hasattr(history, 'final_result') else str(history)
```

- Kai baar `history` ek aisa object hota hai jisme `final_result()` method hai
  - Yeh pure conversation / steps se **end wala summary text** nikal deta hai.
- Agar `final_result` method nahi mila:
  - To fallback: `str(history)` (pure object ko string bana ke use kar lo).

Yeh `result_text` usually woh text hota hai jisme:

- JSON block
- Ya human readable summary

donon ho sakte hain.

### 7. JSON Parse Helper

```python
parsed_result = self._parse_json_output(result_text)
```

Helper function:

```python
def _parse_json_output(self, output: str) -> Dict[str, Any]:
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        return {"raw_output": output, "parsed": False}
```

Flow:

1. **Direct JSON try**:
   - Agar pura output valid JSON hai → seedha `json.loads`.
2. Agar nahi:
   - Regex se pehla `{ ... }` block nikalne ki koshish:
     - `re.DOTALL` se multiline JSON bhi capture ho jata hai.
   - Us block pe `json.loads` try karta hai.
3. Phir bhi fail:
   - Fallback:  
     `{"raw_output": output, "parsed": False}`

Is se fayda:

- Agar LLM ne thoda extra text likh diya ho:
  - “Here is the data: { ...json... } Thanks!”
  - Tab bhi hum JSON portion nikal ke parse kar sakte hain.

### 8. Return Value

Success case:

```python
return {
    "success": True,
    "result": parsed_result,
    "raw_output": result_text
}
```

Error case:

```python
return {
    "success": False,
    "error": str(e),
    "message": "Failed to execute task"
}
```

Yeh dict `app.py` mein Streamlit UI ko jata hai, jo:

- `success` check karta hai
- `result` ko `st.json` se show karta hai
- `raw_output` ko expander mein debug ke liye dikhata hai.

---

## 🧱 Objects & “Markings” Tumne Jo Dekhe

Jab tumne tool run kiya tha aur:

- terminal output,
- agent history GIF,
- ya browser ke andar step highlights,

dekhe honge, woh sab **browser-use ka internal logging / visualization** part hai.

Conceptually kya ho raha hota hai:

1. **State tracking**:
   - Har page ke DOM ka snapshot + LLM ke liye text representation banti hai.
   - Important elements ko tags / indices diye ja sakte hain (jaise “element #3: button ‘Login’”).
2. **Step log**:
   - Agent har action ko store karta hai:
     - “Navigate to …”
     - “Click button X”
     - “Fill input Y with value Z”
3. **Visualization**:
   - Kuch tools / scripts history se GIF ya log generate kar dete hain (jaise `agent_history.gif`).
   - Isme har step par kis object/element ke saath interact hua, woh highlight hota hai.

Tumhara code `universal_browser_tool.py` directly yeh GIF nahi banata,  
lekin `browser-use` library ke andar:

- Agent ke behaviour ko record kiya jata hai,
- Aur optionally usse visualization generate hota hai (jo tumne project mein dekha).

Yeh sab isliye hota hai taaki:

- Developer ko samajh aaye LLM ne kya steps liye,
- Debug kar sakein:
  - Kahan pe wrong click hua
  - Kahan pe form galat fill hui
  - Kahan se DOM parse nahi ho paya, etc.

---

## ⚙️ How It Connects With `app.py`

`app.py` mein `show_universal_tool()` function:

- Sidebar se **model**, **proxy**, **timeout**, **headless** values leta hai.
- Form se **instruction** string leta hai.
- Fir:

```python
tool = UniversalBrowserTool(model=model)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.set_exception_handler(custom_exception_handler)
result = loop.run_until_complete(tool.execute_task(
    instruction=instruction.strip(),
    proxy_server=proxy_server or None,
    proxy_username=proxy_user or None,
    proxy_password=proxy_pass or None,
    timeout=timeout,
    headless=headless
))
loop.close()
```

Important points:

- Har Streamlit request ke liye **naya event loop** ban raha hai:
  - Windows async cleanup issues avoid karne ke liye.
- `custom_exception_handler` ko attach kiya gaya hai:
  - Taaki kuch noisy asyncio cleanup warnings ko swallow kiya ja sake.
- Result UI par:
  - `st.success` + `st.json(result["result"])`
  - Raw output expander mein `result["raw_output"]`.

---

## 🧠 Mental Model (Kaise Socho Isko)

Tum is tool ko aise imagine karo:

- **Layer 1 (UI)** – Streamlit forms:
  - Tum instructions / settings bhar rahe ho
- **Layer 2 (Orchestration)** – `UniversalBrowserTool.execute_task`:
  - Tumhari input ko task description + configs mein convert karta hai
  - Browser + Agent objects banata hai
  - Timeout/manage error handling karta hai
- **Layer 3 (Agent Brain)** – `browser_use.Agent`:
  - LLM se sochta hai:
    - “Next kya karna hai?”
    - “Kon sa element click karna hai?”
  - Har step ka state/history maintain karta hai
- **Layer 4 (Real Browser)** – Playwright / Chrome:
  - Actual clicks, typing, navigation real browser mein ho raha hai.

Iss mental model se tum easily:

- Proxy / headless change kar sakte ho,
- Task instructions ko tweak kar sakte ho,
- Ya future mein custom “specialized tools” bana sakte ho jo `UniversalBrowserTool` ke concept ko extend karein.

---

## 📌 Agar Aur Deep Jaana Ho

Agar tum isse bhi zyada deep jana chahte ho:

- `browser-use` ka source code explore karo:
  - `Agent` ka implementation
  - Browser abstraction
  - History / replay / GIF generation code
- LLM prompt design dekh ke:
  - Kaise instructions + DOM summary ko ek prompt mein merge kiya jata hai
  - Kaise next-step planning hoti hai.

Agar chaho to main next step mein:
- Agent ke prompt structure ka breakdown,
- Ya ek example “real run” ka **step-by-step log** (Step 1: navigate, Step 2: type, …)  
 bhi bana sakta hoon. Bas bolo kis level tak jaana hai.  

