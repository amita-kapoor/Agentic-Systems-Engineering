from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer

MIN_SIMILARITY = 0.40 #A


class ToolRegistry:
    def __init__(self, model: SentenceTransformer):
        self._tools: dict[str, BaseTool] = {}
        self._tool_names: list[str] = []
        self._embeddings: Optional[np.ndarray] = None
        self._model = SentenceTransformer("all-MiniLM-L6-v2") #B

    def register(self, tool: BaseTool) -> None:  #C
        name = tool.metadata.name
        if name in self._tools:
            raise ValueError(
                f"Tool '{name}' is already registered. Use update() to replace it."
            )

        self._tools[name] = tool
        self._tool_names.append(name)

        new_emb = self._model.encode(
            [tool.metadata.description],
            normalize_embeddings=True,
        )
        self._embeddings = (
            new_emb
            if self._embeddings is None
            else np.vstack([self._embeddings, new_emb])
        )

    def get(self, name: str) -> Optional[BaseTool]:  #D
        return self._tools.get(name)

    def search(self, query: str, top_k: int = 3, min_similarity: float = MIN_SIMILARITY,) -> list[BaseTool]:  #E
        if not self._tools:
            return []

        query_emb = self._model.encode(
            [query],
            normalize_embeddings=True,
        )[0]

        scores = np.dot(self._embeddings, query_emb)
        ranked = np.argsort(scores)[::-1][:top_k]

        return [
            self._tools[self._tool_names[i]]
            for i in ranked
            if scores[i] >= min_similarity #F
        ]

#A Calibrated for all-MiniLM-L6-v2 and the tool descriptions in this chapter. Recalibrate for your own. 
#B The registry loads its own embedding model, so ToolRegistry() needs no argument
#C Add a new tool and store its description embedding.
#D Look up a tool by name.
#E Return the most relevant candidate tools for a query.
#F An empty list is a valid answer: nothing registered fits the request
