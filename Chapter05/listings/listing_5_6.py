from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer


class ToolRegistry:
    def __init__(self, model: SentenceTransformer):
        self._tools: dict[str, BaseTool] = {}
        self._tool_names: list[str] = []
        self._embeddings: Optional[np.ndarray] = None
        self._model: SentenceTransformer = model

    def register(
        self, tool: BaseTool
    ) -> None:  # Add a new tool and store its description embedding
        name = tool.metadata.name
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered. Use update() to replace it.")

        self._tools[name] = tool
        self._tool_names.append(name)

        new_emb = self._model.encode(
            [tool.metadata.description],
            normalize_embeddings=True,
        )
        self._embeddings = (
            new_emb if self._embeddings is None else np.vstack([self._embeddings, new_emb])
        )

    def get(self, name: str) -> Optional[BaseTool]:  # Look up a tool by name
        return self._tools.get(name)

    def search(
        self, query: str, top_k: int = 3
    ) -> list[BaseTool]:  # Return the most relevant candidate tools for a query
        if not self._tools:
            return []

        query_emb = self._model.encode(
            [query],
            normalize_embeddings=True,
        )[0]

        scores = np.dot(self._embeddings, query_emb)
        effective_k = min(top_k, len(self._tools))
        top_indices = np.argsort(scores)[-effective_k:][::-1]

        return [self._tools[self._tool_names[i]] for i in top_indices]
