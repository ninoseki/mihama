import httpx


def is_responsive(url: str) -> bool:
    try:
        httpx.get(url)
        return True
    except Exception:
        return False
