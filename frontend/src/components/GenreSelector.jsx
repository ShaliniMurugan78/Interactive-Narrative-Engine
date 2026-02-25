import "./GenreSelector.css";

const GENRES = [
  { id: "fantasy",   label: "Fantasy",   icon: "⚔️",  desc: "Magic, kingdoms & ancient dragons",  color: "#4a90d9" },
  { id: "horror",    label: "Horror",    icon: "👁️",  desc: "Darkness, terror & dread",           color: "#c0392b" },
  { id: "romance",   label: "Romance",   icon: "🌹",  desc: "Passion, longing & love",            color: "#e91e8c" },
  { id: "scifi",     label: "Sci-Fi",    icon: "🚀",  desc: "Future worlds & cosmic mysteries",   color: "#00bcd4" },
  { id: "mystery",   label: "Mystery",   icon: "🕵️", desc: "Clues, secrets & hidden truths",     color: "#9b59b6" },
  { id: "adventure", label: "Adventure", icon: "🗺️",  desc: "Epic journeys & discoveries",        color: "#27ae60" },
];

export default function GenreSelector({ selected, onSelect }) {
  return (
    <div className="genre-selector">
      <h2 className="genre-heading">Choose Your Realm</h2>
      <p className="genre-sub">The genre shapes the world that awaits you</p>
      <div className="genre-grid">
        {GENRES.map((g, i) => (
          <button
            key={g.id}
            className={`genre-card ${selected === g.id ? "selected" : ""}`}
            onClick={() => onSelect(g.id)}
            style={{ animationDelay: `${i * 0.08}s`, "--accent": g.color }}
          >
            <div className="genre-glow" />
            <span className="genre-icon">{g.icon}</span>
            <span className="genre-label">{g.label}</span>
            <span className="genre-desc">{g.desc}</span>
            {selected === g.id && <span className="genre-check">✦</span>}
          </button>
        ))}
      </div>
    </div>
  );
}
