from app.services.llm_service import call_llm
from app.core.context_manager import StoryContext
from app.core.memory_manager import build_context_prompt
from app.config import MAX_TURNS


def should_end_story(context: StoryContext) -> bool:
    """
    Determine if the story should end.
    Uses turn count as primary trigger.

    Args:
        context: Current story context

    Returns:
        bool: True if story should end, False otherwise
    """
    # End based on turn count
    if context.turn >= MAX_TURNS:
        print(f"✅ Story ending triggered: reached max turns ({MAX_TURNS})")
        return True

    # End if manually marked
    if context.is_ended:
        print("✅ Story ending triggered: manually marked as ended")
        return True

    return False


def generate_ending(context: StoryContext) -> str:
    """
    Generate a satisfying ending scene based on all decisions made.

    Args:
        context: Complete story context with all decisions

    Returns:
        str: Final ending scene text
    """
    system_prompt = f"""You are a master storyteller writing the final chapter 
    of a {context.genre} story.
    Write a satisfying, conclusive ending that:
    - Reflects ALL the choices the protagonist made
    - Resolves the main conflict
    - Gives a meaningful conclusion
    - Matches the {context.tone} tone
    Write in second person (You...).
    Length: 3-4 paragraphs.
    Make it memorable and emotionally resonant."""

    # Build full story context
    story_context = build_context_prompt(context)

    # Format all decisions for ending
    all_decisions = "\n".join(
        [f"- Turn {i+1}: {d}" for i, d in enumerate(context.decisions)]
    ) or "No major decisions recorded"

    prompt = f"""Write the FINAL ENDING scene for this story.

{story_context}

ALL DECISIONS MADE BY THE PROTAGONIST:
{all_decisions}

Write a conclusive ending (3-4 paragraphs) that:
- Rewards or shows consequences of their specific choices
- Resolves all major plot threads
- Ends with a powerful final sentence
- Write in second person (You...)

This is the FINAL scene - make it count!"""

    try:
        ending = call_llm(prompt, system_prompt, max_tokens=800)
        context.is_ended = True
        print(f"✅ Story ending generated ({len(ending)} chars)")
        return ending.strip()

    except Exception as e:
        print(f"❌ Ending generation failed: {e}")
        raise e


def get_story_outcome(context: StoryContext) -> str:
    """
    Determine the story outcome based on decisions made.
    Returns a label like 'Hero', 'Tragic', 'Bittersweet'.

    Args:
        context: Complete story context

    Returns:
        str: Outcome label
    """
    system_prompt = """You are a story analyst.
    Based on the decisions made, classify the story outcome.
    Return ONLY one of these words:
    Hero, Tragic, Bittersweet, Mysterious, Triumphant"""

    prompt = f"""Story decisions: {', '.join(context.decisions)}
    Genre: {context.genre}
    Classify the outcome in one word:"""

    try:
        outcome = call_llm(prompt, system_prompt, max_tokens=10)
        outcome = outcome.strip().split()[0]
        print(f"✅ Story outcome: {outcome}")
        return outcome

    except Exception as e:
        print(f"❌ Outcome detection failed: {e}")
        return "Mysterious"