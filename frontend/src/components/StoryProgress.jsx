import "./StoryProgress.css";

export default function StoryProgress({ turn, maxTurns = 10, genre }) {
  const pct = Math.min((turn / maxTurns) * 100, 100);
  return (
    <div className="progress-wrap">
      <div className="progress-info">
        <span className="progress-genre">{genre}</span>
        <span className="progress-turn">Chapter {turn} of {maxTurns}</span>
      </div>
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${pct}%` }} />
        <div className="progress-glow" style={{ left: `${pct}%` }} />
        {Array.from({ length: maxTurns }, (_, i) => (
          <div key={i} className={`progress-tick ${i < turn ? "done" : ""}`}
            style={{ left: `${((i + 1) / maxTurns) * 100}%` }} />
        ))}
      </div>
    </div>
  );
}
