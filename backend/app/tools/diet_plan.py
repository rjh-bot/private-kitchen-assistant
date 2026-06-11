from datetime import datetime, timedelta

async def create_diet_plan(goal: str, daily_calories: int = 1800, days: int = 3) -> str:
    """根据目标生成饮食计划"""
    meal_templates = {
        "减脂": {
            "早餐": ["燕麦粥(50g)+牛奶200ml", "全麦面包2片+鸡蛋1个", "无糖酸奶200g+水果"],
            "午餐": ["鸡胸肉150g+西兰花200g+糙米饭100g", "三文鱼150g+沙拉", "豆腐150g+蔬菜+杂粮饭"],
            "晚餐": ["鸡胸肉120g+蔬菜沙拉", "鱼肉150g+蒸蔬菜", "豆腐100g+菌菇汤"],
            "加餐": ["苹果1个", "坚果20g", "蛋白奶昔1杯"]
        },
        "增肌": {
            "早餐": ["鸡蛋3个+燕麦100g+牛奶250ml", "牛肉面+鸡蛋", "蛋白粉+香蕉+全麦面包"],
            "午餐": ["牛肉200g+米饭200g+蔬菜", "鸡胸肉200g+土豆200g+西兰花", "三文鱼200g+意面+蔬菜"],
            "晚餐": ["鸡胸肉200g+红薯200g+蔬菜", "牛肉150g+米饭150g+蔬菜", "鱼肉200g+米饭150g"],
            "加餐": ["蛋白粉+牛奶", "坚果30g+香蕉", "希腊酸奶+蜂蜜"]
        },
        "控糖": {
            "早餐": ["全麦面包+鸡蛋+无糖豆浆", "燕麦麸皮粥+坚果", "蔬菜蛋饼"],
            "午餐": ["糙米饭100g+鸡胸肉+大量蔬菜", "全麦意面+虾仁+蔬菜", "藜麦沙拉+鸡胸肉"],
            "晚餐": ["鱼肉150g+蔬菜沙拉+少量红薯", "豆腐汤+蔬菜+少量杂粮", "鸡胸肉+西葫芦+少量糙米"],
            "加餐": ["黄瓜/芹菜条", "少量坚果", "无糖酸奶"]
        },
        "健康饮食": {
            "早餐": ["全麦三明治+牛奶", "燕麦水果碗", "鸡蛋+蔬菜+全麦面包"],
            "午餐": ["杂粮饭+鱼肉+蔬菜", "鸡胸肉沙拉+全麦面包", "意面+虾仁+蔬菜"],
            "晚餐": ["蔬菜汤+鱼肉+少量主食", "鸡胸肉+烤蔬菜", "豆腐+菌菇+少量米饭"],
            "加餐": ["水果+酸奶", "坚果+黑巧克力", "蔬果汁"]
        }
    }

    templates = meal_templates.get(goal, meal_templates["健康饮食"])
    plan = [f"## {goal}饮食计划 (每日{daily_calories}千卡)\n"]
    calories_per_meal = {"早餐": 0.25, "午餐": 0.35, "晚餐": 0.3, "加餐": 0.1}

    for d in range(days):
        date = (datetime.now() + timedelta(days=d)).strftime("%m月%d日")
        plan.append(f"### 第{d+1}天 ({date})")
        for meal_type, options in templates.items():
            import random
            option = random.choice(options)
            cal = int(daily_calories * calories_per_meal.get(meal_type, 0.25))
            plan.append(f"- **{meal_type}** (~{cal}千卡): {option}")
        plan.append("")

    return "\n".join(plan)

async def record_meal(foods: list[str], notes: str = "") -> str:
    """记录用户进食内容"""
    meal_log = "、".join(foods)
    result = f"✅ 已记录饮食: {meal_log}"
    if notes:
        result += f"\n备注: {notes}"
    result += "\n💡 坚持记录饮食有助于追踪营养摄入！"
    return result
