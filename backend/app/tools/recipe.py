from app.rag.retriever import RecipeRetriever

_retriever: RecipeRetriever | None = None

def init_recipe_tool(recipes: list[dict]):
    global _retriever
    _retriever = RecipeRetriever(recipes)

async def search_recipes(query: str, top_k: int = 5) -> str:
    """根据关键词搜索菜谱"""
    if not _retriever:
        return "菜谱数据未加载"
    results = _retriever.search(query, top_k)
    if not results:
        return "未找到匹配的菜谱"
    lines = [f"### {r['name']}"]
    for r in results:
        cal = r.get("calories", 0)
        p = r.get("protein", 0)
        f = r.get("fat", 0)
        c = r.get("carbs", 0)
        lines.append(f"- **{r['name']}**: {cal:.0f}千卡 | 蛋白质{p:.0f}g | 脂肪{f:.0f}g | 碳水{c:.0f}g")
        if r.get("description"):
            lines.append(f"  {r['description']}")
    return "\n".join(lines)
