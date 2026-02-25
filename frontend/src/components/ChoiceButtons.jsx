import "./ChoiceButtons.css";

const LETTERS = ["A", "B", "C"];
const LABELS  = ["Cautious", "Bold", "Unexpected"];
const ICONS   = ["🛡", "⚔", "✨"];

export default function ChoiceButtons({ choices, onChoice, disabled }) {
  if (!choices || choices.length === 0) return null;
  return (
    <div className="choices-wrap">
      <div className="choices-header">
        <span className="ch-line" />
        <span className="ch-label">✦ What path do you take? ✦</span>
        <span className="ch-line" />
      </div>
      <div className="choices-list">
        {choices.map((choice, i) => (
          <button key={i} className={`choice-btn choice-${i}`}
            onClick={() => onChoice(choice)} disabled={disabled}
            style={{ animationDelay: `${i * 0.12}s` }}>
            <div className="choice-left">
              <span className="choice-icon">{ICONS[i]}</span>
              <div className="choice-meta">
                <span className="choice-letter">{LETTERS[i]}</span>
                <span className="choice-type">{LABELS[i]}</span>
              </div>
            </div>
            <span className="choice-text">{choice.replace(/^[ABC]\)\s*/, "")}</span>
            <span className="choice-arrow">→</span>
            <div className="choice-hover-bg" />
          </button>
        ))}
      </div>
    </div>
  );
}
