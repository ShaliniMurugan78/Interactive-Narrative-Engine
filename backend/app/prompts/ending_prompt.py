def get_ending_system_prompt(genre: str, tone: str) -> str:
    """System prompt for ending scene generation"""
    return f"""You are a master storyteller writing the final chapter 
of a {genre} story.
Your tone is {tone} and emotionally resonant.
You write in second person (You...) always.
You write endings that feel EARNED based on the choices made.
You resolve all major plot threads.
You write 3-4 paragraphs for the ending.
You end with a single powerful, memorable final sentence.
You never introduce new characters in the ending."""


def get_ending_prompt(
    story_context: str,
    all_decisions: list,
    genre: str,
    outcome: str = "Mysterious"
) -> str:
    """User prompt for ending scene generation"""

    decisions_text = "\n".join(
        [f"  - Turn {i+1}: {d}" for i, d in enumerate(all_decisions)]
    ) or "  - No major decisions recorded"

    return f"""Write the FINAL ENDING scene for this {genre} story.

{story_context}

ALL DECISIONS MADE:
{decisions_text}

Expected Outcome Tone: {outcome}

Instructions:
- Show consequences of ALL decisions made
- Resolve the main conflict completely
- Match the {outcome} outcome tone
- Write in second person (You...)
- 3-4 paragraphs
- End with ONE powerful final sentence
- Make it emotionally memorable
- This is the FINAL scene — make it count!"""


def get_outcome_prompt(decisions: list, genre: str) -> str:
    """Prompt to determine story outcome label"""
    return f"""Based on these story decisions, classify the outcome.

Genre    : {genre}
Decisions: {', '.join(decisions)}

Return ONLY one word from this list:
Hero, Tragic, Bittersweet, Mysterious, Triumphant

One word only:"""