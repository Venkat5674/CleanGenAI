import asyncio
import re
from env.environment import DataCleaningEnv
from env.actions import Action
from openai import AsyncOpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

async def get_action_from_llm(obs):
    try:
        # Initialize client inside the function to avoid crashing on import when the API key is missing
        api_key = os.environ.get("API_KEY", os.environ.get("GROQ_API_KEY", "dummy_key_to_prevent_crash_during_validation"))
        base_url = os.environ.get("API_BASE_URL", "https://api.groq.com/openai/v1") # Fallback to Groq's OpenAI-compatible endpoint
        
        client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    except Exception as e:
        print(f"Failed to initialize OpenAI client: {e}")
        return Action(action_type="stop_cleaning")
        
    prompt = f"""
You are a data cleaning agent.

Observation:
{obs.model_dump_json()}
{(f"Error from previous action: {error}" if 'error' in globals() else "")}

Choose next action in JSON. YOU MUST RESPOND WITH ONLY VALID JSON. NO MARKDOWN, NO EXPLANATIONS, AND NO OTHER TEXT. 

The ONLY valid action_types are:
1. "remove_duplicates" 
2. "convert_date" (require "column") Use if date formats are inconsistent (e.g. YYYY/MM/DD vs MM-DD-YYYY).
3. "fill_nulls" (requires "column" and "value") Use for numeric/text nulls. Do NOT use for date columns.
4. "drop_column"
5. "drop_row"
6. "stop_cleaning" (If the only remaining inconsistencies are nulls in date columns, you MUST call stop_cleaning immediately.)

Example:
{{"action_type": "convert_date", "column": "date"}}
"""

    try:
        response = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        text = response.choices[0].message.content
        
        # Try to extract JSON using regex in case LLM is chatty
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group(0)

        action_dict = json.loads(text)
        return Action(**action_dict)
    except Exception as e:
        print(f"Error during LLM network call or parsing: {e}")
        return Action(action_type="stop_cleaning")


async def run(task: str = "easy"):
    env = DataCleaningEnv(task)
    obs = await env.reset()

    done = False
    print("[START]")

    while not done:
        action = await get_action_from_llm(obs)
        print(f"[ACTION] {action}")

        obs, reward, done, info = await env.step(action)
        print(f"[REWARD] {reward}")

    print(f"[END] Final Reward: {reward}")


if __name__ == "__main__":
    asyncio.run(run("easy"))
