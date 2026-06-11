"""AgentHub: 统一管理 Agent、Tool 与 Provider"""
import asyncio
from typing import Callable, Any

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, dict] = {}

    def register(self, name: str, func: Callable, description: str, parameters: dict):
        self._tools[name] = {
            "func": func,
            "description": description,
            "parameters": parameters,
            "openai_schema": {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters
                }
            }
        }

    def get_schemas(self) -> list[dict]:
        return [t["openai_schema"] for t in self._tools.values()]

    async def execute(self, name: str, **kwargs) -> str:
        tool = self._tools.get(name)
        if not tool:
            return f"错误: 未找到工具 {name}"
        func = tool["func"]
        if asyncio.iscoroutinefunction(func):
            return await func(**kwargs)
        return func(**kwargs)

class AgentHub:
    """管理所有 Agent 和工具注册"""
    def __init__(self):
        self.tools = ToolRegistry()
        self.subagents: dict[str, "SubAgent"] = {}

    def register_tool(self, name: str, func: Callable, description: str, parameters: dict):
        self.tools.register(name, func, description, parameters)

    def register_subagent(self, agent: "SubAgent"):
        self.subagents[agent.name] = agent

    def get_all_tool_schemas(self) -> list[dict]:
        schemas = self.tools.get_schemas()
        for name, agent in self.subagents.items():
            schemas.append({
                "type": "function",
                "function": {
                    "name": f"call_subagent_{name}",
                    "description": agent.description,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": f"向{agent.name}发送的问题"}
                        },
                        "required": ["query"]
                    }
                }
            })
        return schemas

    async def execute(self, name: str, **kwargs) -> str:
        if name.startswith("call_subagent_"):
            agent_name = name[14:]
            agent = self.subagents.get(agent_name)
            if agent:
                return await agent.run(kwargs.get("query", ""))
            return f"错误: 未找到子代理 {agent_name}"
        return await self.tools.execute(name, **kwargs)
