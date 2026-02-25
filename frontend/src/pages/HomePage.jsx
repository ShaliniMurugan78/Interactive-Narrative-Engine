import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useStory } from "../context/StoryContext";
import { startStory } from "../services/storyAPI";
import GenreSelector    from "../components/GenreSelector";
import CharacterSetup   from "../components/CharacterSetup";
import LoadingAnimation from "../components/LoadingAnimation";
import "./HomePage.css";

export default function HomePage() {
  const navigate = useNavigate();
  const { setSessionId, setGenre, setProtagonist, updateScene, setLoading } = useStory();

  const [step,          setStep]          = useState(0);
  const [selectedGenre, setSelectedGenre] = useState("");
  const [formData,      setFormData]      = useState({ protagonist: "", worldSetting: "", tone: "dramatic" });
  const [error,         setError]         = useState("");
  const [starting,      setStarting]      = useState(false);
  const [particles,     setParticles]     = useState([]);

  useEffect(() => {
    const runes = ["✦","⚔","✧","◈","⬡","✵","⟡","◉","☽","✴"];
    setParticles(Array.from({ length: 20 }, (_, i) => ({
      id   : i,
      rune : runes[i % runes.length],
      left : `${Math.random() * 100}%`,
      delay: `${Math.random() * 10}s`,
      dur  : `${10 + Math.random() * 10}s`,
      size : `${0.6 + Math.random() * 0.9}rem`,
    })));
  }, []);

  const handleStart = async () => {
    if (!formData.protagonist.trim()) return setError("Please enter your protagonist's name.");
    if (!formData.worldSetting.trim()) return setError("Please describe your world setting.");
    setError(""); setStarting(true); setLoading(true);
    try {
      const data = await startStory({
        genre        : selectedGenre,
        protagonist  : formData.protagonist.trim(),
        world_setting: formData.worldSetting.trim(),
        tone         : formData.tone,
      });
      setSessionId(data.session_id);
      setGenre(selectedGenre);
      setProtagonist(formData.protagonist.trim());
      updateScene(data);
      navigate("/story");
    } catch {
      setError("Failed to start story. Check your connection and try again.");
    } finally {
      setStarting(false); setLoading(false);
    }
  };

  if (starting) return <LoadingAnimation message="Weaving the threads of your tale..." />;

  return (
    <div className="home-page">
      <div className="particles">
        {particles.map(p => (
          <span key={p.id} className="particle" style={{
            left: p.left, animationDuration: p.dur,
            animationDelay: p.delay, fontSize: p.size
          }}>{p.rune}</span>
        ))}
      </div>
      <div className="home-bg-glow glow-purple" />
      <div className="home-bg-glow glow-gold" />

      <header className="home-header">
        <div className="header-ornament">
          <span className="orn-line" /><span className="orn-diamond">◆</span><span className="orn-line" />
        </div>
        <h1 className="home-title">Narrative Engine</h1>
        <p className="home-tagline">Every choice rewrites destiny</p>
        <div className="header-ornament">
          <span className="orn-line" /><span className="orn-diamond">◆</span><span className="orn-line" />
        </div>
      </header>

      <div className="step-indicator">
        <div className={`step-dot ${step >= 0 ? "active" : ""}`}>
          <span>1</span><label>Genre</label>
        </div>
        <div className={`step-line ${step >= 1 ? "active" : ""}`} />
        <div className={`step-dot ${step >= 1 ? "active" : ""}`}>
          <span>2</span><label>Setup</label>
        </div>
      </div>

      <main className="home-main">
        {step === 0 && (
          <div className="fade-up">
            <GenreSelector selected={selectedGenre} onSelect={g => { setSelectedGenre(g); setError(""); }} />
            {error && <p className="home-error">⚠ {error}</p>}
            <button className="home-cta" onClick={() => {
              if (!selectedGenre) return setError("Please choose a genre to continue.");
              setError(""); setStep(1);
            }}>
              <span>Continue</span><span className="cta-arrow">→</span>
            </button>
          </div>
        )}
        {step === 1 && (
          <div className="fade-up">
            <button className="back-btn" onClick={() => setStep(0)}>← Back</button>
            <CharacterSetup genre={selectedGenre} data={formData} onChange={setFormData} />
            {error && <p className="home-error">⚠ {error}</p>}
            <button className="home-cta" onClick={handleStart}>
              <span>Begin Your Story</span><span className="cta-arrow">✦</span>
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
