import sys
import uvicorn

if __name__ == "__main__":
    print("Initializing FoodGuard Server on port 8000...", flush=True)
    config = uvicorn.Config("backend.app.main:app", host="127.0.0.1", port=8000, log_level="info", loop="asyncio")
    server = uvicorn.Server(config)
    server.run()
