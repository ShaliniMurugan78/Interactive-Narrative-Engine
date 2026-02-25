import uuid
from fastapi import APIRouter, HTTPException
from app.models.request_model import StartStoryRequest, MakeChoiceRequest
from app.models.response_model import (
    StartStoryResponse,
    MakeChoiceResponse,
    ErrorResponse
)
from app.core.context_manager import StoryContext
from app.core.scene_generator import generate_opening_scene, generate_next_scene
from app.core.choice_generator import generate_choices
from app.core.ending_detector import should_end_story, generate_ending, get_story_outcome
from app.core.memory_manager import update_memory
from app.services.image_service import generate_image, extract_image_prompt
from app.services.llm_service import call_llm
from app.database.db import get_sessions_collection, get_stories_collection
from app.prompts.image_prompt import build_image_generation_prompt
import json

router = APIRouter(prefix="/story", tags=["Story"])

# In-memory session store (fast access)
active_sessions = {}


# ─────────────────────────────────────────
# POST /story/start
# ─────────────────────────────────────────
@router.post("/start", response_model=StartStoryResponse)
async def start_story(request: StartStoryRequest):
    """
    Start a new interactive story.
    Creates context, generates opening scene and first choices.
    """
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())[:8]

        # Create story context
        context = StoryContext(
            genre         = request.genre,
            protagonist   = request.protagonist,
            world_setting = request.world_setting,
            tone          = request.tone or "dramatic"
        )

        # Generate opening scene
        scene_text = generate_opening_scene(context)

        # Generate choices
        choices = generate_choices(context, scene_text)

        # Generate scene image
        image_prompt     = extract_image_prompt(scene_text)
        full_image_prompt = build_image_generation_prompt(image_prompt, request.genre)
        image_url        = generate_image(full_image_prompt)

        # Add scene to context
        context.add_scene(
            scene_text = scene_text,
            image_url  = image_url
        )

        # Save context to in-memory session store
        active_sessions[session_id] = context.to_dict()

        # Save to MongoDB
        stories_col = get_stories_collection()
        story_doc = {
            "session_id"   : session_id,
            "user_id"      : request.user_id,
            "genre"        : request.genre,
            "protagonist"  : request.protagonist,
            "world_setting": request.world_setting,
            "tone"         : request.tone,
            "status"       : "ongoing",
            "turn_count"   : 1,
            "characters"   : context.characters,
            "decisions"    : [],
            "scenes"       : context.full_scenes,
            "memory_summary": "",
            "outcome"      : None,
            "final_ending" : None
        }
        await stories_col.insert_one(story_doc)

        print(f"✅ Story started | Session: {session_id} | Genre: {request.genre}")

        return StartStoryResponse(
            success    = True,
            session_id = session_id,
            scene_text = scene_text,
            choices    = choices,
            image_url  = image_url,
            turn       = 1,
            message    = "Story started successfully!"
        )

    except Exception as e:
        print(f"❌ Start story failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# POST /story/choose
# ─────────────────────────────────────────
@router.post("/choose", response_model=MakeChoiceResponse)
async def make_choice(request: MakeChoiceRequest):
    """
    Make a choice and get the next story scene.
    Handles both mid-story scenes and story endings.
    """
    try:
        # Get session from memory
        session_data = active_sessions.get(request.session_id)
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail=f"Session {request.session_id} not found"
            )

        # Restore context from session
        context = StoryContext.from_dict(session_data)

        # Record the decision
        context.add_decision(request.choice)

        # Update memory (summarize old scenes)
        context = update_memory(context)

        # Check if story should end
        if should_end_story(context):
            # Generate ending
            ending_text = generate_ending(context)
            outcome     = get_story_outcome(context)

            # Generate ending image
            image_prompt      = extract_image_prompt(ending_text)
            full_image_prompt = build_image_generation_prompt(
                image_prompt, context.genre
            )
            image_url = generate_image(full_image_prompt)

            # Add ending scene to context
            context.add_scene(
                scene_text  = ending_text,
                choice_made = request.choice,
                image_url   = image_url
            )
            context.is_ended = True

            # Update session
            active_sessions[request.session_id] = context.to_dict()

            # Update MongoDB
            stories_col = get_stories_collection()
            await stories_col.update_one(
                {"session_id": request.session_id},
                {"$set": {
                    "status"      : "completed",
                    "turn_count"  : context.turn,
                    "decisions"   : context.decisions,
                    "scenes"      : context.full_scenes,
                    "outcome"     : outcome,
                    "final_ending": ending_text
                }}
            )

            print(f"✅ Story ended | Session: {request.session_id} | Outcome: {outcome}")

            return MakeChoiceResponse(
                success    = True,
                session_id = request.session_id,
                scene_text = ending_text,
                choices    = None,
                image_url  = image_url,
                turn       = context.turn,
                is_ending  = True,
                outcome    = outcome,
                message    = f"Story completed! Outcome: {outcome}"
            )

        # Generate next scene
        scene_text = generate_next_scene(context, request.choice)

        # Generate choices for next scene
        choices = generate_choices(context, scene_text)

        # Generate scene image
        image_prompt      = extract_image_prompt(scene_text)
        full_image_prompt = build_image_generation_prompt(
            image_prompt, context.genre
        )
        image_url = generate_image(full_image_prompt)

        # Add scene to context
        context.add_scene(
            scene_text  = scene_text,
            choice_made = request.choice,
            image_url   = image_url
        )

        # Update session
        active_sessions[request.session_id] = context.to_dict()

        # Update MongoDB
        stories_col = get_stories_collection()
        await stories_col.update_one(
            {"session_id": request.session_id},
            {"$set": {
                "turn_count"   : context.turn,
                "decisions"    : context.decisions,
                "scenes"       : context.full_scenes,
                "memory_summary": context.memory_summary
            }}
        )

        print(f"✅ Choice made | Session: {request.session_id} | Turn: {context.turn}")

        return MakeChoiceResponse(
            success    = True,
            session_id = request.session_id,
            scene_text = scene_text,
            choices    = choices,
            image_url  = image_url,
            turn       = context.turn,
            is_ending  = False,
            message    = "Scene generated successfully!"
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Make choice failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# GET /story/{session_id}
# ─────────────────────────────────────────
@router.get("/{session_id}")
async def get_story(session_id: str):
    """Get current story state by session ID"""
    try:
        stories_col = get_stories_collection()
        story = await stories_col.find_one(
            {"session_id": session_id},
            {"_id": 0}
        )

        if not story:
            raise HTTPException(
                status_code=404,
                detail=f"Story {session_id} not found"
            )

        return {"success": True, "story": story}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))