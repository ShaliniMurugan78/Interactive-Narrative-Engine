import json
from app.services.llm_service import call_llm_json
from app.core.context_manager import StoryContext


def generate_choices(context: StoryContext, scene_text: str) -> list:
    """
    Generate 3 meaningful choices based on the current scene.

    Args:
        context   : Current story context
        scene_text: The scene text to generate choices for

    Returns:
        list: List of 3 choice strings
    """
    system_prompt = """You are a story choice generator.
    Generate exactly 3 meaningful choices for the reader.
    Each choice must lead the story in a DIFFERENT direction.
    
    Rules:
    - Choice A: Cautious / Safe approach
    - Choice B: Bold / Aggressive approach  
    - Choice C: Creative / Unexpected approach
    
    Each choice should be 1 sentence long.
    Make choices feel consequential and interesting.
    
    Return ONLY valid JSON in this exact format:
    {
        "choices": [
            "A) ...",
            "B) ...",
            "C) ..."
        ]
    }"""

    prompt = f"""Generate 3 choices for this story scene:

Genre: {context.genre}
Current Scene: {scene_text}
Story Decisions So Far: {', '.join(context.decisions) or 'None yet'}

Generate 3 different choices (cautious, bold, unexpected):"""

    try:
        response = call_llm_json(prompt, system_prompt, max_tokens=300)
        data = json.loads(response)
        choices = data.get("choices", [])

        # Validate we got 3 choices
        if len(choices) != 3:
            raise ValueError(f"Expected 3 choices, got {len(choices)}")

        print(f"✅ Generated {len(choices)} choices")
        for choice in choices:
            print(f"   {choice}")

        return choices

    except Exception as e:
        print(f"❌ Choice generation failed: {e}")
        # Fallback choices if generation fails
        return [
            "A) Proceed carefully and observe the situation",
            "B) Take bold action and face the challenge head-on",
            "C) Look for a creative alternative solution"
        ]