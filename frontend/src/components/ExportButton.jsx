import { useState } from "react";
import { downloadPDF } from "../services/storyAPI";
import "./ExportButton.css";

export default function ExportButton({ sessionId }) {
  const [clicked, setClicked] = useState(false);
  const handle = () => {
    setClicked(true);
    downloadPDF(sessionId);
    setTimeout(() => setClicked(false), 2000);
  };
  return (
    <button className={`export-btn ${clicked ? "clicked" : ""}`} onClick={handle}>
      <span className="export-icon">{clicked ? "✓" : "↓"}</span>
      <span>{clicked ? "Downloading..." : "Download Your Story"}</span>
    </button>
  );
}
