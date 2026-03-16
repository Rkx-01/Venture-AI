"""
services/idea_similarity_service.py
-----------------------------------
Generates embeddings and checks for semantic duplicates using pgvector.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.llm_client import get_openai_client
from app.exceptions import ConflictError, ExternalServiceError
from app.models.startup_idea import StartupIdea
from app.utils.logger import get_logger

logger = get_logger(__name__)


class IdeaSimilarityService:
    """
    Handles converting text to vector embeddings and querying the database 
    for semantic duplicates.
    """

    def __init__(self, session: AsyncSession, embedding_model: str = "text-embedding-3-small"):
        self.session = session
        self.embedding_model = embedding_model
        self.client = get_openai_client()

    async def generate_embedding(self, text: str) -> list[float]:
        """
        Calls OpenAI to generate a vector embedding for the given text.
        """
        from app.config.settings import settings
        if settings.USE_MOCK_DB:
            logger.info("USE_MOCK_DB is enabled; returning dummy zero-vector embedding.")
            return [0.0] * 1536  # Default dimension for text-embedding-3-small

        try:
            logger.debug("Generating embedding for text (length: %d)", len(text))
            
            # OpenAI requires relatively clean text, stripped of large newlines
            clean_text = text.replace("\n", " ")
            response = await self.client.embeddings.create(
                input=[clean_text],
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error("Failed to generate embedding: %s", str(e))
            raise ExternalServiceError(
                "Failed to generate AI embedding for similarity check.",
                provider="openai_embeddings"
            ) from e

    async def check_for_duplicates(self, idea_text: str, similarity_threshold: float = 0.85) -> list[float]:
        """
        Generates an embedding for the idea, checks the database for existing 
        ideas with high cosine similarity, and prevents duplicates.
        
        Args:
            idea_text: The incoming startup idea.
            similarity_threshold: Cosine similarity cutoff (e.g., 0.85 means very similar).
            
        Returns:
            The generated embedding, so the caller can save it to the DB without re-calculating.
            
        Raises:
            ConflictError: If a similar idea already exists above the threshold.
        """
        # 1. Create vector from input
        embedding = await self.generate_embedding(idea_text)

        # 2. pgvector's cosine distance operator is `<=>`.
        # Cosine Distance = 1 - Cosine Similarity.
        # So we look for items where distance < (1 - threshold).
        max_distance = 1.0 - similarity_threshold

        query = (
            select(StartupIdea)
            .where(StartupIdea.embedding is not None)  # Only check rows with embeddings
            .where(StartupIdea.embedding.cosine_distance(embedding) < max_distance)  # type: ignore
        )

        result = await self.session.execute(query)
        duplicate = result.scalars().first()

        if duplicate:
            # We explicitly cast to avoid lsp warnings since the query guarantees it's populated
            duplicate_text = duplicate.idea_text[:100] + "..." 
            logger.warning(
                "Duplicate startup idea detected. Conflict with ID %s", duplicate.id,
            )
            raise ConflictError(
                "Similar startup idea already exists.",
                existing_idea_preview=duplicate_text
            )

        # 3. If no duplicates, return the embedding so the API can save it
        return embedding
