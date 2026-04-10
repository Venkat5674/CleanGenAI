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
        api_key = os.environ.get("HF_TOKEN", os.environ.get("API_KEY", os.environ.get("GROQ_API_KEY", "dummy_key_to_prevent_crash_during_validation")))
        base_url = os.environ.get("API_BASE_URL", "https://api.groq.com/openai/v1") # Fallback to Groq's OpenAI-compatible endpoint
        model_name = os.environ.get("MODEL_NAME", "llama-3.1-8b-instant")
        
        async with AsyncOpenAI(api_key=api_key, base_url=base_url) as client:
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

            response = await client.chat.completions.create(
                model=model_name,
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
        # We must not raise to avoid breaking the script execution
        return Action(action_type="stop_cleaning")


async def run(task: str = "easy"):
    env = DataCleaningEnv(task)
    obs = await env.reset()

    done = False
    model_name = os.environ.get("MODEL_NAME", "llama-3.1-8b-instant")
    print(f"[START] task={task} env=data-cleaning-env model={model_name}", flush=True)

    step = 0
    rewards = []
    
    while not done:
        step += 1
        action = await get_action_from_llm(obs)

        obs, reward, done, info = await env.step(action)
        
        rewards.append(reward)
        error_val = info.get('error', None) if info else None
        
        action_str = f"{action.action_type}"
        if action.column: action_str += f"('{action.column}')"
        if action.value: action_str += f"='{action.value}'"
            
        print(f"[STEP] step={step} action={action_str} reward={reward:.2f} done={str(done).lower()} error={error_val if error_val else 'null'}", flush=True)

    score = reward
    score = min(max(score, 0.0), 1.0)
    success = score >= 0.5
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={step} score={score:.2f} rewards={rewards_str}", flush=True)


if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        asyncio.run(run(task))
