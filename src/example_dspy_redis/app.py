import os
import asyncio
from dotenv import load_dotenv
from example_dspy_redis.dspy_extractor import DSPyExtractor
from example_dspy_redis.redis_client import RedisClient

load_dotenv()

class AsyncDspyRedis:
    def __init__(self):
        REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
        REDIS_DB = int(os.getenv("REDIS_DB", 0))
        self.redis_client = RedisClient(REDIS_HOST, REDIS_PORT, db=REDIS_DB)
        OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
        OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
        OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "dspy-ollama")
        self.extractor = DSPyExtractor(OLLAMA_MODEL, OLLAMA_API_BASE, OLLAMA_API_KEY)

    async def listen(self):
        
        await self.redis_client.r.ping()
        print("Connected to Redis server.")
        await self.redis_client.subscribe("ie_request", self.handle_query)

        
    async def handle_query(self, query: str):
        print(f"Received query: {query}")
        response = await self.extractor.extract_info(query)
        await self.redis_client.publish("ie_response", str(response))
        print(f"Published response to channel ie_response: {response}")

    async def close(self):
        await self.redis_client.close()

def main():
    app = AsyncDspyRedis()
    try:
        asyncio.run(app.listen())
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        asyncio.run(app.close())

if __name__ == "__main__":
    main()
