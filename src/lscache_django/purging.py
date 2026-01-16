def lscache_purge(tags=None, uris=None, stale=False):
    parts = []
    parts.append("stale=on" if stale else "stale=off")
    
    if tags:
        parts.extend([f"tag={tag}" for tag in tags])
    if uris:
        parts.extend(uris)
    
    return ",".join(parts)
