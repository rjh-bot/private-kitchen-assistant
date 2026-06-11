import json
from typing import AsyncGenerator
import httpx
from app.config import settings

class DeepSeekClient:
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.base_url = settings.deepseek_base_url
        self.model = settings.model_name

    async def chat(self, messages: list[dict], temperature: float = 0.7) -> str:
        """非流式调用"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(f"{self.base_url}/v1/chat/completions",
                                      json=payload, headers=headers)
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    async def chat_stream(self, messages: list[dict], temperature: float = 0.7) -> AsyncGenerator[str, None]:
        """流式调用"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", f"{self.base_url}/v1/chat/completions",
                                      json=payload, headers=headers) as resp:
                async for line in resp.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        content = json.loads(line[6:])["choices"][0]["delta"].get("content", "")
                        if content:
                            yield content

    async def chat_with_tools(self, messages: list[dict], tools: list[dict]) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "temperature": 0.7
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(f"{self.base_url}/v1/chat/completions",
                                      json=payload, headers=headers)
            return resp.json()

    async def vision_analyze(self, base64_image: str, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-vl2",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }],
            "temperature": 0.3
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                resp = await client.post(f"{self.base_url}/v1/chat/completions",
                                          json=payload, headers=headers)
                return resp.json()["choices"][0]["message"]["content"]
            except Exception as e:
                return f"图片分析暂不可用: {str(e)}。请手动描述食材。"
