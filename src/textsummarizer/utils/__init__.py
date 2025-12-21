from .file_io import read_text_file, write_text_file, save_json, load_json, save_csv
from .text_processing import (
    split_into_sentences,
    preprocess_text,
    tokenize_words,
    calculate_word_frequencies,
    calculate_readability_metrics,
    extract_named_entities,
)
from .vizualization import (
    plot_sentence_scores,
    plot_summary_comparison,
    plot_word_frequencies,
    plot_readability_metrics,
)

__all__ = [
    "read_text_file",
    "write_text_file",
    "save_json",
    "load_json",  # Используется только в тестах. Тоже не должно быть доступно юзеру (инкапсуляция)
    "save_csv",  # Не используется "снаружи" -> не должно быть доступно юзеру (инкапсуляция)
    "split_into_sentences",
    "preprocess_text",
    "tokenize_words",
    "calculate_word_frequencies",  # Не используется "снаружи" -> не должно быть доступно юзеру (инкапсуляция)
    "calculate_readability_metrics",
    "extract_named_entities",  # Не используется "снаружи" -> не должно быть доступно юзеру (инкапсуляция)
    "plot_sentence_scores",
    "plot_summary_comparison",
    "plot_word_frequencies",  # Не используется "снаружи" -> не должно быть доступно юзеру (инкапсуляция)
    "plot_readability_metrics",
]
