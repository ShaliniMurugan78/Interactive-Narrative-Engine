from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Scene(BaseModel):
    """Represents a single story scene"""
    turn        : int
    scene_text  : str
    choices_given: List[str] = []
    user_choice : Optional[str] = None
    image_url   : Optional[str] = None
    timestamp   : str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class Story(BaseModel):
    """Represents a complete story session"""
    session_id    : str
    user_id       : Optional[str] = "anonymous"
    genre         : str
    protagonist   : str
    world_setting : str
    tone          : str = "dramatic"
    status        : str = "ongoing"   # ongoing | completed
    turn_count    : int = 0
    characters    : List[str] = []
    decisions     : List[str] = []
    scenes        : List[Scene] = []
    memory_summary: str = ""
    outcome       : Optional[str] = None
    final_ending  : Optional[str] = None
    created_at    : str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )
    updated_at    : str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class Session(BaseModel):
    """Represents an active game session (temporary storage)"""
    session_id    : str
    story_id      : str
    last_active   : str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )
    current_turn  : int = 0
    context       : dict = {}
    is_active     : bool = True