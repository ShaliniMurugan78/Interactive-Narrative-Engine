# 📖 Interactive Narrative Engine

> An AI-powered interactive story generator where every choice you make rewrites your destiny.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-F55036?style=for-the-badge)

---

## What is This?

The **Interactive Narrative Engine** is a full-stack AI-powered storytelling application. You choose your genre, name your hero, describe your world and an AI writes a unique branching story just for you. Every choice you make at each chapter changes the story direction, leading to a completely unique ending every time.

---

## How It Works

```
You set up → AI writes → You choose → Story branches → Unique ending
```

1. **Choose a Genre** — Fantasy, Horror, Romance, Sci-Fi, Mystery, or Adventure
2. **Name Your Hero** — Any name you want
3. **Describe Your World** — Completely custom world setting
4. **Pick a Tone** — Dramatic, Dark, Lighthearted, Mysterious, or Epic
5. **Play 10 Chapters** — Make choices at each chapter (A, B, or C)
6. **Get Your Ending** — Based on every decision you made
7. **Download PDF** — Save your unique story forever

---

## Features

- AI Story Generation powered by Groq LLaMA 3.3 70B
- AI Scene Images via HuggingFace Stable Diffusion
- Branching Narrative where every choice changes the story
- 10-Chapter Stories with full arc and satisfying endings
- PDF Export to download your complete story
- Story Tree View showing all your decisions visually
- MongoDB Storage for all stories
- Beautiful dark fantasy UI with animations

---

## Tech Stack

| Layer       | Technology                              |
|-------------|----------------------------------------|
| Frontend    | React 18, React Router, CSS Animations |
| Backend     | Python, FastAPI, Uvicorn               |
| AI / LLM    | Groq API (LLaMA 3.3 70B Versatile)     |
| Images      | HuggingFace (Stable Diffusion XL)      |
| Database    | MongoDB Atlas (Free Tier)              |
| PDF Export  | FPDF2                                  |

---

## Project Structure

```
interactive-narrative-engine/
├── backend/
│   ├── app/
│   │   ├── api/            # Story, export, image routes
│   │   ├── core/           # Scene, choice, ending engine
│   │   ├── services/       # Groq, HuggingFace, PDF
│   │   ├── models/         # Pydantic data models
│   │   ├── prompts/        # AI prompt templates
│   │   ├── database/       # MongoDB connection
│   │   ├── config.py
│   │   └── main.py
│   ├── .env
│   ├── requirements.txt
│   └── run.py
│
└── frontend/
    ├── public/
    │   └── index.html
    └── src/
        ├── pages/          # HomePage, StoryPage, EndingPage, TreePage
        ├── components/     # GenreSelector, SceneCard, ChoiceButtons...
        ├── context/        # StoryContext global state
        ├── services/       # storyAPI.js
        ├── utils/          # helpers.js
        ├── App.jsx
        ├── index.js
        └── index.css
```

---

## Example Story Inputs

**Fantasy:**
```
Protagonist : Aria
World       : A crumbling medieval kingdom cursed by an ancient sorcerer
Tone        : Dark
```

**Sci-Fi:**
```
Protagonist : Marcus
World       : A dying space station orbiting a collapsing star
Tone        : Epic
```

**Mystery:**
```
Protagonist : Luna
World       : Victorian city where people vanish every full moon
Tone        : Mysterious
```

---

## API Endpoints

| Method | Endpoint                  | Description          |
|--------|---------------------------|----------------------|
| POST   | /story/start              | Start a new story    |
| POST   | /story/choose             | Make a choice        |
| GET    | /story/{session_id}       | Get story state      |
| POST   | /export/pdf               | Export to PDF        |
| GET    | /export/download/{id}     | Download PDF         |
| GET    | /export/tree/{id}         | Get story tree       |


---

## Acknowledgements

- [Groq](https://groq.com) for ultra-fast LLM inference
- [HuggingFace](https://huggingface.co) for free image generation
- [MongoDB Atlas](https://cloud.mongodb.com) for free cloud database
- [FastAPI](https://fastapi.tiangolo.com) for the Python web framework
- [React](https://reactjs.org) for the frontend library

---

Built with love Shalini — Every choice rewrites destiny
