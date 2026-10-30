"""Ventas: carga, agregacion, graficos y reporte HTML."""
from __future__ import annotations

import logging
import sys
from abc import ABC, abstractmethod
from html import escape
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

logger = logging.getLogger("lab5")
logging.basicConfig(level=logging.INFO)
REQUIRED_COLUMNS = ("order_id", "order_datetime", "customer_id", "city",
                    "category", "brand", "unit_price", "quantity",
                    "channel", "status")
CITIES = {"Москва": (55.76, 37.62), "Санкт-Петербург": (59.94, 30.31),
          "Казань": (55.79, 49.12), "Нижний Новгород": (56.33, 44.00),
          "Екатеринбург": (56.84, 60.61), "Новосибирск": (55.03, 82.92),
          "Краснодар": (45.04, 38.98), "Владивосток": (43.12, 131.89)}


class DataValidationError(Exception):
    """Los datos no cumplen el esquema obligatorio."""


def load_orders(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, parse_dates=["order_datetime"])
    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        raise DataValidationError(f"Faltan columnas: {', '.join(missing)}")
    data["unit_price"] = pd.to_numeric(data["unit_price"], errors="coerce")
    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce")
    bad = (data["unit_price"].isna() | data["quantity"].isna()
           | (data["unit_price"] <= 0) | (data["quantity"] <= 0))
    logger.warning("Filas eliminadas: %d", int(bad.sum()))
    data = data.loc[~bad].copy()
    data["total"] = data["unit_price"] * data["quantity"]
    data["month"] = data["order_datetime"].dt.to_period("M")
    data["weekday"] = data["order_datetime"].dt.dayofweek
    data["hour"] = data["order_datetime"].dt.hour
    return data


def sold_orders(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["status"].isin(["completed", "shipped"])].copy()


def revenue_by_month(df: pd.DataFrame) -> pd.Series:
    return sold_orders(df).groupby("month")["total"].sum().sort_index()


def revenue_by(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        raise ValueError(f"Columna inexistente: {column}")
    return sold_orders(df).groupby(column)["total"].sum().sort_values(ascending=False)


def kpi(df: pd.DataFrame) -> dict:
    sold = sold_orders(df)
    return {"revenue": float(sold["total"].sum()),
            "paid_orders": int(len(sold)),
            "average_ticket": float(sold["total"].mean()),
            "cancelled_percent": float((df["status"] == "cancelled").mean() * 100)}


def plot_monthly_revenue(df: pd.DataFrame) -> plt.Figure:
    values = revenue_by_month(df)
    fig, ax = plt.subplots(figsize=(10, 4), layout="constrained")
    ax.plot(values.index.astype(str), values, marker="o")
    ax.set(title="Выручка по месяцам", xlabel="Месяц", ylabel="Выручка, руб.")
    ax.set_ylim(bottom=0)
    ax.axhline(values.mean(), ls="--", label="Средняя")
    peak = values.idxmax()
    ax.annotate("Максимум", (str(peak), values.max()))
    ax.legend()
    return fig


def plot_category_structure(df: pd.DataFrame) -> plt.Figure:
    table = sold_orders(df).pivot_table(index="month", columns="category",
                                         values="total", aggfunc="sum",
                                         fill_value=0)
    percent = table.div(table.sum(axis=1), axis=0).mul(100)
    fig, axes = plt.subplots(1, 2, figsize=(13, 4), layout="constrained")
    table.plot.bar(stacked=True, ax=axes[0], title="Выручка по категориям")
    percent.plot.bar(stacked=True, ax=axes[1], title="Доля категорий, %")
    return fig


def plot_order_distribution(df: pd.DataFrame) -> plt.Figure:
    sold = sold_orders(df)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), layout="constrained")
    axes[0].hist(sold["total"], bins="auto")
    axes[0].set_xscale("log")
    axes[0].axvline(sold["total"].mean(), color="red", label="Среднее")
    axes[0].axvline(sold["total"].median(), color="blue", label="Медиана")
    axes[0].legend()
    sns.boxplot(data=sold, x="channel", y="total", ax=axes[1])
    axes[1].set_yscale("log")
    return fig


