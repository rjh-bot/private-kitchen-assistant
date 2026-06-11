"""ReAct Agent: 推理→工具调用→结果整合 自主闭环"""
import json
import asyncio
from typing import AsyncGenerator
from app.llm.deepseek import DeepSeekClient
from app.agent.agent_hub import AgentHub

class ReActAgent:
    SYSTEM_PROMPT = """你是私人厨房助理，一个智能饮食管理助手。

你可以使用以下工具来帮助用户：
1. **search_recipes** - 搜索菜谱，支持按食材/菜名/标签查询
2. **analyze_nutrition** - 分析食物营养成分
3. **create_diet_plan** - 制定饮食计划
4. **record_meal** - 记录饮食
5. **calculate_meal_calories** - 计算餐食热量
6. **web_search** - 联网搜索

工作流程：
1. 分析用户意图，决定是否需要调用工具
2. 如果需要工具，一次调用一个，等待结果
3. 根据工具结果给出自然语言回复
4. 如果不需要工具，直接回复

注意：务必用中文回复，给出清晰、实用的建议。
"""

    def __init__(self, hub: AgentHub, llm: DeepSeekClient):
        self.hub = hub
        self.llm = llm

    async def stream_run(self, user_message: str, user_profile: dict = None) -> AsyncGenerator[str, None]:
        messages = [{"role": "system", "content": self._build_system_prompt(user_profile)}]
        messages.append({"role": "user", "content": user_message})

        max_iterations = 5
        for iteration in range(max_iterations):
            yield f"【思考中...】\n"

            response = await self.llm.chat_with_tools(messages, self.hub.get_all_tool_schemas())
            choice = response["choices"][0]
            msg = choice["message"]

            if not msg.get("tool_calls"):
                content = msg.get("content", "")
                if content:
                    # 直接回复
                    yield content
                else:
                    # 尝试获取 assistant 消息的 content
                    messages.append({"role": "assistant", "content": ""})
                    response2 = await self.llm.chat(messages)
                    yield response2
                return

            messages.append({"role": "assistant", "content": msg.get("content") or "",
                             "tool_calls": msg["tool_calls"]})

            for tc in msg["tool_calls"]:
                func_name = tc["function"]["name"]
                try:
                    args = json.loads(tc["function"]["arguments"])
                except json.JSONDecodeError:
                    args = {}

                yield f"🔧 调用工具: {func_name}\n参数: {json.dumps(args, ensure_ascii=False)}\n\n"

                result = await self.hub.execute(func_name, **args)
                yield f"📎 工具结果:\n{result}\n\n"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": result
                })

            if iteration == max_iterations - 1:
                final = await self.llm.chat(messages)
                yield str(final)

    def _build_system_prompt(self, profile: dict = None) -> str:
        prompt = self.SYSTEM_PROMPT
        if profile:
            extra = []
            if profile.get("goal"):
                extra.append(f"用户当前目标: {profile['goal']}")
            if profile.get("diet_preference"):
                extra.append(f"饮食偏好: {profile['diet_preference']}")
            if profile.get("allergies"):
                extra.append(f"过敏原: {profile['allergies']}")
            if profile.get("long_term_instructions"):
                extra.append(f"长期指令: {profile['long_term_instructions']}")
            if profile.get("weight"):
                extra.append(f"体重: {profile['weight']}kg")
            if extra:
                prompt += "\n\n**用户信息**:\n" + "\n".join(extra)
        return prompt

    async def simple_run(self, user_message: str, user_profile: dict = None) -> str:
        """非流式调用"""
        result_parts = []
        async for part in self.stream_run(user_message, user_profile):
            if not part.startswith("【") and not part.startswith("🔧") and not part.startswith("📎"):
                result_parts.append(part)
        return "".join(result_parts)
