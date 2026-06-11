import React, { useState } from "react";

export default function DietPlan({ profile }) {
  const [goal, setGoal] = useState(profile?.goal || "健康饮食");
  const [calories, setCalories] = useState(1800);
  const [days, setDays] = useState(3);
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);

  const GOALS = ["健康饮食", "减脂", "增肌", "控糖"];

  const generatePlan = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: `请帮我制定一个${goal}饮食计划，每日${calories}千卡，共${days}天。`,
          user_id: 1
        }),
      });
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let result = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        result += decoder.decode(value, { stream: true });
      }
      // 提取 SSE data 部分
      const dataLines = result.split("\n")
        .filter(l => l.startsWith("data: "))
        .map(l => l.slice(6));
      setPlan(dataLines.join("\n") || "生成中，请稍候...");
    } catch (err) {
      setPlan("生成失败: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="diet-plan-view">
      <h2>\uD83D\uDCCB 饮食计划</h2>
      <p className="section-desc">根据你的目标自动生成个性化的每日饮食计划。</p>

      <div className="plan-controls">
        <div className="form-group">
          <label>健康目标</label>
          <div className="goal-options">
            {GOALS.map((g) => (
              <button key={g} className={`goal-btn ${goal === g ? "active" : ""}`}
                onClick={() => setGoal(g)}>
                {g}
              </button>
            ))}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>每日热量 (千卡)</label>
            <input type="number" value={calories} onChange={(e) => setCalories(parseInt(e.target.value) || 1800)} />
          </div>
          <div className="form-group">
            <label>天数</label>
            <select value={days} onChange={(e) => setDays(parseInt(e.target.value))}>
              <option value={1}>1天</option>
              <option value={3}>3天</option>
              <option value={7}>7天</option>
            </select>
          </div>
        </div>

        <button className="primary-btn" onClick={generatePlan} disabled={loading}>
          {loading ? "生成中..." : "生成饮食计划"}
        </button>
      </div>

      {plan && (
        <div className="plan-result">
          <h3>你的{goal}计划</h3>
          <pre className="plan-content">{plan}</pre>
        </div>
      )}
    </div>
  );
}
