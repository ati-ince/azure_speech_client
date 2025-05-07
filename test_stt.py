import asyncio
from client_azure_stt_class import AzureSTTClient

if __name__ == "__main__":
    # Create a single client instance
    client = AzureSTTClient()
    
    try:
        # First run with 10 seconds timeout
        print("\n=== Starting first run (10 seconds) ===")
        asyncio.run(client.run(timeout=10))
        
        # Sleep for 2 seconds between runs
        print("\nSleeping for 2 seconds...")
        asyncio.run(asyncio.sleep(2))
        
        # Second run with 15 seconds timeout
        print("\n=== Starting second run (15 seconds) ===")
        asyncio.run(client.run(timeout=15))
        
    except KeyboardInterrupt:
        print("\nStopped by user")  