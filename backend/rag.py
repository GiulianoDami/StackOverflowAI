
from typing import List, Tuple
from backend.models import QuestionAnswer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

class Retriever:
    """
    Retrieves relevant Q&A from local DB based on query embedding similarity.
    """

    def __init__(self, db_session):
        self.db_session = db_session
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def _compute_embeddings(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True)

    def retrieve(self, query: str, top_k: int = 5) -> List[QuestionAnswer]:
        # Fetch all questions in DB
        qas = self.db_session.query(QuestionAnswer).all()
        if not qas:
            return []

        texts = [qa.question_title + " " + (qa.question_body or "") for qa in qas]
        embeddings = self._compute_embeddings(texts)
        query_emb = self._compute_embeddings([query])[0]

        similarities = cosine_similarity([query_emb], embeddings)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]

        return [qas[idx] for idx in top_indices if similarities[idx] > 0.2]  # threshold to filter low sim


class Generator:
    """
    Uses LLM API (e.g., OpenAI) to generate answers based on retrieved contexts.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        import openai
        openai.api_key = self.api_key
        self.openai = openai

    def generate_answer(self, question: str, contexts: List[QuestionAnswer]) -> Tuple[str, List[int]]:
        """
        Generate an AI answer by providing the question and contexts as prompts.
        Returns generated answer and list of source IDs for attribution.
        """
        context_texts = []
        source_ids = []
        for ctx in contexts:
            combined = f"Q: {ctx.question_title}\nA: {ctx.answer_body}\n"
            context_texts.append(combined)
            source_ids.append(ctx.id)

        # Construct prompt with retrieved contexts
        prompt = "You are a helpful software development assistant. Use the following verified StackOverflow Q&A to answer user question. Cite the sources by ID.\n\n"
        prompt += "\n---\n".join(context_texts)
        prompt += f"\n\nUser Question: {question}\nAnswer:"

        # call OpenAI completion
        response = self.openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=256,
            temperature=0.2,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        answer = response.choices[0].text.strip()
        return answer, source_ids
```

```plaintext
