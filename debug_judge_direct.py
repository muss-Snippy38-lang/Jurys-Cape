import httpx
import asyncio
import sys

# The URL you registered for the Judge
# Replace this if you need to, but it reads from input
JUDGE_URL = "https://enoch-tented-tod.ngrok-free.dev"
SWARM_SECRET = "change-me-in-prod-secure-swarm-key"

async def debug_direct():
    print(f"=== DIRECT DEBUG: JUDGE NODE ===")
    print(f"Target: {JUDGE_URL}")
    
    payload = {
        "facts": ["Test Fact"],
        "evidence_summary": "Test Evidence",
        "legal_sections": ["Test Section"]
    }
    
    headers = {"X-Swarm-Secret": SWARM_SECRET}
    
    async with httpx.AsyncClient() as client:
        # 1. Test Root (Should be 404 Not Found usually, but connection succeeds)
        try:
            print("\n1. Pinging Root 'GET /' ...")
            resp = await client.get(f"{JUDGE_URL}/")
            print(f"   Result: {resp.status_code} (This confirms server is reachable)")
        except Exception as e:
            print(f"   [ERROR] Connection Failed: {e}")
            return

        # 2. Test Adjudicate
        print(f"\n2. Testing 'POST /adjudicate' ...")
        try:
            resp = await client.post(
                f"{JUDGE_URL}/adjudicate",
                json=payload,
                headers=headers
            )
            print(f"   Status: {resp.status_code}")
            print(f"   Body:   {resp.text}")
            
            if resp.status_code == 404:
                print("\n[DIAGNOSITC] 404 Not Found means the App is running but '/adjudicate' does not exist.")
                print("Did you perhaps register the 'Librarian' or 'Investigator' URL by mistake?")
                print("Please check which Notebook this URL belongs to in Google Colab.")
            elif resp.status_code == 200:
                print("\n[SUCCESS] The Node is working perfectly directly!")
                print("The issue must be in the local Orchestrator registration.")
                
        except Exception as e:
            print(f"   [ERROR] Request Failed: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(debug_direct())
