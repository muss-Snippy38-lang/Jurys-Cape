import httpx
import asyncio
import sys

# The URL in question
TARGET_URL = "https://enoch-tented-tod.ngrok-free.dev"
SWARM_SECRET = "change-me-in-prod-secure-swarm-key"

async def identify_node():
    print(f"=== NODE IDENTITY PROBE ===")
    print(f"Targeting: {TARGET_URL}")
    print("------------------------------------------------")
    
    endpoints = {
        "Librarian": "/ocr",
        "Investigator": "/analyze_media",
        "Judge": "/adjudicate"
    }
    
    headers = {"X-Swarm-Secret": SWARM_SECRET, "Content-Type": "application/json"}
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for role, endpoint in endpoints.items():
            print(f"Probing for {role} ({endpoint})...", end=" ")
            try:
                # We send a dummy payload. 
                # If we get 422 (Validation Error), the endpoint EXISTS (Success).
                # If we get 404, it DOES NOT exist.
                resp = await client.post(f"{TARGET_URL}{endpoint}", json={}, headers=headers)
                
                if resp.status_code != 404:
                    print(f"FOUND! (Status: {resp.status_code})")
                    print(f"\n[CONCLUSION] This is the **{role}** node.")
                    return
                else:
                    print("No (404)")
            except Exception as e:
                print(f"Error: {e}")

    print("\n[CONCLUSION] Unknown Node. None of the expected endpoints exist.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(identify_node())
