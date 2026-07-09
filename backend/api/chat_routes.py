from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from db.database import get_db
from models.user import User
from models.chat import Chat, ChatMessage
from schemas.chat import ChatCreate, ChatResponse, ChatMessageCreate, ChatMessageResponse
from auth.dependencies import get_current_user
from services.chat_service import ChatService

router = APIRouter(prefix="/api/chats", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def create_chat(
    chat_in: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    title = chat_in.title or "New Chat"
    new_chat = Chat(
        user_id=str(current_user.id),
        repository_id=str(chat_in.repository_id) if chat_in.repository_id else None,
        title=title
    )
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    return ChatResponse(
        id=new_chat.id,
        title=new_chat.title,
        repository_id=new_chat.repository_id,
        messages=[],
        created_at=new_chat.created_at
    )

@router.get("/", response_model=List[ChatResponse])
async def list_chats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Chat).where(Chat.user_id == str(current_user.id)).order_by(Chat.created_at.desc())
    result = await db.execute(stmt)
    chats = result.scalars().all()
    return [
        ChatResponse(id=c.id, title=c.title, repository_id=c.repository_id, messages=[], created_at=c.created_at)
        for c in chats
    ]

@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Chat).where(Chat.id == chat_id, Chat.user_id == str(current_user.id))
    result = await db.execute(stmt)
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    msg_stmt = select(ChatMessage).where(ChatMessage.chat_id == chat_id).order_by(ChatMessage.created_at.asc())
    msg_result = await db.execute(msg_stmt)
    messages = msg_result.scalars().all()

    msg_responses = [
        ChatMessageResponse(id=m.id, role=m.role, content=m.content, metadata_json=m.metadata_json, created_at=m.created_at)
        for m in messages
    ]
    return ChatResponse(id=chat.id, title=chat.title, repository_id=chat.repository_id, messages=msg_responses, created_at=chat.created_at)

@router.post("/{chat_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    chat_id: str,
    msg_in: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        response = await ChatService.process_message(
            chat_id=chat_id,
            user_message_content=msg_in.content,
            user_id=str(current_user.id),
            db=db
        )
        # Update chat updated_at
        chat_stmt = select(Chat).where(Chat.id == chat_id)
        chat_result = await db.execute(chat_stmt)
        chat = chat_result.scalar_one_or_none()
        if chat:
            chat.updated_at = datetime.utcnow()
            await db.commit()
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{chat_id}", status_code=204)
async def delete_chat(
    chat_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Chat).where(Chat.id == chat_id, Chat.user_id == str(current_user.id))
    result = await db.execute(stmt)
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    await db.delete(chat)
    await db.commit()
