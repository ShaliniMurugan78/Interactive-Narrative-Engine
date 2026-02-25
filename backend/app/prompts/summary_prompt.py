def get_summary_system_prompt() -> str:
    """System prompt for scene summarization"""
    return """You are a story summarizer.
Your job is to condense story scenes into brief summaries.
Rules:
- Summarize in exactly 2 sentences
- Keep only the most important plot points
- Keep any major decisions or revelations
- Keep character names that were introduced
- Remove all descriptive language and atmosphere
- Be factual and concise"""


def get_summary_prompt(scene_text: str, choice_made: str = None) -> str:
    """User prompt for scene summarization"""

    choice_text = (
        f"\nDecision made: {choice_made}"
        if choice_made
        else ""
    )

    return f"""Summarize this story scene in exactly 2 sentences.
Keep only the most important plot points and any decisions made.

Scene:
{scene_text}
{choice_text}

2-sentence summary:"""


def get_full_story_summary_prompt(
    scenes_summary: str,
    genre: str,
    protagonist: str
) -> str:
    """Prompt to generate a complete story summary for PDF export"""
    return f"""Write a brief story overview for a {genre} story.

Protagonist: {protagonist}

Story Events:
{scenes_summary}

Write a 3-4 sentence overview of the complete story arc.
Make it read like a back-cover book description.
Write in third person."""