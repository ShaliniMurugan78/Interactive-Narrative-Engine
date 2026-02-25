import { BrowserRouter, Routes, Route } from "react-router-dom";
import { StoryProvider } from "./context/StoryContext";
import HomePage   from "./pages/HomePage";
import StoryPage  from "./pages/StoryPage";
import EndingPage from "./pages/EndingPage";
import TreePage   from "./pages/TreePage";

export default function App() {
  return (
    <BrowserRouter>
      <StoryProvider>
        <Routes>
          <Route path="/"       element={<HomePage />}   />
          <Route path="/story"  element={<StoryPage />}  />
          <Route path="/ending" element={<EndingPage />} />
          <Route path="/tree"   element={<TreePage />}   />
        </Routes>
      </StoryProvider>
    </BrowserRouter>
  );
}
