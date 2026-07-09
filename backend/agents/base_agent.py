from abc import ABC, abstractmethod
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from config.settings import settings

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm = self._get_llm()
    
    def _get_llm(self) -> BaseChatModel:
        if settings.LLM_PROVIDER == 'openai':
            return ChatOpenAI(
                model='gpt-4o',
                api_key=settings.OPENAI_API_KEY,
                temperature=0.1
            )
        else:
            from langchain_community.chat_models import ChatOllama
            return ChatOllama(model='llama3', base_url=settings.OLLAMA_BASE_URL, temperature=0.1)
    
    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's core logic with the given input data."""
        pass
    
    def get_system_prompt(self) -> str:
        return f"You are an expert AI agent named '{self.name}'. {self.description}"
