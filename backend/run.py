import uvicorn

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Launching Interactive Narrative Engine...")
    print("=" * 50)
    print("📖 API Docs  → http://localhost:8000/docs")
    print("❤️  Health    → http://localhost:8000/health")
    print("🌐 Frontend  → http://localhost:3000")
    print("=" * 50)

    uvicorn.run(
        "app.main:app",
        host      = "0.0.0.0",
        port      = 8000,
        reload    = True,    # Auto-reload on file changes
        log_level = "info"
    )