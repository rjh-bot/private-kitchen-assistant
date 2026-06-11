"""Subagent 专家框架 - 内置子代理"""
from app.llm.deepseek import DeepSeekClient

class SubAgent:
    def __init__(self, name: str, description: str, prompt: str, llm: DeepSeekClient):
        self.name = name
        self.description = description
        self.prompt = prompt
        self.llm = llm

    async def run(self, query: str) -> str:
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": query}
        ]
        return await self.llm.chat(messages)

def create_builtin_subagents(llm: DeepSeekClient) -> list[SubAgent]:
    return [
        SubAgent(
            name="营养师",
            description="专业的营养分析建议，擅长计算热量与制定饮食方案",
            prompt="""你是专业营养师。请根据用户提供的信息给出专业营养分析建议。
包含以下方面：
1. 食物/食谱的营养评估
2. 针对用户目标(减脂/增肌/控糖)的饮食建议
3. 食物替换或改良方案
请用中文回复，给出具体可执行的建议。""",
            llm=llm
        ),
        SubAgent(
            name="烹饪顾问",
            description="烹饪技巧指导与菜谱推荐",
            prompt="""你是经验丰富的烹饪顾问。擅长：
1. 推荐适合用户水平的菜谱
2. 指导烹饪技巧和方法
3. 提供食材搭配和替代建议
4. 节省时间的烹饪窍门
请用中文给出详细指导。""",
            llm=llm
        )
    ]
