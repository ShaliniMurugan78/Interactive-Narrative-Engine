import { useState } from "react";
import "./SceneImage.css";

export default function SceneImage({ imageUrl, alt = "Scene" }) {
  const [loaded, setLoaded] = useState(false);
  if (!imageUrl) return null;
  return (
    <div className={`scene-img-wrap ${loaded ? "loaded" : ""}`}>
      {!loaded && (
        <div className="scene-img-skeleton">
          <div className="skeleton-shimmer" />
          <span className="skeleton-icon">🎨</span>
          <span className="skeleton-text">Painting your scene...</span>
        </div>
      )}
      <img src={imageUrl} alt={alt} className="scene-img"
        onLoad={() => setLoaded(true)} style={{ opacity: loaded ? 1 : 0 }} />
      <div className="scene-img-vignette" />
      <div className="scene-img-frame frame-tl">◤</div>
      <div className="scene-img-frame frame-tr">◥</div>
      <div className="scene-img-frame frame-bl">◣</div>
      <div className="scene-img-frame frame-br">◢</div>
    </div>
  );
}
