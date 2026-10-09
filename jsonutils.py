import json
from pathlib import Path

class DocumentError(Exception):
    """Ошибка чтения JSON."""

def read_json(path: str | Path) -> dict:
    """Читает JSON-словарь или поднимает DocumentError."""
    try:
        with Path(path).open(encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise DocumentError(f"{path}: {exc}") from exc
    if not isinstance(data, dict):
        raise DocumentError(f"{path}: JSON должен быть объектом")
    return data

def write_json(data: dict, path: str | Path) -> None:
    """Записывает словарь в JSON, сохраняя кириллицу."""
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    write_json({"id": 1, "name": "Пример"}, "jsonutils_demo.json")
    print(read_json("jsonutils_demo.json"))
