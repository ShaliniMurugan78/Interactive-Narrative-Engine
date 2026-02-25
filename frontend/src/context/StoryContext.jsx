import { createContext, useContext, useState } from "react";

const StoryContext = createContext(null);

export function StoryProvider({ children }) {
  const [sessionId,   setSessionId]   = useState(null);
  const [genre,       setGenre]       = useState("");
  const [protagonist, setProtagonist] = useState("");
  const [sceneText,   setSceneText]   = useState("");
  const [choices,     setChoices]     = useState([]);
  const [imageUrl,    setImageUrl]    = useState(null);
  const [turn,        setTurn]        = useState(0);
  const [isEnding,    setIsEnding]    = useState(false);
  const [outcome,     setOutcome]     = useState(null);
  const [loading,     setLoading]     = useState(false);
  const [history,     setHistory]     = useState([]);

  const updateScene = (data) => {
    setSceneText(data.scene_text  || "");
    setChoices(data.choices       || []);
    setImageUrl(data.image_url    || null);
    setTurn(data.turn             || 0);
    setIsEnding(data.is_ending    || false);
    setOutcome(data.outcome       || null);
    setHistory(prev => [...prev, {
      turn      : data.turn,
      scene_text: data.scene_text,
      image_url : data.image_url,
    }]);
  };

  const resetStory = () => {
    setSessionId(null); setGenre(""); setProtagonist("");
    setSceneText(""); setChoices([]); setImageUrl(null);
    setTurn(0); setIsEnding(false); setOutcome(null);
    setLoading(false); setHistory([]);
  };

  return (
    <StoryContext.Provider value={{
      sessionId, setSessionId,
      genre, setGenre,
      protagonist, setProtagonist,
      sceneText, choices, imageUrl,
      turn, isEnding, outcome,
      loading, setLoading,
      history, updateScene, resetStory
    }}>
      {children}
    </StoryContext.Provider>
  );
}

export const useStory = () => useContext(StoryContext);
