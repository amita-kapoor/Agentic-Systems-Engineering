def search(
    self,
    query: str,
    top_k: int = 3,
    max_risk: RiskLevel = RiskLevel.CRITICAL,
) -> list[BaseTool]:
    """Return relevant tools after filtering by risk level."""
    if not self._tools:
        return []

    #A
    risk_order = list(RiskLevel)
    eligible = [
        (i, name)
        for i, name in enumerate(self._tool_names)
        if risk_order.index(self._tools[name].metadata.risk_level)
        <= risk_order.index(max_risk)
    ]

    if not eligible:
        return []

    #B
    indices, names = zip(*eligible)
    eligible_embs = self._embeddings[list(indices)]

    query_emb = self._model.encode(
        [query],
        normalize_embeddings=True,
    )[0]

    scores = np.dot(eligible_embs, query_emb)
    effective_k = min(top_k, len(eligible))
    top_local = np.argsort(scores)[-effective_k:][::-1]

    return [self._tools[names[i]] for i in top_local]


#A Step 1: Filter tools based on risk level.
#B Step 2: Perform semantic search on filtered tools.
