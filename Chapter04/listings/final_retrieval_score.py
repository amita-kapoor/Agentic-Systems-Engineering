def final_retrieval_score(similarity, item, now):
    if is_suppressed(item, now):
        return 0.0

    decay = decay_weight(item, now, 7 * 24 * 3600)

    return similarity * decay * (0.5 + 0.5 * item.importance)
