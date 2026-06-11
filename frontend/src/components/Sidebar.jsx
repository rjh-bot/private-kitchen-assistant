import React from "react";

const NAV_ITEMS = [
  { key: "chat", icon: "\uD83D\uDCAC", label: "对话" },
  { key: "diet", icon: "\uD83D\uDCCB", label: "饮食计划" },
  { key: "image", icon: "\uD83D\uDCF7", label: "图片识别" },
  { key: "profile", icon: "\uD83D\uDC64", label: "个人档案" },
];

export default function Sidebar({ currentView, onNavigate, profile }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1 className="sidebar-title">\uD83C\uDF73 私人厨房助理</h1>
        {profile && (
          <div className="sidebar-goal">
            目标: {profile.goal || "未设置"}
          </div>
        )}
      </div>
      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.key}
            className={`nav-btn ${currentView === item.key ? "active" : ""}`}
            onClick={() => onNavigate(item.key)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}
