from app.services.llm_service import call_llm
from app.core.context_manager import StoryContext
from app.core.memory_manager import build_context_prompt


def generate_opening_scene(context: StoryContext) -> str:
    """
    Generate the very first scene of the story.

    Args:
        context: Story context with setup info

    Returns:
        str: Opening scene text
    """
    system_prompt = f"""You are a master storyteller writing a {context.genre} story.
    Write in a vivid, dramatic, and immersive style.
    Build atmosphere and tension from the very first sentence.
    Always write in second person (You...).
    Never use character names as headers.
    Keep scenes between 2-3 paragraphs."""

    prompt = f"""Write the opening scene of a {context.genre} story.
    
Protagonist : {context.protagonist}
World       : {context.world_setting}
Tone        : {context.tone}

Start the story dramatically. Introduce the world and 
set up an immediate conflict or mystery.
End at a natural decision point."""

    try:
        scene = call_llm(prompt, system_prompt, max_tokens=500)
        print(f"✅ Opening scene generated ({len(scene)} chars)")
        return scene.strip()

    except Exception as e:
        print(f"❌ Opening scene generation failed: {e}")
        raise e


def generate_next_scene(context: StoryContext, user_choice: str) -> str:
    """
    Generate the next scene based on user's choice.

    Args:
        context    : Current story context
        user_choice: The choice the user made

    Returns:
        str: Next scene text
    """
    system_prompt = f"""You are a master storyteller writing a {context.genre} story.
    Write in a vivid, dramatic, and immersive style.
    Always show consequences of the user's choice immediately.
    Write in second person (You...).
    Keep scenes between 2-3 paragraphs.
    Build tension gradually as the story progresses.
    Stay consistent with established characters and world details."""

    # Build full context for LLM
    story_context = build_context_prompt(context)

    prompt = f"""Continue this {context.genre} story based on the user's choice.

{story_context}

User just chose: "{user_choice}"

Write the next scene (2-3 paragraphs):
- Show immediate consequences of the choice
- Build on existing plot and characters  
- Increase tension compared to previous scene
- End at a new natural decision point
- Write in second person (You...)"""

    try:
        scene = call_llm(prompt, system_prompt, max_tokens=600)
        print(f"✅ Scene {context.turn + 1} generated ({len(scene)} chars)")
        return scene.strip()

    except Exception as e:
        print(f"❌ Scene generation failed: {e}")
        raise e