import asyncio
import pandas as pd
from inference import run
from env.grader import grade

async def evaluate():
    tasks = ["easy", "medium", "hard"]
    
    print("🚀 Starting Evaluation...\n")
    
    for task in tasks:
        print(f"--- Evaluating Task: {task.upper()} ---")
        try:
            # Re-run inference workflow so the LLM cleans it
            from env.environment import DataCleaningEnv
            from inference import get_action_from_llm
            
            # Use on_bad_lines='skip' for potentially broken datasets in raw
            env = DataCleaningEnv(task)
            
            # Since reset reads from raw_..., intercept it and use resilient parsing
            import pandas as pd
            raw_df = pd.read_csv(f"data/raw_{task}.csv", on_bad_lines='skip', engine='python')
            env.df = raw_df
            env.steps = 0
            obs = env.state()
            
            done = False
            while not done:
                action = await get_action_from_llm(obs)
                print(f"Action taken: {action.action_type} on {action.column} with {action.value}")
                obs, reward, done, info = await env.step(action)
                
            output_df = env.df
            expected_df = pd.read_csv(f"data/expected_{task}.csv", on_bad_lines='skip', engine='python')
            
            from env.grader import grade
            score = grade(output_df, expected_df)
            print(f"✅ Score for {task.upper()}: {score:.2%} ({score})")
            
        except Exception as e:
            print(f"❌ Error evaluating {task.upper()}: {e}")
            
        print("\n")

if __name__ == "__main__":
    asyncio.run(evaluate())
