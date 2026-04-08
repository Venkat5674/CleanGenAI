from fastapi import FastAPI, Request
from env.environment import DataCleaningEnv
from env.actions import Action
import uvicorn

app = FastAPI(title="AI Data Cleaner API for OpenEnv Grader")

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == '__main__':
    main()

current_env = None

@app.post("/reset")
async def reset_env(request: Request):
    global current_env
    try:
        body = await request.json()
        task = body.get("task", "easy")
    except:
        task = "easy"
        
    current_env = DataCleaningEnv(task=task)
    obs = await current_env.reset()
    
    # Clean NaNs out of the preview for JSON compliance
    return _clean_nan(obs.dict())

def _clean_nan(obj):
    import math
    if isinstance(obj, dict):
        return {k: _clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_clean_nan(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj

@app.post("/step")
async def step_env(request: Request):
    global current_env
    try:
        body = await request.json()
        action_data = body.get("action", body)
        action = Action(**action_data)
    except:
        return {"error": "Invalid action payload"}

    if current_env is None:
        current_env = DataCleaningEnv(task="easy")
        await current_env.reset()
        
    obs, reward, done, info = await current_env.step(action)
    
    # We must substitute NaNs so JSON encoding doesn't break.
    return {
        "observation": _clean_nan(obs.dict()),
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/")
def read_root():
    return {"status": "ok", "message": "OpenEnv API running successfully"}
