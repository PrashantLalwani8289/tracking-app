import asyncio
import base64
from datetime import datetime
import json
import os
from typing import Union
from fastapi import APIRouter, Depends, Query, WebSocket
from fastapi import WebSocketDisconnect
from fastapi.websockets import WebSocketState
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from pydantic import BaseModel
from fastapi_csrf_protect import CsrfProtect


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, websocket: WebSocket, message: int):
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_text(message)

    async def broadcast(self, message: int):
        for connection in self.active_connections:
            if connection.client_state == WebSocketState.CONNECTED:
                await connection.send_text(json.dumps(message))


manager = ConnectionManager()


class CsrfSettings(BaseModel):
    secret_key: str = "your-secret-key"


# Ensure the limiter is imported from the app state
limiter = Limiter(key_func=get_remote_address)

# from fastapi import File, UploadFile, HTTPException
from pydantic import BaseModel
from app.features.blog.repository import (
    add_comment,
    create_blog,
    get_all_blogs,
    get_all_blogs_by_category,
    get_all_comments,
    get_blog,
    get_destination_summary,
    get_is_liked,
    get_likes,
    get_top_3_blogs,
    handle_reaction,
)
from app.features.blog.schemas import (
    CommentSchema,
    CreateBlog,
    Destination,
    GetLikes,
    LikeSchema,
)
from app.utils.routes import routes
from sqlalchemy.orm import Session

# import whisper
# import warnings
# import io
# from pydub import AudioSegment
# import numpy as np

# warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
from app.common.schemas import ResponseModal
from app.database import db_connection

from app.utils.oauth import is_user_authorised

blogRouter = APIRouter(prefix=routes.BLOG)

# Convert to float32


# model = whisper.load_model("base")
# model = model.float()


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@blogRouter.post(routes.CREATE_BLOG, response_model=ResponseModal)
async def create_new_blog(
    request: CreateBlog,
    db: Session = Depends(db_connection),
    currentUser: dict = Depends(is_user_authorised),
):
    return await create_blog(request, db, currentUser)


@blogRouter.get(routes.GET_BLOG, response_model=ResponseModal)
async def get_the_blog(
    BlogId: Union[int, str] = Query(-1, description="Enter the blog id"),
    db: Session = Depends(db_connection),
):
    return await get_blog(BlogId, db)


@blogRouter.get(routes.GET_ALL_BLOG, response_model=ResponseModal)
# @limiter.limit("5/minute")
async def get_the_blog(
    request: Request,
    db: Session = Depends(db_connection),
    # csrf_protect: CsrfProtect = Depends(),
):
    return await get_all_blogs(db)


@blogRouter.get(routes.GET_TOP_3_BLOGS, response_model=ResponseModal)
async def get_the_blog(db: Session = Depends(db_connection)):
    return await get_top_3_blogs(db)


@blogRouter.get(routes.GET_ALL_BLOG_BY_CATEGORY, response_model=ResponseModal)
async def get_the_blog(
    category: str = Query("all"), db: Session = Depends(db_connection)
):
    return await get_all_blogs_by_category(category, db)


@blogRouter.post(routes.HANDLE_REACTION, response_model=ResponseModal)
async def handle_like(
    request: LikeSchema,
    db: Session = Depends(db_connection),
    currentUser: dict = Depends(is_user_authorised),
):
    return await handle_reaction(request, db, currentUser)


@blogRouter.post(routes.IS_LIKED, response_model=ResponseModal)
async def is_liked_by_me(
    request: GetLikes,
    db: Session = Depends(db_connection),
    currentUser: dict = Depends(is_user_authorised),
):
    return await get_is_liked(request, db, currentUser)


@blogRouter.websocket(routes.GET_LIKES)
async def return_likes(
    websocket: WebSocket,
):
    await manager.connect(websocket)
    while len(manager.active_connections) > 0:
        likes = get_likes()
        print(likes)
        await manager.broadcast(likes)
        await asyncio.sleep(5)


@blogRouter.post(routes.ADD_COMMENT, response_model=ResponseModal)
async def add_new_comment(
    request: CommentSchema,
    db: Session = Depends(db_connection),
    currentUser: dict = Depends(is_user_authorised),
):
    return await add_comment(request, db, currentUser)


@blogRouter.get(routes.GET_COMMENTS, response_model=ResponseModal)
async def get_comments(
    blog_id: Union[int, str] = Query(-1),
    comment_id: Union[int, str] = Query(-1),
    db: Session = Depends(db_connection),
):
    return await get_all_comments(blog_id, comment_id, db)


@blogRouter.post(routes.GET_AUTO_BLOGS, response_model=ResponseModal)
async def get_comments(
    request: Destination,
    db: Session = Depends(db_connection),
    currentUser: dict = Depends(is_user_authorised),
):
    return await get_destination_summary(request, db, currentUser)


@blogRouter.post("/transcribe", response_model=ResponseModal)
async def get_comments(
    request: Destination,
    db: Session = Depends(db_connection),
    currentUser: dict = Depends(is_user_authorised),
):
    return await get_destination_summary(request, db, currentUser)


# class TranscriptResponse(BaseModel):
#     transcript: str


# def convert_audio_to_text(audio_file_path):
#     # wav_file_path = convert_audio_to_wav(audio_file_path)

#     result = model.transcribe(audio_file_path)
#     text = result["text"]

#     # if os.path.exists(wav_file_path):
#     #     os.remove(wav_file_path)

#     return text


# class AudioInput(BaseModel):
#     audio: str


# def fix_base64_padding(data):
#     missing_padding = len(data) % 4
#     if missing_padding:
#         data += "=" * (4 - missing_padding)
#     return data


# @blogRouter.post("/transcribe-audio", response_model=ResponseModal)
# async def transcribe_audio(audio_input: AudioInput):
#     try:
#         print(audio_input.audio[21:], "audio_input")

#         audio_data = base64.b64decode(audio_input.audio[21:])

#         # mp3_file_path = "temp_audio.mp3"
#         # async with aiofiles.open(mp3_file_path, "wb") as mp3_file:
#         #     await mp3_file.write(audio_data)

#         mp3_file_path = os.path.join(os.getcwd(), rf"app\features\blog\temp_audio.mp3")
#         with open(mp3_file_path, "wb") as mp3_file:
#             mp3_file.write(audio_data)
#         print(mp3_file_path)

#         text = convert_audio_to_text(mp3_file_path)

#         # if os.path.exists(mp3_file_path):
#         #     os.remove(mp3_file_path)
#         print(text, "text")

#         return {
#             "message": "Destination summary fetched successfully",
#             "success": True,
#             "data": text,
#         }
#     except Exception as e:
#         print(e)
#         return {
#             "message": "An error occurred while fetching the destination summary",
#             "success": False,
#         }


# @blogRouter.websocket("/ws/transcribe-websocket")
# async def websocket_transcribe(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             # Receive audio data (Base64-encoded)
#             data = await websocket.receive_text()
#             audio_data = base64.b64decode(data)

#             # Save the audio file temporarily
#             mp3_file_path = os.path.join(os.getcwd(), "temp_audio.mp3")
#             with open(mp3_file_path, "wb") as mp3_file:
#                 mp3_file.write(audio_data)

#             # Process the audio file
#             text = convert_audio_to_text(mp3_file_path)
#             print(text)

#             await websocket.send_text(text)
#     except Exception as e:
#         print(f"WebSocket error: {e}")
#         await websocket.close()
