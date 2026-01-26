"""
Amazon Auto-Buyer Tool (LOCAL - FREE)
FIXED: Updated to latest browser-use API
"""

from langchain_openai import ChatOpenAI
from browser_use import Agent
from typing import Optional, Dict, Any
import asyncio
import json
import re
import os
from dotenv import load_dotenv
from browser_use.browser.browser import Browser, BrowserConfig

load_dotenv()


class AmazonAutoBuyer:
    """Tool for automating Amazon purchases using local browser-use"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the Amazon Auto-Buyer
        
        Args:
            model: LLM model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=0
        )
    
    async def purchase(
        self,
        email: str,
        password: str,
        product_url: str,
        quantity: int = 1,
        credit_card: Optional[str] = None,
        gift_card_code: Optional[str] = None,
        shipping_speed: str = "Standard"
    ) -> Dict[str, Any]:
        """
        Automate Amazon purchase process
        
        Args:
            email: Amazon account email
            password: Amazon account password
            product_url: Product URL or ASIN
            quantity: Number of items to purchase
            credit_card: Credit card information (last 4 digits)
            gift_card_code: Optional gift card code
            shipping_speed: Shipping speed preference
            
        Returns:
            Dictionary with success status and result details
        """
        try:
            # Construct the task description
            task_description = f"""
            I want to purchase a product from Amazon. Follow these steps:
            
            1. Go to {product_url}
            2. Login with:
               - Email: {email}
               - Password: {password}
            3. Add {quantity} item(s) to cart
            4. Go to checkout
            5. Select shipping speed: {shipping_speed}
            """
            
            if gift_card_code:
                task_description += f"\n6. Apply gift card: {gift_card_code}"
            
            if credit_card:
                task_description += f"\n7. Use card ending in: {credit_card[-4:]}"
            
            task_description += """
            
            ⚠️ CRITICAL: STOP before final "Place Order" button
            
            Extract and return as JSON:
            {
                "success": true,
                "product_title": "...",
                "order_total": "...",
                "delivery_date": "...",
                "status": "Ready for manual confirmation"
            }
            """
            
            # Create agent with headful browser
            browser = Browser(config=BrowserConfig(headless=False))
            agent = Agent(
                task=task_description,
                llm=self.llm,
                browser=browser
            )
            
            # Run agent
            history = await agent.run()
            
            # Extract final result
            result_text = history.final_result() if hasattr(history, 'final_result') else str(history)
            
            # Parse JSON from result
            parsed_result = self._parse_json_output(result_text)
            
            return {
                "success": True,
                "result": parsed_result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to complete purchase automation"
            }
    
    async def check_product_availability(self, product_url: str) -> Dict[str, Any]:
        """
        Check if a product is available and get its details
        
        Args:
            product_url: Product URL or ASIN
            
        Returns:
            Dictionary with product availability and details
        """
        try:
            task_description = f"""
            Go to: {product_url}
            
            Extract and return as JSON:
            {{
                "title": "product name",
                "price": "current price",
                "availability": "in stock / out of stock",
                "rating": "X.X stars",
                "reviews_count": "number"
            }}
            """
            
            # Create browser and agent
            browser = Browser(config=BrowserConfig(headless=False))
            agent = Agent(
                task=task_description,
                llm=self.llm,
                browser=browser
            )
            
            history = await agent.run()
            result_text = history.final_result() if hasattr(history, 'final_result') else str(history)
            product_info = self._parse_json_output(result_text)
            
            return {
                "success": True,
                "product_info": product_info
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
    
    # Initialize buyer
    # Initialize buyer
    buyer = AmazonAutoBuyer(
        # openai_api_key is now loaded from environment
        model="gpt-4o-mini"  # Cheapest option
    )
    
    # Example: Check product availability
    print("🔍 Checking product...")
    availability = await buyer.check_product_availability(
        product_url="https://www.amazon.in/dp/B0CX23V2ZK"
    )
    print(availability)


if __name__ == "__main__":
    asyncio.run(main())
