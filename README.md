# 📚 python-labs-gutierrez

> **Repositorio de prácticas** de la asignatura de Python  
> **Autor:** Гутьеррес Рейес Оньель Сергей  
> **Grupo:** M26-534  
> **Institución:** МИФИ  
> **Repositorio:** https://github.com/sedergsoft/python-labs-gutierrez

---

## 🎯 Descripción general

Este repositorio contiene las **prácticas de laboratorio** realizadas a lo largo del curso. Cada práctica está en su propia carpeta (o archivo, en el caso de las primeras), con su notebook de Jupyter, sus archivos auxiliares y, cuando corresponde, su `README.md` específico.

El objetivo es documentar el progreso del curso y servir como portafolio de los ejercicios realizados.

---

## 📂 Estructura del repositorio


<div align="center">

**ЛР4 — ООП и SOLID** · Python 3 · Google Colab · GitHub

</div>
python-labs-gutierrez/
│
├── lab1.ipynb # ЛР1 — notebook inicial
├── lab1new.ipynb # ЛР1 — versión revisada
│
├── lab2/ # ЛР2 — carpeta de la práctica 2
│
├── lab3/ # ЛР3 — carpeta de la práctica 3
├── lab3.ipynb # ЛР3 — notebook
│
├── lab-04.ipynb # ЛР4 — notebook de la práctica 4
├── ЛР4_Python_04_ООП_Принципы_SOLID_в1_сергей.ipynb # ЛР4 — versión original
│
├── pathlib_demo/data/raw/ # Demostración de pathlib
│
├── catalog.json # Datos de ejemplo (ЛР3)
├── jsonutils.py # Utilidades JSON (ЛР3)
├── jsonutils_demo.json # Datos de ejemplo (ЛР3)
├── lbyl_eafp_demo.txt # Demostración LBYL vs EAFP (ЛР3)
│
├── Python__04_ЛР_2.pdf # Enunciado de la ЛР2
├── Python__04_ЛР_3.pdf # Enunciado de la ЛР3
│
├── .gitignore # Exclusiones de Git
└── README.md # Este archivo


---

## 🧪 Prácticas incluidas

### ЛР1 — Introducción a Python

- **Archivos:** `lab1.ipynb`, `lab1new.ipynb`
- **Contenido:** primeros pasos con Python, tipos de datos, estructuras de control y funciones básicas.
- `lab1new.ipynb` es una versión revisada y ampliada de la primera entrega.

---

### ЛР2 — Trabajo con archivos y estructuras de datos

- **Carpeta:** `lab2/`
- **Enunciado:** `Python__04_ЛР_2.pdf`
- **Contenido:** lectura y escritura de archivos, procesamiento de datos, estructuras de datos avanzadas (listas, diccionarios, conjuntos) y organización del código en módulos.

---

### ЛР3 — JSON, `pathlib` y manejo de errores

- **Carpeta:** `lab3/`, notebook `lab3.ipynb`
- **Enunciado:** `Python__04_ЛР_3.pdf`
- **Archivos auxiliares:**
  - `catalog.json` — datos de ejemplo en formato JSON.
  - `jsonutils.py` — utilidades para leer/escribir JSON.
  - `jsonutils_demo.json` — datos generados por la demo.
  - `lbyl_eafp_demo.txt` — comparación de los estilos LBYL (*Look Before You Leap*) y EAFP (*Easier to Ask Forgiveness than Permission*).
  - `pathlib_demo/data/raw/` — demostración del uso de `pathlib` para manejar rutas.
- **Contenido:** serialización JSON, manejo de rutas con `pathlib`, tratamiento de excepciones y estilos de programación defensiva.

---

### ЛР4 — Programación orientada a objetos y principios SOLID

- **Archivos:** `lab-04.ipynb`, `ЛР4_Python_04_ООП_Принципы_SOLID_в1_сергей.ipynb`
- **Tema:** ООП y principios SOLID aplicados a una **модель домена интернет-магазина**.
- **Contenido:**
  - Clases y objetos (`Product`, `Customer`, `OrderItem`, `Order`).
  - Encapsulación con `@property` y validación.
  - Herencia y `super()` (`VipCustomer`).
  - Polimorfismo y clases abstractas (`Discount`, `PercentageDiscount`, `FixedDiscount`, `NoDiscount`).
  - Métodos mágicos (`__str__`, `__repr__`, `__eq__`, `__add__`, `__len__`).
  - Principios **SOLID** (SRP, OCP, LSP, ISP, DIP).
  - Inyección de dependencias (`OrderService` + `OrderRepository`).
  - Almacenamiento en memoria con `uuid` (`InMemoryOrderRepository`).
- **README específico de la ЛР4:** descripción detallada de la arquitectura de clases y de la aplicación de SOLID.

---

## 🛠️ Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| **Python 3** | Lenguaje principal |
| **Jupyter / Google Colab** | Entorno de desarrollo de los notebooks |
| **Git / GitHub** | Control de versiones y publicación |
| **`pathlib`, `json`, `uuid`, `abc`** | Bibliotecas estándar usadas en las prácticas |

---

## 🚀 Cómo usar este repositorio

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/sedergsoft/python-labs-gutierrez.git
   cd python-labs-gutierrez
