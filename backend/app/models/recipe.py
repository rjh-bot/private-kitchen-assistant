from sqlalchemy import Column, Integer, String, Text, Float
from app.models.database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    ingredients = Column(Text)        # JSON: {"食材": "用量"}
    steps = Column(Text)              # JSON 数组
    calories = Column(Float)          # 千卡
    protein = Column(Float)           # 蛋白质(g)
    fat = Column(Float)               # 脂肪(g)
    carbs = Column(Float)             # 碳水(g)
    tags = Column(String(500))        # 标签，逗号分隔
    description = Column(Text)
