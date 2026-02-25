from pydantic import BaseModel, Field
from typing import Optional


class StartStoryRequest(BaseModel):
    """Request body for starting a new story"""
    genre        : str = Field(
        ...,
        description="Story genre",
        examples=["fantasy", "horror", "romance", "scifi", "mystery", "adventure"]
    )
    protagonist  : str = Field(
        ...,
        description="Name of the main character",
        examples=["Aria", "John", "Luna"]
    )
    world_setting: str = Field(
        ...,
        description="Description of the story world",
        examples=["Medieval kingdom under dark curse", "Post-apocalyptic city"]
    )
    tone         : Optional[str] = Field(
        default="dramatic",
        description="Story tone",
        examples=["dramatic", "dark", "lighthearted", "mysterious"]
    )
    user_id      : Optional[str] = Field(
        default="anonymous",
        description="Optional user ID"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "genre"        : "fantasy",
                "protagonist"  : "Aria",
                "world_setting": "Medieval kingdom under a dark curse",
                "tone"         : "dramatic",
                "user_id"      : "user_001"
            }
        }


class MakeChoiceRequest(BaseModel):
    """Request body for making a story choice"""
    session_id: str = Field(
        ...,
        description="Active session ID from start story response"
    )
    choice    : str = Field(
        ...,
        description="The choice made by the user",
        examples=["A) Enter the dark forest", "B) Turn back to the village"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "abc123xyz",
                "choice"    : "A) Enter the dark forest"
            }
        }


class ExportStoryRequest(BaseModel):
    """Request body for exporting story to PDF"""
    session_id: str = Field(
        ...,
        description="Session ID of the story to export"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "abc123xyz"
            }
        }