from __future__ import annotations

DATA: dict[str, list[dict]] = {}  # {"YYYY-MM-DD": [{"text": str, "done": bool}, ...]}

def key(y: int, m: int, d: int) -> str:
    return f"{y:04d}-{m:02d}-{d:02d}"

def tasks_for(y: int, m: int, d: int) -> list[dict]:
    return DATA.setdefault(key(y, m, d), [])

