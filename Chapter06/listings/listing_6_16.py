@dataclass
class EpisodicRecord:
    task_signature: str  # Short label for the kind of task
    outcome: Literal["success", "failure"]
    insight: str  # what the agent learned
    timestamp: float = field(default_factory=time.time)


class EpisodicMemory:
    """Distilled records from past tasks. Grows over time, retrieved selectively."""

    def __init__(self) -> None:
        self._records: list[EpisodicRecord] = []

    def store(self, record: EpisodicRecord) -> None:
        self._records.append(record)

    def retrieve(self, task_signature: str, k: int = 3) -> list[EpisodicRecord]:
        """Score records by token overlap with the task signature."""
        if not self._records:
            return []
        query_tokens = set(task_signature.lower().split())
        scored = []
        for rec in self._records:
            rec_tokens = set(rec.task_signature.lower().split())
            overlap = len(query_tokens & rec_tokens)
            scored.append((overlap, rec))
        scored.sort(key=lambda x: (-x[0], -x[1].timestamp))
        return [rec for score, rec in scored[:k] if score > 0]

    def as_prompt_block(self, records: list[EpisodicRecord]) -> str:
        if not records:
            return "No relevant past experience."
        return "\n".join(f"- [{r.outcome}] {r.task_signature}: {r.insight}" for r in records)


MEMORY = EpisodicMemory()
print("Episodic memory initialized. Currently empty.")
