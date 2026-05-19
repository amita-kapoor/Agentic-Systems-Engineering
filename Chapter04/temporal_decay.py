def decay_weight(item, now, half_life_seconds):
    age = max(0.0, now - item.created_at)

    return 0.5 ** (age / half_life_seconds)


def time_adjusted_score(similarity, item, now):
    half_life = 7 * 24 * 3600 if item.kind == "episodic" else 30 * 24 * 3600

    return similarity * decay_weight(item, now, half_life)
