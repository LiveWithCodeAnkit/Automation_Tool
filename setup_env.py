"""
Setup script to create .env file from template
Run this script to set up your environment variables
"""

import os

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    env_example = ".env.example"
    
    if os.path.exists(env_file):
        print(f"✅ {env_file} already exists!")
        return
    
    # Create .env.example content
    env_content = """# Browser Use Cloud API Key
# Get your API key from: https://cloud.browser-use.com
BROWSER_USE_API_KEY=bu_your_api_key_here
"""
    
    # Write .env.example
    with open(env_example, "w") as f:
        f.write(env_content)
    print(f"✅ Created {env_example}")
    
    # Create .env from example
    with open(env_file, "w") as f:
        f.write(env_content)
    print(f"✅ Created {env_file}")
    print("\n⚠️  Please edit .env file and add your actual API key!")
    print("   Get your API key from: https://cloud.browser-use.com")

if __name__ == "__main__":
    create_env_file()
