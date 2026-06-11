async def analyze_nutrition(food_name: str, weight_g: float = 100) -> str:
    """分析食物的营养成分"""
    # 常见食物营养数据库 (简化版，每100g)
    food_db = {
        "鸡胸肉": {"calories": 133, "protein": 31, "fat": 3.6, "carbs": 0},
        "鸡蛋": {"calories": 144, "protein": 13.3, "fat": 8.8, "carbs": 1.5},
        "米饭": {"calories": 116, "protein": 2.6, "fat": 0.3, "carbs": 25.9},
        "牛肉": {"calories": 125, "protein": 20.2, "fat": 4.2, "carbs": 0.2},
        "三文鱼": {"calories": 208, "protein": 20.0, "fat": 13.4, "carbs": 0},
        "西兰花": {"calories": 34, "protein": 2.8, "fat": 0.4, "carbs": 6.6},
        "红薯": {"calories": 86, "protein": 1.6, "fat": 0.1, "carbs": 20.1},
        "豆腐": {"calories": 76, "protein": 8.1, "fat": 3.7, "carbs": 1.9},
        "牛油果": {"calories": 160, "protein": 2.0, "fat": 14.7, "carbs": 8.5},
        "燕麦": {"calories": 367, "protein": 13.5, "fat": 6.7, "carbs": 66.3},
        "牛奶": {"calories": 66, "protein": 3.2, "fat": 3.6, "carbs": 4.8},
        "香蕉": {"calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 22.8},
    }
    info = food_db.get(food_name)
    if not info:
        return f"未收录「{food_name}」的营养数据"

    ratio = weight_g / 100
    return (f"**{food_name}** ({weight_g}g):\n"
            f"- 热量: {info['calories']*ratio:.0f} 千卡\n"
            f"- 蛋白质: {info['protein']*ratio:.1f}g\n"
            f"- 脂肪: {info['fat']*ratio:.1f}g\n"
            f"- 碳水化合物: {info['carbs']*ratio:.1f}g")

async def calculate_meal_calories(foods: list[dict]) -> str:
    """计算一餐的总热量"""
    total_cal = sum(f.get("calories", 0) for f in foods)
    total_protein = sum(f.get("protein", 0) for f in foods)
    total_fat = sum(f.get("fat", 0) for f in foods)
    total_carbs = sum(f.get("carbs", 0) for f in foods)
    return (f"**餐食总计**:\n"
            f"- 总热量: {total_cal:.0f} 千卡\n"
            f"- 蛋白质: {total_protein:.1f}g\n"
            f"- 脂肪: {total_fat:.1f}g\n"
            f"- 碳水: {total_carbs:.1f}g")
