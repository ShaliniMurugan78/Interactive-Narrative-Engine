import { useNavigate } from "react-router-dom";
import { useStory } from "../context/StoryContext";
import ExportButton from "../components/ExportButton";
import "./EndingPage.css";

export default function EndingPage() {
  const navigate = useNavigate();
  const { sessionId, sceneText, outcome, genre, protagonist, resetStory } = useStory();
  if (!sessionId) { navigate("/"); return null; }
  return (
    <div className="ending-page">
      <div className="ending-bg-glow" />
      <div className="ending-content fade-up">
        <div className="ending-crown floating">👑</div>
        <h1 className="ending-title">Your Tale is Complete</h1>
        <div className="ending-outcome">
          <span className="eo-label">Outcome Achieved</span>
          <span className="eo-value">{outcome || "Mysterious"}</span>
        </div>
        <div className="ending-meta">
          <span>🧙 {protagonist}</span>
          <span className="dot">·</span>
          <span>📖 {genre}</span>
        </div>
        <div className="ending-excerpt">
          <p>{sceneText?.slice(0, 320)}...</p>
        </div>
        <div className="ending-btns">
          <ExportButton sessionId={sessionId} />
          <button className="ending-tree-btn" onClick={() => navigate("/tree")}>🌿 View Story Tree</button>
          <button className="ending-new-btn" onClick={() => { resetStory(); navigate("/"); }}>✦ New Story</button>
        </div>
      </div>
    </div>
  );
}
