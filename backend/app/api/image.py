from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import base64, io

from app.models.database import get_db
from app.llm.deepseek import DeepSeekClient

router = APIRouter(prefix="/api/image", tags=["image"])

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件")
    contents = await file.read()
    base64_str = base64.b64encode(contents).decode("utf-8")

    llm = DeepSeekClient()
    result = await llm.vision_analyze(base64_str, "请识别图中的食材或菜品，并估算其营养成分（热量、蛋白质、脂肪、碳水）。如果有多种食材，请分别列出。")
    return {"result": result}
