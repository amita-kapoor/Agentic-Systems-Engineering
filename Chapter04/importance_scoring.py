def update_importance(item, signal):
    if signal.get("user_confirmed"):
        item.importance += 0.1

    if signal.get("used_in_success"):
        item.importance += 0.05

    if signal.get("user_corrected"):
        item.importance -= 0.3

    if signal.get("used_in_failure"):
        item.importance -= 0.1

    item.importance = min(1.0, max(0.0, item.importance))
