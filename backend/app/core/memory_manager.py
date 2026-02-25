from app.services.llm_service import call_llm
from app.core.context_manager import StoryContext


def summarize_scene(scene_text: str) -> str:
    """
    Summarize a single scene into 2 sentences.

    Args:
        scene_text: Full scene text to summarize

    Returns:
        str: 2 sentence summary
    """
    system_prompt = """You are a story summarizer.
    Summarize the given story scene in exactly 2 sentences.
    Keep only the most important plot points and decisions.
    Be concise and clear."""

    prompt = f"Summarize this scene in 2 sentences:\n{scene_text}"

    try:
        summary = call_llm(prompt, system_prompt, max_tokens=100)
        return summary.strip()
    except Exception as e:
        print(f"❌ Scene summarization failed: {e}")
        return scene_text[:200] + "..."


def update_memory(context: StoryContext) -> StoryContext:
    """
    Update story memory by summarizing older scenes.
    Keeps last 2 scenes full, summarizes the rest.

    Args:
        context: Current story context

    Returns:
        StoryContext: Updated context with memory summary
    """
    scenes = context.full_scenes

    # Only summarize if we have more than 2 scenes
    if len(scenes) <= 2:
        return context

    # Scenes to summarize (all except last 2)
    older_scenes = scenes[:-2]

    # Build summary from older scenes
    summaries = []
    for scene in older_scenes:
        summary = summarize_scene(scene["scene_text"])
        summaries.append(f"Turn {scene['turn']}: {summary}")
        if scene.get("choice_made"):
            summaries.append(f"  → Chose: {scene['choice_made']}")

    # Update memory summary in context
    context.memory_summary = "\n".join(summaries)
    print(f"✅ Memory updated with {len(older_scenes)} summarized scenes")

    return context


def build_context_prompt(context: StoryContext) -> str:
    """
    Build a complete context string to pass to the LLM.
    Uses 3-layer memory system:
    - Layer 1: Key facts (genre, characters, world)
    - Layer 2: Memory summary (older scenes)
    - Layer 3: Last 2 full scenes

    Args:
        context: Current story context

    Returns:
        str: Formatted context string for LLM prompt
    """
    scenes = context.full_scenes

    # Layer 1: Key facts
    key_facts = f"""
STORY SETUP:
- Genre      : {context.genre}
- Protagonist: {context.protagonist}
- World      : {context.world_setting}
- Location   : {context.current_location}
- Characters : {', '.join(context.characters)}
- Turn       : {context.turn}
    """.strip()

    # Layer 2: Memory summary of older scenes
    memory = ""
    if context.memory_summary:
        memory = f"""
STORY SO FAR (Summary):
{context.memory_summary}
        """.strip()

    # Layer 3: Last 2 full scenes
    recent = ""
    if scenes:
        recent_scenes = scenes[-2:]
        recent_texts = []
        for scene in recent_scenes:
            text = f"Scene (Turn {scene['turn']}):\n{scene['scene_text']}"
            if scene.get("choice_made"):
                text += f"\nUser chose: {scene['choice_made']}"
            recent_texts.append(text)
        recent = "RECENT SCENES:\n" + "\n\n".join(recent_texts)

    # Combine all layers
    full_context = "\n\n".join(filter(None, [key_facts, memory, recent]))
    return full_context