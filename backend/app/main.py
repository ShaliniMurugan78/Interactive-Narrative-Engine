from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import FRONTEND_URL
from app.database.db import connect_db, disconnect_db
from app.api.story_routes import router as story_router
from app.api.export_routes import router as export_router
from app.api.image_routes import router as image_router


# ─────────────────────────────────────────
# Lifespan (startup & shutdown)
# ─────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──
    print("=" * 50)
    print("🚀 Starting Interactive Narrative Engine...")
    print("=" * 50)
    await connect_db()
    print("✅ Server is ready!")
    print("=" * 50)
    yield

    # ── Shutdown ──
    print("=" * 50)
    print("🛑 Shutting down server...")
    await disconnect_db()
    print("✅ Server shutdown complete!")
    print("=" * 50)


# ─────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────
app = FastAPI(
    title       = "Interactive Narrative Engine",
    description = "An AI-powered interactive story generator with branching narratives",
    version     = "1.0.0",
    lifespan    = lifespan
)


# ─────────────────────────────────────────
# CORS Middleware
# ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins     = [FRONTEND_URL, "http://localhost:3000"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)


# ─────────────────────────────────────────
# Register Routers
# ─────────────────────────────────────────
app.include_router(story_router)
app.include_router(export_router)
app.include_router(image_router)


# ─────────────────────────────────────────
# Root Endpoint
# ─────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Welcome to Interactive Narrative Engine API!",
        "version": "1.0.0",
        "status" : "running",
        "docs"   : "http://localhost:8000/docs"
    }


# ─────────────────────────────────────────
# Health Check Endpoint
# ─────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status" : "healthy",
        "message": "All systems operational"
    }


# ─────────────────────────────────────────
# Global Error Handler
# ─────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print(f"❌ Unhandled error: {exc}")
    return JSONResponse(
        status_code = 500,
        content     = {
            "success": False,
            "error"  : str(exc),
            "message": "Internal server error"
        }
    )