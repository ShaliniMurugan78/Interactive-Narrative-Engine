import "./SceneCard.css";

export default function SceneCard({ text, turn, isEnding, outcome }) {
  if (!text) return null;
  return (
    <div className={`scene-card ${isEnding ? "ending" : ""}`}>
      <div className="scene-ornament">
        <span className="orn-line-h" />
        <span className="orn-text">{isEnding ? `✦ ${outcome || "The End"} ✦` : `Chapter ${turn}`}</span>
        <span className="orn-line-h" />
      </div>
      <div className="scene-body">
        {text.split("\n\n").map((para, i) => (
          <p key={i} className="scene-para" style={{ animationDelay: `${i * 0.15}s` }}>{para}</p>
        ))}
      </div>
      <div className="scene-ornament bottom">
        <span className="orn-line-h" /><span className="orn-diamond">◆</span><span className="orn-line-h" />
      </div>
    </div>
  );
}
