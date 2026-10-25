# 📘 README.md — Лабораторная работа № 4

> **Тема:** Объектно-ориентированное программирование. Принципы SOLID  
> **Прикладная задача:** Доменная модель интернет-магазина  
> **Среда:** Google Colab + GitLab / GitHub

---

## 🎯 Цель работы

Спроектировать объектную модель для управления **товарами**, **клиентами**, **заказами** и **скидками**, применив:

- инкапсуляцию и свойства (`@property`)
- наследование и `super()`
- полиморфизм и абстрактные классы (`ABC`)
- магические методы (`__str__`, `__repr__`, `__eq__`, `__add__`, `__len__`)
- принципы **SOLID** (SRP, OCP, LSP, ISP, DIP)
- внедрение зависимостей (Dependency Injection)

---

## 🏗️ Архитектура классов

```
                    ┌─────────────┐
                    │   Product   │  ← инкапсуляция price/stock/name
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  OrderItem  │  ← __eq__, __add__, subtotal
                    └──────┬──────┘
                           │
   ┌─────────────┐  ┌──────▼──────┐  ┌──────────────┐
   │  Customer   │◄─┤    Order    │─►│   Discount   │ (ABC)
   └──────┬──────┘  └──────┬──────┘  └──────┬───────┘
          │                │                 │
   ┌──────▼──────┐         │        ┌────────┼─────────┐
   │ VipCustomer │         │        │        │         │
   └─────────────┘         │  Percentage  Fixed   NoDiscount
                           │   Discount   Discount
                    ┌──────▼───────┐
                    │ OrderService │  ← DIP: зависит от абстракции
                    └──────┬───────┘
                           │
                    ┌──────▼──────────┐
                    │ OrderRepository │ (ABC)
                    └──────┬──────────┘
                           │
                    ┌──────▼──────────────────┐
                    │ InMemoryOrderRepository │  ← uuid для ID
                    └─────────────────────────┘
```

### 📋 Краткое описание классов

| Класс | Ответственность |
|---|---|
| `Product` | Товар с валидируемыми `name`, `price`, `stock` |
| `Customer` | Клиент с балансом, `deposit/withdraw`, `get_discount() → 0%` |
| `VipCustomer` | VIP-клиент: бонус при создании, `get_discount() → 10%` |
| `OrderItem` | Позиция заказа: товар + количество, `subtotal` |
| `Order` | Композиция: клиент + позиции + скидка, `total()`, `__len__` |
| `Discount` (ABC) | Абстрактная скидка, метод `apply(total)` |
| `PercentageDiscount` | Процентная скидка (0–100 %) |
| `FixedDiscount` | Фиксированная скидка (не уходит в минус) |
| `NoDiscount` | Null Object — удобная замена `None` |
| `OrderRepository` (ABC) | Интерфейс хранилища: `save`, `get_by_id`, `get_all` |
| `InMemoryOrderRepository` | Хранилище в словаре, ID через `uuid4` |
| `OrderService` | Оркестратор: валидация + делегирование в репозиторий |

---

## 🧩 Применение принципов SOLID

### 1️⃣ SRP — Single Responsibility Principle

> *У класса должна быть только одна причина для изменения.*

| Класс | Единственная ответственность |
|---|---|
| `Order` | Только состав заказа и расчёт суммы |
| `Discount` | Только применение скидки к сумме |
| `OrderRepository` | Только хранение заказов |
| `OrderService` | Только сценарий оформления заказа |

❌ `Order` **не** сохраняет себя в БД, **не** печатает счета, **не** шлёт email.

---

### 2️⃣ OCP — Open/Closed Principle

> *Классы открыты для расширения, но закрыты для модификации.*

**Пример на иерархии скидок.** Чтобы добавить новую скидку (например, `SeasonalDiscount`), достаточно создать нового наследника `Discount`:

```python
class SeasonalDiscount(Discount):
    def __init__(self, percent: float, season: str) -> None:
        self.percent = percent
        self.season = season

    def apply(self, total: float) -> float:
        return total * (1 - self.percent / 100)
```

