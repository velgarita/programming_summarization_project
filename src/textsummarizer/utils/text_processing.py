# Не отсортированы импорты, нет докстрингов

import re
import string
from typing import List, Dict, Tuple
import math
from collections import Counter
import logging

logger = logging.getLogger(__name__)


def split_into_sentences(text: str) -> List[str]:
    if not text or not isinstance(text, str):
        return []

    text = text.replace("\n", " ").strip()

    sentence_endings = re.compile(r"[.!?]+")
    sentences = sentence_endings.split(text)

    sentences = [s.strip() for s in sentences if s.strip()]

    logger.debug(f"Текст разделен на {len(sentences)} предложений")
    return sentences


def preprocess_text(
    text: str,
    lowercase: bool = True,
    remove_punctuation: bool = True,
    remove_numbers: bool = False,
) -> str:
    if not text:
        return ""

    processed = text
    if lowercase:
        processed = processed.lower()

    if remove_punctuation:
        processed = processed.translate(
            str.maketrans("", "", string.punctuation + '«»—"')
        )

    if remove_numbers:
        processed = re.sub(r"\d+", "", processed)

    processed = re.sub(r"\s+", " ", processed).strip()

    return processed


def tokenize_words(text: str) -> List[str]:
    if not text:
        return []

    words = text.split()
    words = [word for word in words if word]

    return words


def calculate_word_frequencies(words: List[str]) -> Dict[str, float]:
    if not words:
        return {}

    total_words = len(words)
    word_counts = Counter(words)

    frequencies = {word: count / total_words for word, count in word_counts.items()}

    return frequencies


def calculate_readability_metrics(text: str) -> Dict[str, float]:
    sentences = split_into_sentences(text)
    words = tokenize_words(preprocess_text(text, remove_punctuation=True))

    if not sentences or not words:
        return {}

    total_sentences = len(sentences)
    total_words = len(words)

    def count_syllables(word: str) -> int:
        vowels = "аеёиоуыэюяaeiouy"  # Следовало вынести из py-файлов. Например, в txt.
        return sum(1 for char in word.lower() if char in vowels)

    total_syllables = sum(count_syllables(word) for word in words)

    flesch_score = (
        206.835
        - 1.3 * (total_words / total_sentences)
        - 60.1 * (total_syllables / total_words)
    )

    avg_sentence_length = total_words / total_sentences

    avg_word_length = sum(len(word) for word in words) / total_words

    unique_words = len(set(words))
    lexical_diversity = unique_words / total_words if total_words > 0 else 0

    metrics = {
        "flesch_score": round(flesch_score, 2),
        "avg_sentence_length": round(avg_sentence_length, 2),
        "avg_word_length": round(avg_word_length, 2),
        "lexical_diversity": round(lexical_diversity, 3),
        "total_sentences": total_sentences,
        "total_words": total_words,
        "unique_words": unique_words,
    }

    logger.debug(f"Рассчитаны метрики читабельности: {metrics}")
    return metrics


def extract_named_entities(text: str) -> List[str]:
    words = tokenize_words(text)

    named_entities = []
    for word in words:
        if word and word[0].isupper() and len(word) > 1:
            named_entities.append(word)

    return list(set(named_entities))
