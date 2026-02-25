from pydantic import BaseModel
from typing import List, Optional


class StartStoryResponse(BaseModel):
    """Response for starting a new story"""
    success    : bool
    session_id : str
    scene_text : str
    choices    : List[str]
    image_url  : Optional[str] = None
    turn       : int = 1
    message    : str = "Story started successfully!"

    class Config:
        json_schema_extra = {
            "example": {
                "success"   : True,
                "session_id": "abc123xyz",
                "scene_text": "You stand at the edge of the dark forest...",
                "choices"   : [
                    "A) Enter the forest carefully",
                    "B) Rush into the forest boldly",
                    "C) Look for another way around"
                ],
                "image_url" : "data:image/jpeg;base64,...",
                "turn"      : 1,
                "message"   : "Story started successfully!"
            }
        }


class MakeChoiceResponse(BaseModel):
    """Response for making a story choice"""
    success    : bool
    session_id : str
    scene_text : str
    choices    : Optional[List[str]] = None
    image_url  : Optional[str] = None
    turn       : int
    is_ending  : bool = False
    outcome    : Optional[str] = None
    message    : str = "Scene generated successfully!"

    class Config:
        json_schema_extra = {
            "example": {
                "success"   : True,
                "session_id": "abc123xyz",
                "scene_text": "You step into the dark forest...",
                "choices"   : [
                    "A) Follow the strange light",
                    "B) Hide behind a tree",
                    "C) Call out into the darkness"
                ],
                "image_url" : "data:image/jpeg;base64,...",
                "turn"      : 2,
                "is_ending" : False,
                "outcome"   : None,
                "message"   : "Scene generated successfully!"
            }
        }


class EndStoryResponse(BaseModel):
    """Response for story ending"""
    success    : bool
    session_id : str
    scene_text : str
    image_url  : Optional[str] = None
    outcome    : str
    turn       : int
    is_ending  : bool = True
    message    : str = "Story completed!"

    class Config:
        json_schema_extra = {
            "example": {
                "success"   : True,
                "session_id": "abc123xyz",
                "scene_text": "Your journey comes to an end...",
                "image_url" : "data:image/jpeg;base64,...",
                "outcome"   : "Hero",
                "turn"      : 10,
                "is_ending" : True,
                "message"   : "Story completed!"
            }
        }


class ExportResponse(BaseModel):
    """Response for PDF export"""
    success  : bool
    file_path: str
    message  : str = "Story exported successfully!"

    class Config:
        json_schema_extra = {
            "example": {
                "success"  : True,
                "file_path": "exports/story_abc123xyz.pdf",
                "message"  : "Story exported successfully!"
            }
        }


class ErrorResponse(BaseModel):
    """Generic error response"""
    success: bool = False
    error  : str
    message: str = "Something went wrong!"

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error"  : "Session not found",
                "message": "Something went wrong!"
            }
        }