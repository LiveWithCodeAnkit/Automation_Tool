"""
Claim Search Tool (LOCAL - FREE)
FIXED: Updated to latest browser-use API
"""

from browser_use.llm.openai.chat import ChatOpenAI
from browser_use import Agent
from browser_use.browser.profile import BrowserProfile
from typing import Optional, Dict, Any, List
import asyncio
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()


class ClaimSearchTool:
    """Tool for automating claim searches on websites using local browser-use"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the Claim Search Tool
        
        Args:
            model: LLM model to use (default: gpt-4o-mini for cost efficiency)
        """
        # Use browser-use's ChatOpenAI (reads API key from .env automatically)
        self.llm = ChatOpenAI(
            model=model,
            temperature=0
        )
    
    async def execute_task(self, instruction: str) -> Dict[str, Any]:
        """
        Execute a natural language task on any website
        
        Args:
            instruction: Natural language instruction describing what to do
                        Example: "Go to https://example.com, login with email test@test.com and password test123, 
                                 then search for all claims from 2024 and return them as JSON"
            
        Returns:
            Dictionary with task results
        """
        try:
            # Use the instruction directly as task description
            task_description = f"""
            {instruction}
            
            IMPORTANT: Return the results as structured JSON format with all the information you found.
            If you're searching for claims, return them in this format:
            {{
                "success": true,
                "claims": [
                    {{
                        "id": "...",
                        "status": "...",
                        "date": "...",
                        "amount": "...",
                        "description": "..."
                    }}
                ],
                "total_found": ...
            }}
            
            If it's a different task, return the results in a clear JSON structure.
            """
            
            # Create agent with headful browser (reduces bot detection)
            agent = Agent(
                task=task_description,
                llm=self.llm,
                browser_profile=BrowserProfile(headless=False)
            )
            
            # Run the agent
            history = await agent.run()
            
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
    
    async def search_claims(
        self,
        website_url: str,
        username: str,
        password: str,
        search_query: str,
        claim_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        login_url: Optional[str] = None,
        wait_time: int = 10
    ) -> Dict[str, Any]:
        """
        Login to website and search for claims (Legacy method - use execute_task for flexibility)
        
        Args:
            website_url: Main website URL
            username: Login username/email
            password: Login password
            search_query: What to search for
            claim_id: Optional specific claim ID to search
            date_from: Optional start date (YYYY-MM-DD)
            date_to: Optional end date (YYYY-MM-DD)
            login_url: Optional specific login page URL
            wait_time: Wait time in seconds for page loads
            
        Returns:
            Dictionary with search results
        """
        try:
            # Construct the task description
            login_page = login_url if login_url else f"{website_url}/login"
            
            task_description = f"""
            I need to login to a website and search for claims. Follow these steps:
            
            1. Navigate to the login page: {login_page}
            2. Login with username: {username} and password: {password}
            3. Wait {wait_time} seconds for the page to fully load
            4. Navigate to the claims/search section
            """
            
            if claim_id:
                task_description += f"\n5. Search for claim with ID: {claim_id}"
            else:
                task_description += f"\n5. Search for: {search_query}"
            
            if date_from and date_to:
                task_description += f"\n6. Filter results from {date_from} to {date_to}"
            elif date_from:
                task_description += f"\n6. Filter results from {date_from}"
            elif date_to:
                task_description += f"\n6. Filter results until {date_to}"
            
            task_description += """
            7. Extract all found claims with the following information:
               - Claim ID
               - Claim status
               - Date submitted
               - Amount (if available)
               - Description/Details
               - Any other relevant information
            
            8. Return the results as structured JSON:
            {
                "success": true,
                "claims": [
                    {
                        "id": "...",
                        "status": "...",
                        "date": "...",
                        "amount": "...",
                        "description": "..."
                    }
                ],
                "total_found": ...
            }
            """
            
            # Create agent with headful browser (reduces bot detection)
            agent = Agent(
                task=task_description,
                llm=self.llm,
                browser_profile=BrowserProfile(headless=False)
            )
            
            # Run the agent
            history = await agent.run()
            
            # Extract final result
            result_text = history.final_result() if hasattr(history, 'final_result') else str(history)
            
            # Parse JSON from output
            parsed_result = self._parse_json_output(result_text)
            
            # Ensure claims is a list
            if "claims" not in parsed_result:
                parsed_result["claims"] = []
            if "total_found" not in parsed_result:
                parsed_result["total_found"] = len(parsed_result.get("claims", []))
            
            return {
                "success": True,
                **parsed_result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "claims": [],
                "total_found": 0,
                "message": "Failed to search for claims"
            }
    
    async def get_claim_details(
        self,
        website_url: str,
        username: str,
        password: str,
        claim_id: str,
        login_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific claim
        
        Args:
            website_url: Main website URL
            username: Login username/email
            password: Login password
            claim_id: Specific claim ID to retrieve
            login_url: Optional specific login page URL
            
        Returns:
            Dictionary with claim details
        """
        try:
            login_page = login_url if login_url else f"{website_url}/login"
            
            task_description = f"""
            Login to {login_page} with username: {username} and password: {password}
            Navigate to claim details page for claim ID: {claim_id}
            Extract all available information about this claim including:
            - Full claim details
            - Status history
            - Documents/files (if visible)
            - Communication history (if visible)
            - Payment information (if visible)
            - Next steps or actions required
            
            Return as structured JSON with all available fields.
            """
            
            agent = Agent(
                task=task_description,
                llm=self.llm,
                browser_profile=BrowserProfile(headless=False)
            )
            
            history = await agent.run()
            result_text = history.final_result() if hasattr(history, 'final_result') else str(history)
            
            claim_details = self._parse_json_output(result_text)
            
            return {
                "success": True,
                "claim_details": claim_details
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
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


# ========================================
# USAGE EXAMPLE
# ========================================

async def main():
    """Example usage"""
    
    # Initialize claim search tool
    tool = ClaimSearchTool(
        model="gpt-4o-mini"  # Cheapest option
    )
    
    # Example: Search for claims
    print("🔍 Searching for claims...")
    result = await tool.search_claims(
        website_url="https://example.com",
        username="your-username",
        password="your-password",
        search_query="insurance claims",
        date_from="2024-01-01",
        date_to="2024-12-31"
    )
    print(result)
    
    # Example: Get specific claim details
    if result.get("success") and result.get("claims"):
        claim_id = result["claims"][0].get("id")
        if claim_id:
            print(f"\n📋 Getting details for claim: {claim_id}")
            details = await tool.get_claim_details(
                website_url="https://example.com",
                username="your-username",
                password="your-password",
                claim_id=claim_id
            )
            print(details)


if __name__ == "__main__":
    asyncio.run(main())