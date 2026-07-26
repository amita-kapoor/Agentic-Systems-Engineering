def episodic_reset(memory, keep_recent=0):
    episodic = [m for m in memory if m.kind == "episodic"]

    non_episodic = [m for m in memory if m.kind != "episodic"]

    episodic_sorted = sorted(episodic, key=lambda m: m.created_at, reverse=True)

    kept = episodic_sorted[:keep_recent]
    archived = episodic_sorted[keep_recent:]

    return non_episodic + kept, archived
