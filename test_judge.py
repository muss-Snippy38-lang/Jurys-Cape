import httpx
import asyncio
import sys

# Configuration
API_URL = "http://localhost:8000/api/v1"

async def test_judge():
    print("=== TESTING JUDGE NODE DISPATCH ===")
    
    # Payload matching the Judge Notebook's expected input
    payload = {
        "facts": [
            "Suspect was seen entering the building at 10:00 PM.",
            "Surveillance footage shows Suspect carrying a crowbar.",
            "Window was broken at 10:05 PM."
        ],
        "evidence_summary": "Video footage and witness testimony match.",
        "legal_sections": ["Section 305 (BNS) - Theft", "Section 303 (BNS) - Break and Enter"]
    }
    
    print("1. Sending Case to Orchestrator (Localhost)...")
    print(f"   Target: {API_URL}/swarm/dispatch/judge")
    print("   ... Orchestrator will forward to Colab Judge (Ngrok) ...")

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # We hit the 'dispatch' endpoint. 
            # 'task_endpoint' param tells the worker node which internal route to use (e.g. /adjudicate)
            response = await client.post(
                f"{API_URL}/swarm/dispatch/judge", 
                params={"task_endpoint": "/adjudicate"},
                json=payload
            )
            
            if response.status_code == 200:
                print("\n[SUCCESS] Judge Returned Verdict!")
                print("------------------------------------------------")
                print(response.json())
                print("------------------------------------------------")
            else:
                print(f"\n[ERROR] Dispatch Failed: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"\n[ERROR] Request Failed: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_judge())
