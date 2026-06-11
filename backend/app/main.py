import asyncio
import json
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.database import init_db
from app.llm.deepseek import DeepSeekClient
from app.agent.agent_hub import AgentHub
from app.agent.react_agent import ReActAgent
from app.agent.subagent import create_builtin_subagents
from app.tools.recipe import init_recipe_tool, search_recipes
from app.tools.nutrition import analyze_nutrition, calculate_meal_calories
from app.tools.diet_plan import create_diet_plan, record_meal
from app.tools.web_search import web_search
from app.api.chat import router as chat_router, set_agent
from app.api.user import router as user_router
from app.api.image import router as image_router

def load_seed_recipes():
    recipes_path = os.path.join(os.path.dirname(__file__), "..", "data", "recipes.json")
    if os.path.exists(recipes_path):
        with open(recipes_path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    return []

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[start] Starting Private Kitchen Assistant...")
    await init_db()
    print("[ok] Database initialized")

    recipes = load_seed_recipes()
    init_recipe_tool(recipes)
    print(f"[ok] Loaded {len(recipes)} recipes")

    llm = DeepSeekClient()

    hub = AgentHub()
    hub.register_tool("search_recipes", search_recipes,
        "Search recipes by keywords (ingredients, name, tags)",
        {"type": "object", "properties": {
            "query": {"type": "string", "description": "Search keywords"},
            "top_k": {"type": "integer", "description": "Number of results"}
        }, "required": ["query"]})
    hub.register_tool("analyze_nutrition", analyze_nutrition,
        "Analyze nutrition of a food item",
        {"type": "object", "properties": {
            "food_name": {"type": "string", "description": "Food name"},
            "weight_g": {"type": "number", "description": "Weight in grams"}
        }, "required": ["food_name"]})
    hub.register_tool("calculate_meal_calories", calculate_meal_calories,
        "Calculate total calories for a meal",
        {"type": "object", "properties": {
            "foods": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "calories": {"type": "number"},
                        "protein": {"type": "number"},
                        "fat": {"type": "number"},
                        "carbs": {"type": "number"}
                    }
                },
                "description": "List of foods"
            }
        }, "required": ["foods"]})
    hub.register_tool("create_diet_plan", create_diet_plan,
        "Generate a diet plan based on goals",
        {"type": "object", "properties": {
            "goal": {"type": "string", "description": "Goal: loss/muscle/sugar/healthy"},
            "daily_calories": {"type": "integer", "description": "Daily target calories"},
            "days": {"type": "integer", "description": "Number of days"}
        }, "required": ["goal"]})
    hub.register_tool("record_meal", record_meal,
        "Record user meal",
        {"type": "object", "properties": {
            "foods": {"type": "array", "items": {"type": "string"}, "description": "List of foods"},
            "notes": {"type": "string", "description": "Notes"}
        }, "required": ["foods"]})
    hub.register_tool("web_search", web_search,
        "Search the web for recipes or nutrition info",
        {"type": "object", "properties": {
            "query": {"type": "string", "description": "Search query"}
        }, "required": ["query"]})

    subagents = create_builtin_subagents(llm)
    for sa in subagents:
        hub.register_subagent(sa)
    print("[ok] AgentHub initialized with tools and subagents")

    agent = ReActAgent(hub, llm)
    set_agent(agent)
    print("[ok] ReAct Agent ready")

    yield
    print("[bye] Private Kitchen Assistant stopped")

app = FastAPI(title="Private Kitchen Assistant", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(user_router)
app.include_router(image_router)

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "Private Kitchen Assistant"}

async def main():
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    asyncio.run(main())
