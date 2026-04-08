from fastapi import FastAPI, Request
from env.environment import DataCleaningEnv
from env.actions import Action

app = FastAPI(title="AI Data Cleaner API for OpenEnv Grader")
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
    return obs.dict()

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
    
    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/")
def read_root():
    return {"status": "ok", "message": "OpenEnv API running successfully"}
