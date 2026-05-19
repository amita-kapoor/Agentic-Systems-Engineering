import math


def prune(memory, now, budget):
    def utility(item):
        # A
        half_life = 14 * 24 * 3600 if item.kind == "episodic" else 90 * 24 * 3600
        decay = decay_weight(item, now, half_life)
        frequency = math.log1p(item.access_count)

        return (
            0.5 * item.importance +  # what must be retained
            0.3 * decay +           # what is still relevant
            0.2 * frequency         # what has proven useful
        )

    memory_sorted = sorted(memory, key=utility, reverse=True)

    return memory_sorted[:budget]


# A Use the same decay logic as retrieval, but with a longer half-life
