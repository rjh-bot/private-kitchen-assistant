import React, { useState, useRef } from "react";
import { analyzeImage } from "../api";

export default function ImageUpload() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileRef = useRef(null);

  const handleFile = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setImage(file);
    setResult(null);
    const reader = new FileReader();
    reader.onload = (ev) => setPreview(ev.target.result);
    reader.readAsDataURL(file);
  };

  const handleAnalyze = async () => {
    if (!image) return;
    setLoading(true);
    try {
      const data = await analyzeImage(image);
      setResult(data.result);
    } catch (err) {
      setResult("分析失败: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="image-view">
      <h2>\uD83D\uDCF7 食材/菜品识别</h2>
      <p className="section-desc">拍照上传食材或菜品，AI 帮你识别并估算营养成分。</p>

      <div className="image-upload-area">
        {preview ? (
          <img src={preview} alt="upload" className="image-preview" />
        ) : (
          <div className="upload-placeholder" onClick={() => fileRef.current.click()}>
            <div className="upload-icon">\uD83D\uDCC8</div>
            <p>点击上传图片</p>
          </div>
        )}
        <input type="file" ref={fileRef} onChange={handleFile} accept="image/*" hidden />
      </div>

      {preview && (
        <div className="image-actions">
          <button className="secondary-btn" onClick={() => { setImage(null); setPreview(null); setResult(null); }}>
            重新选择
          </button>
          <button className="primary-btn" onClick={handleAnalyze} disabled={loading}>
            {loading ? "分析中..." : "识别营养成分"}
          </button>
        </div>
      )}

      {result && (
        <div className="image-result">
          <h3>识别结果</h3>
          <pre className="result-content">{result}</pre>
        </div>
      )}
    </div>
  );
}
