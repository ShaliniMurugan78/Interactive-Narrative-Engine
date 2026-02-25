from typing import List, Optional
from datetime import datetime


class StoryContext:
    """
    Manages the complete context of an ongoing story.
    Tracks characters, world, decisions, and current state.
    """

    def __init__(
        self,
        genre: str,
        protagonist: str,
        world_setting: str,
        tone: str = "dramatic"
    ):
        # ---- Story Setup ----
        self.genre        = genre
        self.protagonist  = protagonist
        self.world_setting = world_setting
        self.tone         = tone

        # ---- Story State ----
        self.turn         = 0
        self.is_ended     = False
        self.created_at   = datetime.now().isoformat()

        # ---- Story Elements ----
        self.characters: List[str] = [protagonist]
        self.decisions: List[str]  = []
        self.current_location      = world_setting
        self.current_scene_text    = ""

        # ---- Memory ----
        self.full_scenes: List[dict]    = []
        self.memory_summary: str        = ""

    def add_character(self, character: str):
        """Add a new character to the story"""
        if character not in self.characters:
            self.characters.append(character)
            print(f"✅ Character added: {character}")

    def add_decision(self, decision: str):
        """Record a decision made by the user"""
        self.decisions.append(decision)
        print(f"✅ Decision recorded: {decision}")

    def add_scene(self, scene_text: str, choice_made: str = None, image_url: str = None):
        """Add a completed scene to story history"""
        scene = {
            "turn"       : self.turn,
            "scene_text" : scene_text,
            "choice_made": choice_made,
            "image_url"  : image_url,
            "timestamp"  : datetime.now().isoformat()
        }
        self.full_scenes.append(scene)
        self.current_scene_text = scene_text
        self.turn += 1
        print(f"✅ Scene {self.turn} added to context")

    def update_location(self, location: str):
        """Update the current story location"""
        self.current_location = location

    def to_dict(self) -> dict:
        """Convert context to dictionary for storage"""
        return {
            "genre"           : self.genre,
            "protagonist"     : self.protagonist,
            "world_setting"   : self.world_setting,
            "tone"            : self.tone,
            "turn"            : self.turn,
            "is_ended"        : self.is_ended,
            "created_at"      : self.created_at,
            "characters"      : self.characters,
            "decisions"       : self.decisions,
            "current_location": self.current_location,
            "current_scene"   : self.current_scene_text,
            "full_scenes"     : self.full_scenes,
            "memory_summary"  : self.memory_summary
        }

    def get_story_summary(self) -> str:
        """Get a formatted summary of the story so far"""
        if not self.decisions:
            return "Story just started."

        summary = f"""
Genre         : {self.genre}
Protagonist   : {self.protagonist}
World         : {self.world_setting}
Location      : {self.current_location}
Characters    : {', '.join(self.characters)}
Turn          : {self.turn}
Decisions Made: {', '.join(self.decisions)}
Memory Summary: {self.memory_summary or 'None yet'}
        """.strip()

        return summary

    @classmethod
    def from_dict(cls, data: dict) -> "StoryContext":
        """Restore context from a dictionary"""
        ctx = cls(
            genre         = data["genre"],
            protagonist   = data["protagonist"],
            world_setting = data["world_setting"],
            tone          = data.get("tone", "dramatic")
        )
        ctx.turn             = data.get("turn", 0)
        ctx.is_ended         = data.get("is_ended", False)
        ctx.characters       = data.get("characters", [ctx.protagonist])
        ctx.decisions        = data.get("decisions", [])
        ctx.current_location = data.get("current_location", ctx.world_setting)
        ctx.current_scene_text = data.get("current_scene", "")
        ctx.full_scenes      = data.get("full_scenes", [])
        ctx.memory_summary   = data.get("memory_summary", "")
        return ctx