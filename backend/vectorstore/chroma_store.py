import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_openai import OpenAIEmbeddings
from config.settings import settings

class ChromaStore:
    def __init__(self):
        self.client = chromadb.HttpClient(
            host=settings.CHROMA_HOST, 
            port=settings.CHROMA_PORT,
            settings=ChromaSettings(allow_reset=True)
        )
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )
        
    def get_or_create_collection(self, name: str):
        return self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
        
    async def add_documents(self, collection_name: str, documents: list[str], metadatas: list[dict], ids: list[str]):
        collection = self.get_or_create_collection(collection_name)
        # ChromaDB automatically handles embeddings if we pass docs, but we explicitly generate them
        # if we want to ensure we're using OpenAI models consistently.
        # However, for speed in this implementation, we will let Chroma client handle or pass pre-embedded.
        # Let's generate embeddings manually for full control.
        embedded_docs = await self.embeddings.aembed_documents(documents)
        
        collection.add(
            embeddings=embedded_docs,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
    async def query(self, collection_name: str, query_text: str, n_results: int = 5) -> list[dict]:
        collection = self.get_or_create_collection(collection_name)
        query_embedding = await self.embeddings.aembed_query(query_text)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        formatted_results = []
        if results and results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "document": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results and results['distances'] else None
                })
                
        return formatted_results
        
    async def delete_collection(self, collection_name: str):
        try:
            self.client.delete_collection(name=collection_name)
        except Exception:
            pass
