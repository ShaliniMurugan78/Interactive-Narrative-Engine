def get_opening_scene_system_prompt(genre: str, tone: str) -> str:
    """System prompt for opening scene generation"""
    return f"""You are a master storyteller writing a {genre} story.
Your writing style is {tone}, vivid, and deeply immersive.
You write in second person (You...) always.
You build atmosphere from the very first sentence.
You never use character names as headers or labels.
You write scenes between 2-3 paragraphs only.
You always end scenes at a natural decision point."""


def get_opening_scene_prompt(
    genre: str,
    protagonist: str,
    world_setting: str,
    tone: str
) -> str:
    """User prompt for opening scene generation"""
    return f"""Write the opening scene of a {genre} story.

Protagonist : {protagonist}
World       : {world_setting}
Tone        : {tone}

Instructions:
- Start dramatically and grab attention immediately
- Introduce the world atmosphere vividly
- Set up an immediate conflict or mystery
- Write in second person (You...)
- End at a natural decision point
- Keep it 2-3 paragraphs"""


def get_next_scene_system_prompt(genre: str, tone: str) -> str:
    """System prompt for next scene generation"""
    return f"""You are a master storyteller continuing a {genre} story.
Your writing is {tone}, vivid, and consequence-driven.
You ALWAYS show immediate consequences of the user's choice.
You write in second person (You...) always.
You stay consistent with all established characters and world details.
You build tension gradually with each passing scene.
You never contradict previous story events.
You write scenes between 2-3 paragraphs only."""


def get_next_scene_prompt(
    story_context: str,
    user_choice: str,
    genre: str,
    turn: int
) -> str:
    """User prompt for next scene generation"""

    # Increase tension instruction based on turn number
    if turn <= 3:
        tension = "Build mild tension and intrigue"
    elif turn <= 6:
        tension = "Build strong tension, stakes are rising"
    else:
        tension = "Maximum tension, story is reaching its climax"

    return f"""Continue this {genre} story based on the user's choice.

{story_context}

User just chose: "{user_choice}"

Instructions:
- Show IMMEDIATE consequences of this choice
- {tension}
- Stay consistent with all characters and world details
- Build on existing plot threads
- Write in second person (You...)
- End at a new natural decision point
- Keep it 2-3 paragraphs"""