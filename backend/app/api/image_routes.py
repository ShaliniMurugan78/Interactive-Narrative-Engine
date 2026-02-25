from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.image_service import generate_image, extract_image_prompt
from app.prompts.image_prompt import build_image_generation_prompt

router = APIRouter(prefix="/image", tags=["Image"])


# ── Request Models ──
class GenerateImageRequest(BaseModel):
    prompt: str
    genre : str = "fantasy"


class SceneImageRequest(BaseModel):
    scene_text: str
    genre     : str = "fantasy"


# ─────────────────────────────────────────
# POST /image/generate
# ─────────────────────────────────────────
@router.post("/generate")
async def generate_image_endpoint(request: GenerateImageRequest):
    """
    Generate an image from a direct text prompt.
    """
    try:
        # Build full image prompt with genre style
        full_prompt = build_image_generation_prompt(
            request.prompt,
            request.genre
        )

        # Generate image
        image_url = generate_image(full_prompt)

        if not image_url:
            raise HTTPException(
                status_code=503,
                detail="Image generation failed or model is loading. Try again."
            )

        print(f"✅ Image generated for prompt: {request.prompt[:50]}")

        return {
            "success"  : True,
            "image_url": image_url,
            "prompt"   : full_prompt
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# POST /image/from-scene
# ─────────────────────────────────────────
@router.post("/from-scene")
async def generate_image_from_scene(request: SceneImageRequest):
    """
    Generate an image from a story scene text.
    Automatically extracts visual description from scene.
    """
    try:
        # Extract visual description from scene
        image_prompt = extract_image_prompt(request.scene_text)

        # Build full prompt with genre style
        full_prompt = build_image_generation_prompt(
            image_prompt,
            request.genre
        )

        # Generate image
        image_url = generate_image(full_prompt)

        if not image_url:
            raise HTTPException(
                status_code=503,
                detail="Image generation failed or model is loading. Try again."
            )

        print(f"✅ Scene image generated | Genre: {request.genre}")

        return {
            "success"      : True,
            "image_url"    : image_url,
            "image_prompt" : image_prompt,
            "full_prompt"  : full_prompt
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Scene image generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))