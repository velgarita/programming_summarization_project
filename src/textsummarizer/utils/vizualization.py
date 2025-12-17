import matplotlib.pyplot as plt
import matplotlib
from typing import List, Dict, Any
import numpy as np
from pathlib import Path
import logging

matplotlib.use("Agg")

logger = logging.getLogger(__name__)


def plot_sentence_scores(
    sentences: List[str], scores: List[float], save_path: str = None, top_n: int = 10
) -> None:
    if not sentences or not scores or len(sentences) != len(scores):
        logger.warning("Некорректные данные для построения графика")
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    positions = range(len(scores))
    ax1.bar(positions, scores, alpha=0.7)
    ax1.set_xlabel("Номер предложения")
    ax1.set_ylabel("Оценка важности")
    ax1.set_title("Оценки важности предложений")
    ax1.grid(True, alpha=0.3)

    if top_n > 0 and top_n < len(scores):
        top_indices = np.argsort(scores)[-top_n:]
        for idx in top_indices:
            ax1.bar(idx, scores[idx], color="red", alpha=0.8)

    ax2.hist(scores, bins=20, edgecolor="black", alpha=0.7)
    ax2.set_xlabel("Оценка важности")
    ax2.set_ylabel("Частота")
    ax2.set_title("Распределение оценок важности")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        logger.info(f"График сохранен: {save_path}")
    else:
        plt.show()

    plt.close()


def plot_summary_comparison(
    original_stats: Dict[str, Any], summary_stats: Dict[str, Any], save_path: str = None
) -> None:
    if not original_stats or not summary_stats:
        logger.warning("Нет данных для сравнения")
        return

    labels = ["Предложения", "Слова", "Уникальные слова"]

    original_values = [
        original_stats.get("total_sentences", 0),
        original_stats.get("total_words", 0),
        original_stats.get("unique_words", 0),
    ]

    summary_values = [
        summary_stats.get("total_sentences", 0),
        summary_stats.get("total_words", 0),
        summary_stats.get("unique_words", 0),
    ]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(x - width / 2, original_values, width, label="Оригинал", alpha=0.8)
    bars2 = ax.bar(x + width / 2, summary_values, width, label="Саммари", alpha=0.8)

    ax.set_xlabel("Метрики")
    ax.set_ylabel("Количество")
    ax.set_title("Сравнение оригинального текста и саммари")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{int(height)}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

    autolabel(bars1)
    autolabel(bars2)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        logger.info(f"График сравнения сохранен: {save_path}")
    else:
        plt.show()

    plt.close()


def plot_word_frequencies(
    word_freq: Dict[str, float], top_n: int = 20, save_path: str = None
) -> None:
    if not word_freq:
        logger.warning("Нет данных о частоте слов")
        return

    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    top_words = sorted_words[:top_n]
    words, frequencies = zip(*top_words) if top_words else ([], [])

    fig, ax = plt.subplots(figsize=(12, 8))

    y_pos = np.arange(len(words))
    ax.barh(y_pos, frequencies, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(words)
    ax.invert_yaxis()
    ax.set_xlabel("Частота")
    ax.set_title(f"Топ-{top_n} самых частых слов")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        logger.info(f"График частотности слов сохранен: {save_path}")
    else:
        plt.show()

    plt.close()


def plot_readability_metrics(metrics: Dict[str, float], save_path: str = None) -> None:
    if not metrics:
        logger.warning("Нет данных о метриках читабельности")
        return

    labels = list(metrics.keys())
    values = list(metrics.values())

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection="polar"))

    ax.plot(angles, values, "o-", linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Метрики читабельности текста")
    ax.grid(True)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        logger.info(f"Радар-диаграмма сохранена: {save_path}")
    else:
        plt.show()

    plt.close()
