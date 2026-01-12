import httpx
import asyncio
import sys

# Configuration
API_URL = "http://localhost:8000/api/v1"

async def test_librarian():
    print("=== TESTING LIBRARIAN NODE DISPATCH ===")
    
    # Payload matching the Librarian Notebook's expected input
    payload = {
        "file_url": "https://example.com/sample_contract.pdf"
    }
    
    print("1. Sending OCR Task to Orchestrator (Localhost)...")
    print(f"   Target: {API_URL}/swarm/dispatch/librarian")

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # We hit the 'dispatch' endpoint with task_endpoint='/ocr'
            response = await client.post(
                f"{API_URL}/swarm/dispatch/librarian", 
                params={"task_endpoint": "/ocr"},
                json=payload
            )
            
            if response.status_code == 200:
                print("\n[SUCCESS] Librarian Returned Result!")
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
    asyncio.run(test_librarian())
