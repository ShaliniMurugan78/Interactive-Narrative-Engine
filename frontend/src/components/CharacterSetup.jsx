import { genreEmoji } from "../utils/helpers";
import "./CharacterSetup.css";

const TONES = [
  { id: "dramatic",     label: "Dramatic",     icon: "🎭" },
  { id: "dark",         label: "Dark",         icon: "🌑" },
  { id: "lighthearted", label: "Lighthearted", icon: "☀️" },
  { id: "mysterious",   label: "Mysterious",   icon: "🌫️" },
  { id: "epic",         label: "Epic",         icon: "⚡" },
];

export default function CharacterSetup({ genre, data, onChange }) {
  const set = (key, val) => onChange(prev => ({ ...prev, [key]: val }));
  return (
    <div className="char-setup">
      <div className="char-header">
        <span className="char-genre-badge">{genreEmoji(genre)} {genre}</span>
        <h2 className="char-heading">Craft Your Legend</h2>
        <p className="char-sub">Shape the hero and world of your story</p>
      </div>
      <div className="field-group">
        <label className="field-label"><span className="label-icon">⚔</span> Protagonist Name</label>
        <input className="field-input" type="text" placeholder="e.g. Aria, Marcus, Luna, Zephyr..."
          value={data.protagonist} onChange={e => set("protagonist", e.target.value)} />
      </div>
      <div className="field-group">
        <label className="field-label"><span className="label-icon">🌍</span> World Setting</label>
        <textarea className="field-input field-textarea" rows={3}
          placeholder="e.g. A crumbling medieval kingdom where an ancient curse has turned all magic against the living..."
          value={data.worldSetting} onChange={e => set("worldSetting", e.target.value)} />
      </div>
      <div className="field-group">
        <label className="field-label"><span className="label-icon">🎨</span> Story Tone</label>
        <div className="tone-grid">
          {TONES.map(t => (
            <button key={t.id} className={`tone-btn ${data.tone === t.id ? "selected" : ""}`}
              onClick={() => set("tone", t.id)}>
              <span>{t.icon}</span><span>{t.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
