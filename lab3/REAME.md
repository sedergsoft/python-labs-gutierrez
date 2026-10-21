# Лабораторная работа №3. Обработка исключений, модуль OS, виртуальные окружения

## Цель работы
Освоить механизм обработки исключений в Python (`try/except/else/finally`,
иерархия исключений, собственные исключения, LBYL и EAFP), работу с файлами
и JSON (`with open`, режимы, `encoding`, `json.dump/load`), модули `os`,
`os.path`, `pathlib`, создание собственных модулей и пакетов, виртуальные
окружения (`venv`, `requirements.txt`, `.env`, `.gitignore`) и логирование
с уровнями и ротацией на примере конвейера пакетного импорта JSON-документов.

## Структура ноутбука

Ноутбук `lab3_exceptions_files.ipynb` содержит две части:

- **Часть I. Теория** — исключения и их иерархия, собственные исключения,
  LBYL и EAFP, работа с файлами и JSON, `os` / `os.path` / `pathlib`,
  модули и пакеты, виртуальные окружения, логирование.
- **Часть II. Задания (1–20)** — базовые упражнения по исключениям и файлам
  и единый pipeline «Пакетный импорт JSON-документов» с изоляцией ошибок,
  логированием и сводным отчётом.

---

## Часть I. Теория

Кратко рассмотрены:

- синтаксис `try/except/else/finally` и порядок выполнения;
- иерархия исключений от `BaseException` (`ArithmeticError`, `LookupError`,
  `OSError`, `ValueError`, `TypeError`, `AttributeError`);
- создание собственных исключений (`IngestError`, `ConfigError`,
  `DocumentError`);
- LBYL vs EAFP и почему в Python идиоматичен EAFP;
- лучшие практики: ловить конкретные типы, не проглатывать молча,
  сохранять traceback через `raise ... from exc`;
- файловые режимы (`r`, `w`, `a`, `x`, `b`), `encoding="utf-8"`,
  `with open(...)`;
- JSON: `json.dump/load`, `json.dumps/loads`, `ensure_ascii=False`,
  `json.JSONDecodeError`;
- `os`, `os.path`, `pathlib` (`rglob`, `read_text`, `write_text`, `stat`);
- модули и пакеты, `if __name__ == "__main__"`, `__init__.py`;
- виртуальные окружения, `pip`, `requirements.txt`, `.env`, `.gitignore`;
- логирование: уровни, `Logger` / `Handler` / `Formatter`,
  `RotatingFileHandler`, ленивое форматирование.

---

## Часть II. Базовые упражнения (задания 1–10)

| № | Задание | Реализовано |
|---|---|---|
| 1 | Функция vs процедура | `log_error`, `parse_int_safe` |
| 2 | Все виды исключений + `__mro__` | `expressions` + цикл `try/except` |
| 3 | `try/except/else/finally` | `safe_divide` |
| 4 | Своя иерархия исключений | `IngestError`, `ConfigError`, `DocumentError` |
| 5 | LBYL vs EAFP | два способа чтения файла |
| 6 | Файловые режимы | запись `w`, дозапись `a`, чтение `r` |
| 7 | JSON: сериализация/десериализация | `json.dump/load`, ловля `JSONDecodeError` |
| 8 | Работа с `pathlib` | `Path(...).rglob("*.json")`, `stat().st_size` |
| 9 | Свой модуль | `jsonutils.py` (`read_json`, `write_json`) |
| 10 | Логирование с уровнями | консоль INFO + файл DEBUG с ротацией |

### Ключевые результаты заданий 1–10

- **Задание 2.** Предсказаны и подтверждены типы исключений:
  `ZeroDivisionError` (родитель `ArithmeticError`), `ValueError`,
  `IndexError` и `KeyError` (родитель `LookupError`), `TypeError`,
  `FileNotFoundError` (родитель `OSError`). Для каждого выведен `__mro__`.
- **Задание 3.** `safe_divide(10, 2) → 5.0`, `safe_divide(10, 0) → None`,
  `safe_divide(10, "x") → None`; `else` срабатывает только при успехе,
  `finally` — всегда.
- **Задание 4.** `except IngestError` ловит и `ConfigError`, и
  `DocumentError` — полиморфизм исключений.
- **Задание 5.** LBYL (`os.path.exists` + `open`) и EAFP
  (`try/except FileNotFoundError`) дают одинаковый результат,
  но EAFP устойчив к race conditions.
