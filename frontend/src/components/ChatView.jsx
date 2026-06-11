import React, { useState, useRef, useEffect } from "react";
import { createChatStream } from "../api";

export default function ChatView({ profile }) {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "你好！我是你的私人厨房助理。我可以帮你搜索菜谱、分析营养、制定饮食计划、识别食材。有什么需要帮忙的吗？" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);
    setStreaming(true);

    try {
      const res = await createChatStream(userMsg);
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let assistantMsg = "";

      const readLoop = async () => {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });

          const lines = buffer.split("\n");
          buffer = lines.pop() || "";

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const data = line.slice(6);
              setMessages((prev) => {
                const updated = [...prev];
                const last = updated[updated.length - 1];
                if (last && last.role === "assistant") {
                  updated[updated.length - 1] = { ...last, content: data };
                } else {
                  updated.push({ role: "assistant", content: data });
                }
                return updated;
              });
              assistantMsg = data;
            }
          }
        }
        setStreaming(false);
        setLoading(false);
      };
      readLoop();
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `错误: ${err.message}` }]);
      setLoading(false);
      setStreaming(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-view">
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-msg ${msg.role}`}>
            <div className="msg-avatar">
              {msg.role === "user" ? "\uD83D\uDC64" : "\uD83C\uDF73"}
            </div>
            <div className="msg-content">{msg.content}</div>
          </div>
        ))}
        {loading && !streaming && (
          <div className="chat-msg assistant">
            <div className="msg-avatar">\uD83C\uDF73</div>
            <div className="msg-content typing">思考中...</div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>
      <div className="chat-input">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="输入你的问题（Enter发送，Shift+Enter换行）"
          rows={2}
          disabled={loading}
        />
        <button className="send-btn" onClick={handleSend} disabled={loading || !input.trim()}>
          发送
        </button>
      </div>
    </div>
  );
}
