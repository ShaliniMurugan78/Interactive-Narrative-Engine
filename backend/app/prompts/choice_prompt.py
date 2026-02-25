def get_choice_system_prompt() -> str:
    """System prompt for choice generation"""
    return """You are a story choice generator for an interactive narrative.
Your job is to generate exactly 3 meaningful choices.

Rules you MUST follow:
- Choice A: Cautious / Safe / Careful approach
- Choice B: Bold / Aggressive / Direct approach
- Choice C: Creative / Unexpected / Clever approach

Each choice must:
- Lead the story in a genuinely DIFFERENT direction
- Be exactly 1 clear sentence
- Feel consequential and interesting
- Match the story's genre and tone
- NOT be cosmetic variations of the same action

Return ONLY valid JSON in this exact format:
{
    "choices": [
        "A) ...",
        "B) ...",
        "C) ..."
    ]
}"""


def get_choice_prompt(
    genre: str,
    scene_text: str,
    decisions_so_far: list
) -> str:
    """User prompt for choice generation"""

    decisions_text = (
        ", ".join(decisions_so_far)
        if decisions_so_far
        else "None yet"
    )

    return f"""Generate 3 choices for this story moment.

Genre          : {genre}
Current Scene  : {scene_text}
Past Decisions : {decisions_text}

Generate 3 meaningfully different choices:
- A) Cautious approach
- B) Bold approach  
- C) Unexpected approach

Return valid JSON only."""