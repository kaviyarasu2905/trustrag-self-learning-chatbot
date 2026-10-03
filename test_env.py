from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("✅ .env file loaded successfully!")
    print(f"✅ API Key found: {api_key[:20]}...")
else:
    print("❌ ERROR: OPENAI_API_KEY not found in .env")
    print("Please check:")
    print("1. .env file exists in root folder")
    print("2. File contains: OPENAI_API_KEY=sk-...")
    print("3. No extra spaces or quotes")
