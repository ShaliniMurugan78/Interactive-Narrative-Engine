import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useStory } from "../context/StoryContext";
import { getTreeData } from "../services/storyAPI";
import "./TreePage.css";

export default function TreePage() {
  const navigate = useNavigate();
  const { sessionId, genre } = useStory();
  const [treeData, setTreeData] = useState(null);
  const [loading,  setLoading]  = useState(true);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    if (!sessionId) { navigate("/"); return; }
    getTreeData(sessionId).then(setTreeData).catch(console.error).finally(() => setLoading(false));
  }, [sessionId, navigate]);

  if (!sessionId) return null;

  return (
    <div className="tree-page">
      <div className="tree-bg" />
      <header className="tree-header">
        <button className="tree-back" onClick={() => navigate("/story")}>← Back</button>
        <h1 className="tree-title">Your Story Path</h1>
        <span className="tree-genre">{genre}</span>
      </header>
      {loading && (
        <div className="tree-loading">
          <div className="tree-spinner" /><p>Building your story tree...</p>
        </div>
      )}
      {!loading && treeData && (
        <div className="tree-content fade-up">
          <p className="tree-desc">✦ {treeData.nodes?.length || 0} chapters · {treeData.edges?.length || 0} choices made</p>
          <div className="tree-visual">
            {treeData.nodes?.map((node, i) => (
              <div key={node.id} className={`tree-node-wrap`} style={{ animationDelay: `${i * 0.1}s` }}>
                <div
                  className={`tree-node ${selected === node.id ? "selected" : ""}`}
                  onClick={() => setSelected(selected === node.id ? null : node.id)}
                >
                  <div className="node-num">{i + 1}</div>
                  <div className="node-info">
                    <span className="node-label">{node.label}</span>
                    {selected === node.id && <span className="node-preview fade-in">{node.text}</span>}
                  </div>
                  <span className="node-expand">{selected === node.id ? "▲" : "▼"}</span>
                </div>
                {i < treeData.nodes.length - 1 && (
                  <div className="node-connector">
                    <span className="connector-line" />
                    <span className="connector-choice">{treeData.edges?.[i]?.label?.slice(0, 50) || "→"}</span>
                    <span className="connector-arrow">↓</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
