from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.database import get_db
from app.models.user import User

router = APIRouter(prefix="/api/user", tags=["user"])

class UserUpdate(BaseModel):
    name: str = "用户"
    goal: str = "健康饮食"
    weight: float | None = None
    height: float | None = None
    age: int | None = None
    diet_preference: str = ""
    allergies: str = ""
    long_term_instructions: str = ""

@router.get("/profile")
async def get_profile(user_id: int = 1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        # 创建默认用户
        user = User(id=user_id, name="用户")
        db.add(user)
        await db.commit()
    return {"id": user.id, "name": user.name, "goal": user.goal,
            "weight": user.weight, "height": user.height, "age": user.age,
            "diet_preference": user.diet_preference, "allergies": user.allergies,
            "long_term_instructions": user.long_term_instructions}

@router.put("/profile")
async def update_profile(data: UserUpdate, user_id: int = 1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        user = User(id=user_id)
        db.add(user)
    user.name = data.name
    user.goal = data.goal
    user.weight = data.weight
    user.height = data.height
    user.age = data.age
    user.diet_preference = data.diet_preference
    user.allergies = data.allergies
    user.long_term_instructions = data.long_term_instructions
    await db.commit()
    return {"status": "ok"}
