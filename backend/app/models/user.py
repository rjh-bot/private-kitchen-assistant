from sqlalchemy import Column, Integer, String, Text, Float
from app.models.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), default="用户")
    goal = Column(String(100), default="健康饮食")  # 减脂/增肌/控糖/健康饮食
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    age = Column(Integer, nullable=True)
    diet_preference = Column(String(200), default="")  # 饮食偏好
    allergies = Column(String(200), default="")       # 过敏原
    long_term_instructions = Column(Text, default="") # 长期饮食指令
