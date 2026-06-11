import React, { useState } from "react";
import { updateProfile } from "../api";

const GOALS = ["健康饮食", "减脂", "增肌", "控糖"];

export default function UserProfile({ profile, onUpdate }) {
  const [form, setForm] = useState({ ...profile });
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateProfile(form);
      onUpdate(form);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (err) {
      alert("保存失败: " + err.message);
    }
    setSaving(false);
  };

  return (
    <div className="profile-view">
      <h2>\uD83D\uDC64 个人档案</h2>
      <p className="section-desc">设置你的健康目标和饮食偏好，助理将据此提供个性化建议。</p>

      <div className="form-group">
        <label>健康目标</label>
        <div className="goal-options">
          {GOALS.map((g) => (
            <button
              key={g}
              className={`goal-btn ${form.goal === g ? "active" : ""}`}
              onClick={() => handleChange("goal", g)}
            >
              {g}
            </button>
          ))}
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>体重 (kg)</label>
          <input type="number" value={form.weight || ""}
            onChange={(e) => handleChange("weight", e.target.value ? parseFloat(e.target.value) : null)} />
        </div>
        <div className="form-group">
          <label>身高 (cm)</label>
          <input type="number" value={form.height || ""}
            onChange={(e) => handleChange("height", e.target.value ? parseFloat(e.target.value) : null)} />
        </div>
      </div>

      <div className="form-group">
        <label>饮食偏好</label>
        <input type="text" value={form.diet_preference || ""}
          onChange={(e) => handleChange("diet_preference", e.target.value)}
          placeholder="例如：喜欢清淡、偏爱鸡肉和鱼类" />
      </div>

      <div className="form-group">
        <label>过敏原 / 忌口</label>
        <input type="text" value={form.allergies || ""}
          onChange={(e) => handleChange("allergies", e.target.value)}
          placeholder="例如：花生过敏、不吃辣" />
      </div>

      <div className="form-group">
        <label>长期饮食指令</label>
        <textarea value={form.long_term_instructions || ""}
          onChange={(e) => handleChange("long_term_instructions", e.target.value)}
          placeholder="例如：每餐保证蛋白质摄入，少油少盐"
          rows={3} />
      </div>

      <button className="primary-btn" onClick={handleSave} disabled={saving}>
        {saving ? "保存中..." : saved ? "\u2705 已保存" : "保存设置"}
      </button>
    </div>
  );
}