def plot_activity_heatmap(df: pd.DataFrame) -> plt.Figure:
    table = pd.crosstab(df["weekday"], df["hour"]).reindex(range(7), fill_value=0)
    fig, ax = plt.subplots(figsize=(13, 4), layout="constrained")
    sns.heatmap(table, cmap="Blues", ax=ax,
                yticklabels=["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"])
    ax.set(title="Активность заказов", xlabel="Час", ylabel="День недели")
    return fig


def plot_sales_map(df: pd.DataFrame, cities: dict[str, tuple[float, float]]) -> go.Figure:
    summary = (sold_orders(df).groupby("city")
               .agg(revenue=("total", "sum"), orders=("order_id", "count"))
               .reset_index())
    summary["lat"] = summary["city"].map(lambda x: cities.get(x, (None, None))[0])
    summary["lon"] = summary["city"].map(lambda x: cities.get(x, (None, None))[1])
    summary = summary.dropna(subset=["lat", "lon"])
    fig = px.scatter_geo(summary, lat="lat", lon="lon", size="revenue",
                         hover_name="city", hover_data=["revenue", "orders"],
                         title="Продажи по городам")
    fig.update_geos(fitbounds="locations")
    Path("lab5_output").mkdir(exist_ok=True)
    fig.write_html("lab5_output/sales_map.html")
    return fig


class ChartBuilder(ABC):
    title: str
    filename: str

    @abstractmethod
    def build(self, df: pd.DataFrame) -> object: ...

    @abstractmethod
    def save(self, fig: object, path: Path) -> Path: ...


class MatplotlibChart(ChartBuilder):
    def save(self, fig: object, path: Path) -> Path:
        path = path.with_suffix(".png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return path


class PlotlyChart(ChartBuilder):
    def save(self, fig: object, path: Path) -> Path:
        path = path.with_suffix(".html")
        fig.write_html(path)
        return path


class MonthlyRevenueChart(MatplotlibChart):
    title, filename = "Выручка по месяцам", "monthly_revenue.png"
    def build(self, df): return plot_monthly_revenue(df)


class CategoryStructureChart(MatplotlibChart):
    title, filename = "Структура продаж", "category_structure.png"
    def build(self, df): return plot_category_structure(df)


class OrderDistributionChart(MatplotlibChart):
    title, filename = "Распределение заказов", "order_distribution.png"
    def build(self, df): return plot_order_distribution(df)


class ActivityHeatmapChart(MatplotlibChart):
    title, filename = "Активность", "activity_heatmap.png"
    def build(self, df): return plot_activity_heatmap(df)


class SalesMapChart(PlotlyChart):
    title, filename = "Карта продаж", "sales_map.html"
    def build(self, df): return plot_sales_map(df, CITIES)


def render_charts(builders: list[ChartBuilder], df: pd.DataFrame,
                  output_dir: Path) -> dict[str, list]:
    directory = output_dir / "figures"
    directory.mkdir(parents=True, exist_ok=True)
    result = {"saved": [], "failed": []}
    for builder in builders:
        try:
            result["saved"].append(builder.save(builder.build(df),
                                                directory / builder.filename))
        except Exception:
            logger.exception("Error en %s", builder.title)
            result["failed"].append(builder.title)
    return result


def build_html_report(kpi_values: dict, charts: list[tuple[str, Path]],
                      output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    body = "<h1>Informe de ventas</h1><ul>" + "".join(
        f"<li>{escape(str(k))}: {escape(str(v))}</li>"
        for k, v in kpi_values.items()) + "</ul>"
    body += "".join(f"<h2>{escape(title)}</h2><img src='{path.relative_to(output_path.parent).as_posix()}'>"
                    if path.suffix == ".png" else
                    f"<p><a href='{path.relative_to(output_path.parent).as_posix()}'>{escape(title)}</a></p>"
                    for title, path in charts)
    output_path.write_text(f"<!doctype html><meta charset='utf-8'>{body}", encoding="utf-8")
    return output_path


def main() -> int:
    try:
        data = load_orders("lab5_data/orders.csv")
    except (OSError, ValueError, DataValidationError):
        logger.exception("Datos inválidos")
        return 2
    builders = [MonthlyRevenueChart(), CategoryStructureChart(),
                OrderDistributionChart(), ActivityHeatmapChart(), SalesMapChart()]
    result = render_charts(builders, data, Path("lab5_output"))
    charts = [(b.title, Path("lab5_output/figures") / b.filename) for b in builders]
    build_html_report(kpi(data), charts, Path("lab5_output/report.html"))
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
