import asyncio
from env.environment import DataCleaningEnv

async def main():
    env = DataCleaningEnv()
    obs = await env.reset()
    print(obs.model_dump() if hasattr(obs, "model_dump") else obs.dict())

asyncio.run(main())
