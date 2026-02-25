import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useStory } from "../context/StoryContext";
import { makeChoice } from "../services/storyAPI";
import SceneCard        from "../components/SceneCard";
import SceneImage       from "../components/SceneImage";
import ChoiceButtons    from "../components/ChoiceButtons";
import StoryProgress    from "../components/StoryProgress";
import ExportButton     from "../components/ExportButton";
import LoadingAnimation from "../components/LoadingAnimation";
import "./StoryPage.css";

export default function StoryPage() {
  const navigate = useNavigate();
  const {
    sessionId, genre, protagonist,
    sceneText, choices, imageUrl,
    turn, isEnding, outcome,
    loading, setLoading,
    updateScene, resetStory
  } = useStory();

  useEffect(() => { if (!sessionId) navigate("/"); }, [sessionId, navigate]);
  if (!sessionId) return null;
  if (loading) return <LoadingAnimation message="The story continues to unfold..." />;

  const handleChoice = async (choice) => {
    setLoading(true);
    try {
      const data = await makeChoice(sessionId, choice);
      updateScene(data);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  };

  return (
    <div className="story-page">
      <div className="story-ambient" />
      <nav className="story-nav">
        <button className="nav-btn" onClick={() => { resetStory(); navigate("/"); }}>← New Story</button>
        <div className="nav-center">
          <span className="nav-protagonist">✦ {protagonist} ✦</span>
        </div>
        {isEnding && <ExportButton sessionId={sessionId} />}
      </nav>
      <div className="story-progress-bar">
        <StoryProgress turn={turn} genre={genre} />
      </div>
      <main className="story-main">
        <SceneImage imageUrl={imageUrl} alt={`Chapter ${turn}`} />
        <SceneCard text={sceneText} turn={turn} isEnding={isEnding} outcome={outcome} />
        {!isEnding ? (
          <ChoiceButtons choices={choices} onChoice={handleChoice} disabled={loading} />
        ) : (
          <div className="ending-actions fade-up">
            <div className="outcome-badge">
              <span className="outcome-label">Your Outcome</span>
              <span className="outcome-value">{outcome}</span>
            </div>
            <ExportButton sessionId={sessionId} />
            <button className="restart-btn" onClick={() => navigate("/tree")}>🌿 View Story Tree</button>
            <button className="restart-btn" onClick={() => { resetStory(); navigate("/"); }}>✦ Begin a New Tale</button>
          </div>
        )}
      </main>
    </div>
  );
}
