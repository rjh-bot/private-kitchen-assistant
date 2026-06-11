async def web_search(query: str) -> str:
    """联网搜索食谱或营养信息 (模拟)"""
    return (
        f"🔍 搜索: {query}\n\n"
        f"当前为离线演示模式，无法执行实时搜索。\n"
        f"建议在 .env 中配置搜索API后使用。\n\n"
        f"现有菜谱库中可能包含相关结果，请尝试使用「搜索菜谱」功能。"
    )