- **Задание 6.** Повторное открытие в `'w'` усекает файл; `'a'`
  дописывает в конец.
- **Задание 7.** `ensure_ascii=False` сохраняет кириллицу как есть;
  битый JSON ловится как `JSONDecodeError`.
- **Задание 8.** `rglob("*.json")` рекурсивно обходит дерево;
  `stat().st_size` даёт размер в байтах.
- **Задание 9.** `jsonutils.py` с блоком `if __name__ == "__main__"`
  импортируется без побочных эффектов.
- **Задание 10.** Консоль видит INFO и выше, файл — всё (DEBUG и выше);
  `RotatingFileHandler` ротирует лог по размеру.

---

## Часть II. Прикладная задача «Пакетный импорт JSON-документов» (задания 11–20)

### Инициализация данных (перед заданием 11)

Каталог `inbox/` создаётся заново при каждом запуске ноутбука:
6 JSON-файлов — 3 валидных (`good/a.json`, `good/b.json`,
`nested/c.json`) и 3 проблемных (`broken.json` — битый JSON,
`no_keys.json` — нет обязательных полей, `not_object.json` —
не объект, а список). Обязательные поля: `id`, `name`.

### Реализованные классы и функции

| № | Задание | Классы / функции |
|---|---|---|
| 11 | Настройки из окружения | `Settings`, `Settings.from_env`, `ConfigError` |
| 12 | Обход каталога | `Ingester.iter_files` |
| 13 | Чтение одного документа | `IngesterWithLoad.load_document` |
| 14 | Конвейер с изоляцией ошибок | `IngesterRun.run` |
| 15 | Сохранение отчёта | `IngesterFull._save` |
| 16 | Настройка логирования | `setup_logging` |
| 17 | CLI с кодами выхода | `main` |
| 18 | Проверка сценариев | запуск конвейера на подготовленных данных |
| 19 | Секреты и `.gitignore` | `.env`, `.gitignore`, `load_dotenv` |
| 20 | Единый pipeline | `generate_report`, `pipeline_main` |

### Ключевые результаты заданий 11–20

- **Задание 11.** `Settings.from_env()` читает `SOURCE_DIR`,
  `OUTPUT_PATH`, `REQUIRED_KEYS`; при отсутствии каталога или пустых
  ключах бросает `ConfigError`.
- **Задание 12.** `iter_files()` возвращает отсортированный итератор
  по 6 файлам: `broken.json`, `good/a.json`, `good/b.json`,
  `nested/c.json`, `no_keys.json`, `not_object.json`.
- **Задание 13.** `load_document` валидирует:
  - `OSError` → `DocumentError("не читается ...")` через `raise ... from exc`;
  - `JSONDecodeError` → `DocumentError("битый JSON ...")`;
  - не объект → `DocumentError("ожидался объект, получено list")`;
  - нет полей → `DocumentError("нет полей: id, name")`.
  Результат: 3 OK, 3 FAIL.
- **Задание 14.** `run()` изолирует ошибки: `total_files=6`,
  `imported=3`, `skipped=3`, в `errors` — три причины.
- **Задание 15.** `_save` создаёт родительский каталог
  (`parents=True, exist_ok=True`) и пишет `catalog.json`
  с `ensure_ascii=False`; ошибки записи оборачиваются в `ConfigError`.
- **Задание 16.** `setup_logging()` настраивает корневой логгер:
  консоль INFO, файл `ingest.log` DEBUG с ротацией
  (`maxBytes=100_000`, `backupCount=3`).
- **Задание 17.** `main()` возвращает:
  `0` — успех, `1` — ошибка конвейера, `2` — ошибка конфигурации.
- **Задание 18.** Сквозной сценарий: 3 валидных файла импортированы,
  3 проблемных пропущены с причинами, код выхода `0`.
- **Задание 19.** `.env` загружается через `python-dotenv`;
  `.env`, `venv/`, `__pycache__/`, `*.log`, `inbox/`, `catalog.json`
  добавлены в `.gitignore`.
- **Задание 20.** `generate_report` + `pipeline_main` создают
  `catalog.json` и `ingest.log`. Сводка: **6 файлов, 3 импортировано,
  3 пропущено**, код выхода `0`.

### Сводка выполнения (задание 20)
