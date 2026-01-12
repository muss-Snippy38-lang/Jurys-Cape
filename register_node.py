import httpx
import asyncio
import sys

# Configuration
API_URL = "http://localhost:8000/api/v1"

async def register_node():
    print("=== JURIS-CAPE NODE REGISTRATION ===")
    print("Ensure your local server is running (uvicorn app.main:app --reload)")
    print("---------------------------------------------------------------")
    
    # 1. Get Inputs
    role = input("Enter Node Role (librarian / investigator / judge): ").strip().lower()
    if role not in ["librarian", "investigator", "judge"]:
        print("Invalid role! specific 'librarian', 'investigator', or 'judge'.")
        return

    url = input("Enter the Ngrok URL (e.g., https://xxxx.ngrok-free.dev): ").strip()
    if not url.startswith("http"):
        print("Invalid URL! Must start with http or https.")
        return

    # 2. Send Request
    print(f"\nRegistering '{role}' at '{url}'...")
    
    async with httpx.AsyncClient() as client:
        try:
            # First check if local server is up
            try:
                await client.get(f"{API_URL}/")
            except Exception:
                print(f"[ERROR] Could not connect to {API_URL}. Is your local server running?")
                return

            # Register
            payload = {"role": role, "url": url}
            response = await client.post(f"{API_URL}/swarm/register", json=payload)
            
            if response.status_code == 200:
                print(f"\n[SUCCESS] Node Registered Successfully!")
                print(f"Response: {response.json()}")
            else:
                print(f"\n[ERROR] Registration Failed: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"\n[ERROR] Request Failed: {e}")

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(register_node())
    except KeyboardInterrupt:
        pass
