def suppress(item, seconds):
    item.suppressed_until = time.time() + seconds


def is_suppressed(item, now):
    return item.suppressed_until is not None and now < item.suppressed_until
