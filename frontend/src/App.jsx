import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import ChatView from "./components/ChatView";
import UserProfile from "./components/UserProfile";
import DietPlan from "./components/DietPlan";
import ImageUpload from "./components/ImageUpload";
import { getProfile } from "./api";

export default function App() {
  const [currentView, setCurrentView] = useState("chat");
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getProfile()
      .then(setProfile)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const renderView = () => {
    switch (currentView) {
      case "chat":
        return <ChatView profile={profile} />;
      case "profile":
        return <UserProfile profile={profile} onUpdate={setProfile} />;
      case "diet":
        return <DietPlan profile={profile} />;
      case "image":
        return <ImageUpload />;
      default:
        return <ChatView profile={profile} />;
    }
  };

  if (loading) {
    return <div className="app-loading">加载中...</div>;
  }

  return (
    <div className="app">
      <Sidebar currentView={currentView} onNavigate={setCurrentView} profile={profile} />
      <main className="main-content">
        {renderView()}
      </main>
    </div>
  );
}
