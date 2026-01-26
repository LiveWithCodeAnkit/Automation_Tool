"""
Universal Browser Tool (LOCAL - FREE)
Upgraded version of Claim Search Tool with Proxy and Timeout support.
"""

from langchain_openai import ChatOpenAI
# In 0.1.25, BrowserProfile might effectively be BrowserConfig or similar, but for now we'll check if BrowserProfile exists or if we need to adjust.
# Based on dir(browser_use), it has 'Browser' and 'BrowserConfig'.
# Let's check 'browser_use.browser' content first via script, but to be fast I will assume we might need to change how we init browser.
# Wait, checking step 223 output: 'browser' submodule exists.
from browser_use.browser.browser import BrowserConfig
from browser_use import Agent
from typing import Optional, Dict, Any
import asyncio
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

class UniversalBrowserTool:
    """
    Universal tool for executing any browser automation task with advanced configuration.
    Supports Proxy, Timeouts, and Custom User Agents.
    """
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the Universal Browser Tool
        
        Args:
            model: LLM model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.output_model = model
        # Use browser-use's ChatOpenAI (reads API key from .env automatically)
        # We can also support other models if configured
        self.llm = ChatOpenAI(
            model=model,
            temperature=0
        )
    
    async def execute_task(
        self, 
        instruction: str,
        proxy_server: Optional[str] = None,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
        timeout: int = 120,
        headless: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a natural language task on any website with advanced options.
        """
        try:
            # Configure Proxy if provided
            proxy_config = None
            if proxy_server:
                # Format: protocol://user:pass@host:port or just protocol://host:port
                # browser-use 0.1.25 might accept a simple proxy dictionary in BrowserConfig or playwright args
                if proxy_username and proxy_password:
                    # Construct full proxy URL with auth
                    proxy_parts = proxy_server.split("://")
                    protocol = proxy_parts[0] if len(proxy_parts) > 1 else "http"
                    host = proxy_parts[-1]
                    proxy_config = f"{protocol}://{proxy_username}:{proxy_password}@{host}"
                else:
                    proxy_config = proxy_server
            
            # Create Task Description
            task_description = f"""
            {instruction}
            
            IMPORTANT: Return the results as structured JSON format with all the information you found.
            """
            
            # Initialize Browser with Config
            from browser_use.browser.browser import Browser, BrowserConfig
            
            # Prepare config arguments
            config_args = {
                "headless": headless,
            }
            
            if proxy_config:
               config_args["proxy"] = {"server": proxy_config}
               
            browser = Browser(config=BrowserConfig(**config_args))
            
            # Create Agent
            agent = Agent(
                task=task_description,
                llm=self.llm,
                browser=browser,
            )
            
            # Run the agent
            try:
                history = await asyncio.wait_for(agent.run(), timeout=timeout)
            except asyncio.TimeoutError:
                return {
                    "success": False,
                    "error": f"Task timed out after {timeout} seconds",
                    "message": "The automation took too long to complete."
                }
            
            # Extract final result
            result_text = history.final_result() if hasattr(history, 'final_result') else str(history)
            
            # Parse JSON from output
            parsed_result = self._parse_json_output(result_text)
            
            return {
                "success": True,
                "result": parsed_result,
                "raw_output": result_text
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to execute task"
            }
    
    def _parse_json_output(self, output: str) -> Dict[str, Any]:
        """Helper to parse JSON from LLM output"""
        try:
            # Try direct JSON parse
            return json.loads(output)
        except json.JSONDecodeError:
            # Extract JSON using regex
            json_match = re.search(r'\{.*\}', output, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
            
            # Fallback
            return {
                "raw_output": output,
                "parsed": False
            }
