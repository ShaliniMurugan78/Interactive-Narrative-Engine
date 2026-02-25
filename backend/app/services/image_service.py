import requests
import base64
import os
from app.config import HUGGINGFACE_API_KEY, HUGGINGFACE_MODEL

# HuggingFace API URL
API_URL = f"https://router.huggingface.co/hf-inference/models/{HUGGINGFACE_MODEL}"

# Headers for authentication
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


def generate_image(image_prompt: str) -> str:
    """
    Generate an image from a text prompt using HuggingFace API.

    Args:
        image_prompt: Text description of the image to generate

    Returns:
        str: Base64 encoded image string OR error message
    """
    try:
        print(f"🎨 Generating image for: {image_prompt[:50]}...")

        # Send request to HuggingFace
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": image_prompt},
            timeout=60  # Wait up to 60 seconds
        )

        # Check if model is still loading
        if response.status_code == 503:
            print("⏳ Model is loading, please wait...")
            return None

        # Check for errors
        if response.status_code != 200:
            print(f"❌ Image generation failed: {response.text}")
            return None

        # Convert image bytes to base64
        image_bytes = response.content
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        print("✅ Image generated successfully!")
        return f"data:image/jpeg;base64,{image_base64}"

    except Exception as e:
        print(f"❌ Image service error: {e}")
        return None


def extract_image_prompt(scene_text: str) -> str:
    """
    Extract a short visual description from a scene text
    to use as image generation prompt.

    Args:
        scene_text: Full story scene text

    Returns:
        str: Short visual description for image generation
    """
    from app.services.llm_service import call_llm

    system_prompt = """You are a visual description extractor.
    Extract a short image generation prompt from story text.
    Maximum 20 words. Focus on: setting, mood, main character action.
    No dialogue. No names. Just visual description."""

    prompt = f"""Extract a visual image prompt from this story scene:
    {scene_text}
    
    Return only the image prompt, nothing else."""

    try:
        image_prompt = call_llm(prompt, system_prompt, max_tokens=50)
        print(f"✅ Image prompt extracted: {image_prompt}")
        return image_prompt.strip()

    except Exception as e:
        print(f"❌ Image prompt extraction failed: {e}")
        return "fantasy landscape, dramatic lighting, cinematic"