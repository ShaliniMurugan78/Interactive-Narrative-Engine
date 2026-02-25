const BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const post = async (url, body) => {
  const res = await fetch(`${BASE}${url}`, {
    method : "POST",
    headers: { "Content-Type": "application/json" },
    body   : JSON.stringify(body)
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
};

const get = async (url) => {
  const res = await fetch(`${BASE}${url}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
};

export const startStory  = (data)              => post("/story/start",  data);
export const makeChoice  = (sessionId, choice) => post("/story/choose", { session_id: sessionId, choice });
export const getStory    = (sessionId)         => get(`/story/${sessionId}`);
export const exportPDF   = (sessionId)         => post("/export/pdf",   { session_id: sessionId });
export const getTreeData = (sessionId)         => get(`/export/tree/${sessionId}`);
export const downloadPDF = (sessionId)         => window.open(`${BASE}/export/download/${sessionId}`, "_blank");
