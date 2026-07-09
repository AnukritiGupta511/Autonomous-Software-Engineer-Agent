import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.chat import Chat, ChatMessage
from schemas.chat import ChatMessageResponse
from config.settings import settings


class ChatService:
    @staticmethod
    async def process_message(
        chat_id: str,
        user_message_content: str,
        user_id: str,
        db: AsyncSession
    ) -> ChatMessageResponse:

        # 1. Verify chat exists and belongs to user
        stmt = select(Chat).where(Chat.id == str(chat_id), Chat.user_id == str(user_id))
        result = await db.execute(stmt)
        chat = result.scalar_one_or_none()
        if not chat:
            raise ValueError("Chat not found")

        # 2. Save user message
        user_msg = ChatMessage(
            chat_id=str(chat_id),
            role="user",
            content=user_message_content
        )
        db.add(user_msg)
        await db.commit()

        # 3. Get AI response
        assistant_content = await ChatService._get_ai_response(
            user_message_content, str(chat_id), db
        )

        # 4. Save assistant message
        assistant_msg = ChatMessage(
            chat_id=str(chat_id),
            role="assistant",
            content=assistant_content
        )
        db.add(assistant_msg)
        await db.commit()
        await db.refresh(assistant_msg)

        return ChatMessageResponse(
            id=str(assistant_msg.id),
            role=assistant_msg.role,
            content=assistant_msg.content,
            metadata_json=assistant_msg.metadata_json,
            created_at=assistant_msg.created_at
        )

    @staticmethod
    async def _get_ai_response(user_message: str, chat_id: str, db: AsyncSession) -> str:
        api_key = settings.OPENAI_API_KEY

        # Use mock if no API key
        if not api_key or api_key.strip() == "" or api_key == "your-openai-api-key-here":
            return ChatService._mock_response(user_message)

        # Try real OpenAI call
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

            # Fetch recent history (last 10 messages)
            history_stmt = (
                select(ChatMessage)
                .where(ChatMessage.chat_id == chat_id)
                .order_by(ChatMessage.created_at.desc())
                .limit(10)
            )
            history_result = await db.execute(history_stmt)
            history = list(reversed(history_result.scalars().all()))

            messages = [
                SystemMessage(content=(
                    "You are an expert AI Software Engineer Agent. "
                    "You help users understand code, build features, fix bugs, and manage repositories. "
                    "Be concise, helpful, and professional."
                ))
            ]
            for msg in history:
                if msg.role == "user":
                    messages.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    messages.append(AIMessage(content=msg.content))

            llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0.7)
            response = await llm.ainvoke(messages)
            return response.content

        except Exception as e:
            return f"⚠️ AI error: {str(e)}\n\nPlease check your OpenAI API key in `backend/.env`."

    @staticmethod
    def _mock_response(user_message: str) -> str:
        msg = user_message.lower().strip()
        if any(w in msg for w in ["hello", "hi", "hey", "helo"]):
            return (
                "👋 Hello! I'm your **AI Software Engineer Agent**.\n\n"
                "I'm currently running in **offline mode** — no OpenAI key detected.\n\n"
                "To enable real AI responses, add this to `backend/.env`:\n"
                "```\nOPENAI_API_KEY=sk-your-key-here\n```\n\n"
                "I can help you with:\n"
                "- 🔍 **Code review** and bug fixing\n"
                "- 🚀 **Feature generation**\n"
                "- 📁 **Repository analysis**\n"
                "- 📝 **Documentation generation**"
            )
        elif any(w in msg for w in ["help", "what can you do", "features"]):
            return (
                "Here's what I can do:\n\n"
                "1. **Analyze repositories** — understand code structure and architecture\n"
                "2. **Review code** — find bugs, security issues, and improvements\n"
                "3. **Generate features** — write new code matching your project style\n"
                "4. **Fix bugs** — diagnose and fix errors with explanations\n"
                "5. **Write docs** — generate README, API docs, architecture guides\n\n"
                "_Add your OpenAI API key to enable real AI responses._"
            )
        else:
            return (
                f"📨 I received your message: *\"{user_message}\"*\n\n"
                "I'm running in **offline mode**. To get real AI responses, "
                "add your `OPENAI_API_KEY` to `backend/.env` and restart the server."
            )
