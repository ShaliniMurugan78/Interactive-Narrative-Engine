# Genre-specific visual styles for image generation
GENRE_STYLES = {
    "fantasy"  : "fantasy art style, magical, ethereal lighting, detailed",
    "horror"   : "dark horror style, eerie atmosphere, shadow, fog, unsettling",
    "romance"  : "warm romantic lighting, soft colors, cinematic, beautiful",
    "scifi"    : "sci-fi concept art, futuristic, neon lights, cyberpunk style",
    "mystery"  : "noir style, dramatic shadows, moody, cinematic lighting",
    "adventure": "epic adventure art, dramatic landscape, action-packed, vivid"
}

# Default style fallback
DEFAULT_STYLE = "cinematic, dramatic lighting, detailed, high quality digital art"


def get_image_extraction_system_prompt() -> str:
    """System prompt for extracting image description from scene"""
    return """You are a visual description extractor for AI image generation.
Extract a short, vivid image prompt from story text.

Rules:
- Maximum 20 words
- Focus on: setting, mood, lighting, main action
- No dialogue or speech
- No character names
- No abstract concepts
- Only visual, concrete descriptions
- Think like a movie scene description"""


def get_image_extraction_prompt(scene_text: str) -> str:
    """User prompt for extracting image description"""
    return f"""Extract a visual image generation prompt from this story scene.
Maximum 20 words. Focus on setting, mood, and main visual action.

Scene:
{scene_text}

Visual description (20 words max):"""


def build_image_generation_prompt(
    visual_description: str,
    genre: str
) -> str:
    """
    Build the final image generation prompt with style.

    Args:
        visual_description: Extracted visual description
        genre             : Story genre for style matching

    Returns:
        str: Complete image generation prompt
    """
    # Get genre-specific style
    style = GENRE_STYLES.get(genre.lower(), DEFAULT_STYLE)

    # Combine description with style
    final_prompt = f"{visual_description}, {style}"

    # Add quality boosters
    final_prompt += ", masterpiece, highly detailed, 4k"

    return final_prompt


def get_character_image_prompt(
    protagonist: str,
    genre: str,
    world_setting: str
) -> str:
    """
    Build image prompt for protagonist portrait.

    Args:
        protagonist  : Protagonist name/description
        genre        : Story genre
        world_setting: Story world

    Returns:
        str: Image prompt for character portrait
    """
    style = GENRE_STYLES.get(genre.lower(), DEFAULT_STYLE)

    return f"""Portrait of a {genre} protagonist, {world_setting} setting,
    heroic pose, {style}, character concept art, detailed face,
    dramatic lighting, masterpiece"""