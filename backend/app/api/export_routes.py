from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models.request_model import ExportStoryRequest
from app.models.response_model import ExportResponse
from app.services.pdf_service import export_story_pdf
from app.database.db import get_stories_collection
import os

router = APIRouter(prefix="/export", tags=["Export"])


# ─────────────────────────────────────────
# POST /export/pdf
# ─────────────────────────────────────────
@router.post("/pdf", response_model=ExportResponse)
async def export_pdf(request: ExportStoryRequest):
    """
    Export a completed story to PDF file.
    Fetches story from MongoDB and generates PDF.
    """
    try:
        # Get story from MongoDB
        stories_col = get_stories_collection()
        story = await stories_col.find_one(
            {"session_id": request.session_id},
            {"_id": 0}
        )

        if not story:
            raise HTTPException(
                status_code=404,
                detail=f"Story {request.session_id} not found"
            )

        # Generate PDF
        pdf_path = export_story_pdf(story)

        print(f"✅ PDF exported | Session: {request.session_id}")

        return ExportResponse(
            success   = True,
            file_path = pdf_path,
            message   = "Story exported to PDF successfully!"
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ PDF export failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# GET /export/download/{session_id}
# ─────────────────────────────────────────
@router.get("/download/{session_id}")
async def download_pdf(session_id: str):
    """
    Download the generated PDF file directly.
    Returns the PDF file as a downloadable response.
    """
    try:
        pdf_path = f"exports/story_{session_id}.pdf"

        # Check if PDF exists
        if not os.path.exists(pdf_path):
            # Try to generate it first
            stories_col = get_stories_collection()
            story = await stories_col.find_one(
                {"session_id": session_id},
                {"_id": 0}
            )

            if not story:
                raise HTTPException(
                    status_code=404,
                    detail=f"Story {session_id} not found"
                )

            pdf_path = export_story_pdf(story)

        return FileResponse(
            path             = pdf_path,
            media_type       = "application/pdf",
            filename         = f"my_story_{session_id}.pdf"
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ PDF download failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# GET /export/tree/{session_id}
# ─────────────────────────────────────────
@router.get("/tree/{session_id}")
async def get_story_tree(session_id: str):
    """
    Get the branching tree data for a story.
    Returns nodes and edges for frontend visualization.
    """
    try:
        stories_col = get_stories_collection()
        story = await stories_col.find_one(
            {"session_id": session_id},
            {"_id": 0}
        )

        if not story:
            raise HTTPException(
                status_code=404,
                detail=f"Story {session_id} not found"
            )

        # Build tree nodes and edges
        nodes = []
        edges = []

        scenes = story.get("scenes", [])

        for i, scene in enumerate(scenes):
            # Add node for each scene
            nodes.append({
                "id"   : f"scene_{i}",
                "label": f"Chapter {i + 1}",
                "text" : scene.get("scene_text", "")[:100] + "...",
                "turn" : scene.get("turn", i)
            })

            # Add edge from previous scene
            if i > 0:
                edges.append({
                    "from" : f"scene_{i-1}",
                    "to"   : f"scene_{i}",
                    "label": scene.get("choice_made", "")[:30]
                })

        print(f"✅ Tree data built | Nodes: {len(nodes)} | Edges: {len(edges)}")

        return {
            "success"   : True,
            "session_id": session_id,
            "nodes"     : nodes,
            "edges"     : edges
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Tree generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))