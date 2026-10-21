"""Утилиты для работы с JSON."""
import json
from pathlib import Path


def read_json(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(data: dict, path) -> None:
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    write_json({"hello": "мир"}, "demo_module.json")
    print(read_json("demo_module.json"))