**Код `Order.total()` не меняется** — он вызывает `discount.apply(base)` через абстракцию.

То же самое с хранилищем: чтобы добавить `SQLOrderRepository`, создаём нового наследника `OrderRepository`, не трогая `OrderService`.

---

### 3️⃣ LSP — Liskov Substitution Principle

> *Наследник должен без ошибок подставляться вместо родителя.*

✅ `VipCustomer` подставляется туда, где ожидается `Customer`:

```python
customer: Customer = VipCustomer("Мария", 1000.0, bonus=500.0)
order = Order(customer)   # Order использует только customer.name
```

✅ Любой наследник `Discount` подставляется в `Order.discount`:

```python
order.discount = PercentageDiscount(10)  # OK
order.discount = FixedDiscount(500)      # OK
order.discount = NoDiscount()            # OK
```

✅ Любой наследник `OrderRepository` подставляется в `OrderService`.

**Контракт не усиливается:** наследники не бросают новых исключений и не возвращают `None` там, где родитель возвращал значение.

---

### 4️⃣ ISP — Interface Segregation Principle

> *Лучше много специализированных интерфейсов, чем один огромный.*

Интерфейс `OrderRepository` содержит только то, что реально нужно сервису:

```python
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> str: ...
    @abstractmethod
    def get_by_id(self, order_id: str) -> Order | None: ...
    @abstractmethod
    def get_all(self) -> list[Order]: ...
```

Клиент, которому нужен только `save`, не обязан реализовывать `get_all`. При необходимости интерфейс можно разделить на `OrderWriter` и `OrderReader`.

---

### 5️⃣ DIP — Dependency Inversion Principle

> *Зависимость от абстракций, а не от конкретных реализаций.*

```python
class OrderService:
    def __init__(self, repository: OrderRepository) -> None:  # абстракция
        self.repository = repository
```

- `OrderService` (модуль высокого уровня) **не знает** про `InMemoryOrderRepository`.
- `InMemoryOrderRepository` (модуль низкого уровня) **не знает** про `OrderService`.
- Оба зависят от **абстракции** `OrderRepository`.

**Dependency Injection в действии:**

```python
repo = InMemoryOrderRepository()   # создаётся снаружи
service = OrderService(repo)        # внедряется через конструктор
order_id = service.place_order(order)
```

Чтобы перейти на SQL/Redis/файл — достаточно передать другой `OrderRepository`, код сервиса не меняется.

---

## 📂 Структура репозитория

```
python-labs-gutierrez/
└── lab4/
    ├── lab4_oop.ipynb     # ноутбук со всеми заданиями 1–20
    ├── README.md          # этот файл
    └── .gitignore         # исключения для Python/Jupyter
```

### `.gitignore`

```gitignore
__pycache__/
.ipynb_checkpoints/
*.pyc
```

---

## 🚀 Как запустить

1. Открыть `lab4_oop.ipynb` в **Google Colab** или локальном **Jupyter**.
2. Выполнить: **Kernel → Restart & Run All**.
3. Убедиться, что все ячейки выполняются **сверху вниз без ошибок**.

### Проверка PEP 8

```bash
pip install flake8
flake8 lab4_oop.ipynb
```

---

## ✅ Чек-лист сдачи (Задание 20)

- [x] Docstring ко всем классам и публичным методам
- [x] Код проверен линтером (PEP 8)
- [x] `README.md` описывает архитектуру
- [x] Обоснованы принципы **DIP** и **OCP**
- [x] Коммит и `git push` в репозиторий
- [x] Ноутбук выполняется сверху вниз без ошибок

---

## 🔗 Ссылка на репозиторий

**GitHub:** https://github.com/sedergsoft/python-labs-gutierrez/

---

## 👤 Автор

- **ФИО:** Гутьеррес Рейес Оньель Сергей
- **Группа:** M26-534
- **Дата:** 2026-10-25

---

<div align="center">

**ЛР4 — ООП и SOLID** · Python 3 · Google Colab · GitHub

</div>
