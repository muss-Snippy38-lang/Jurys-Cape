import asyncio
import httpx
import sys

# Configuration
API_URL = "http://localhost:8000/api/v1"

async def register_mock_node():
    """Registers a 'fake' node to test the registration endpoint."""
    print("1. Registering Mock Node...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_URL}/swarm/register",
                json={"role": "test-node", "url": "https://mock-ngrok.com"}
            )
            print(f"   Response: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"   FAILED: {e}")
            return False
    return True

async def list_nodes():
    """Lists all registered nodes."""
    print("\n2. Listing Nodes...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_URL}/swarm/nodes")
            print(f"   Nodes: {response.json()}")
        except Exception as e:
            print(f"   FAILED: {e}")

async def main():
    print("=== JURIS-CAPE SWARM VERIFICATION ===")
    print(f"Targeting Local API: {API_URL}")
    
    # 1. Health Check
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get("http://localhost:8000/api/v1/")
            if resp.status_code == 200:
                print("   [OK] Server is Online")
            else:
                print(f"   [ERR] Server returned {resp.status_code}")
                sys.exit(1)
        except Exception:
            print("   [ERR] Could not connect to localhost:8000. Is the server running?")
            sys.exit(1)

    # 2. Register
    if await register_mock_node():
        # 3. List
        await list_nodes()
        
    print("\n=== VERIFICATION COMPLETE ===")
    print("To test actual Colab nodes, you must start the Colab notebook and register the REAL Ngrok URL.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
