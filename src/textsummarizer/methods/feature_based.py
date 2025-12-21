# Не отсортированы импорты, нет докстрингов

from typing import List, Dict
import re
from .base import BaseSummarizer
from ..entities import Sentence
from ..utils.text_processing import (
    preprocess_text,
    tokenize_words,
    calculate_readability_metrics,
)


class FeatureBasedSummarizer(BaseSummarizer):
    def __init__(self):
        self._position_weights = {"first": 1.0, "last": 0.8, "middle": 0.3}

        self._keywords = {  # Следовало вынести из py-файлов. Например, в txt.
            "важно",
            "следовательно",
            "итог",
            "вывод",
            "заключение",
            "основной",
            "главный",
            "результат",
            "цель",
            "задача",
            "проблема",
            "решение",
            "метод",
            "способ",
            "алгоритм",
            "анализ",
            "исследование",
            "эксперимент",
            "доказательство",
        }

    def _extract_features(
        self, sentence: str, idx: int, total_sentences: int
    ) -> Dict[str, float]:
        features = {}  # Лишняя строчка

        features["position_score"] = self._calculate_position_score(
            idx, total_sentences
        )

        words = sentence.split()
        features["length_score"] = self._calculate_length_score(len(words))

        features["has_numbers"] = 1.0 if re.search(r"\d", sentence) else 0.0

        uppercase_words = [w for w in words if w and w[0].isupper()]
        features["proper_noun_ratio"] = (
            len(uppercase_words) / len(words) if words else 0.0
        )

        processed_sentence = preprocess_text(
            sentence, lowercase=True, remove_punctuation=True, remove_numbers=False
        )
        processed_words = tokenize_words(processed_sentence)
        features["lexical_diversity"] = (
            len(set(processed_words)) / len(processed_words) if processed_words else 0.0
        )

        sentence_lower = sentence.lower()
        found_keywords = sum(1 for kw in self._keywords if kw in sentence_lower)
        features["keyword_score"] = min(found_keywords / 3, 1.0)  # Нормализуем

        readability_metrics = calculate_readability_metrics(sentence)
        flesch_score = readability_metrics.get("flesch_score", 0)
        # Expected type 'int' (matched generic type
        # 'SupportsRichComparisonT ≤: Union[SupportsDunderLT, SupportsDunderGT]'), got 'float' instead
        # Вообще не должно работать
        features["readability_score"] = max(0, min(flesch_score / 100, 1.0))

        return features

    def _calculate_position_score(self, idx: int, total: int) -> float:
        if idx == 0:
            return self._position_weights["first"]
        elif idx == total - 1:
            return self._position_weights["last"]
        else:
            distance_to_edge = min(idx, total - 1 - idx)
            edge_score = 1.0 - (distance_to_edge / (total / 2))
            return self._position_weights["middle"] * edge_score

    def _calculate_length_score(self, word_count: int) -> float:  # Method '_calculate_length_score' may be 'static'
        if 15 <= word_count <= 25:
            return 1.0
        elif 10 <= word_count < 15 or 25 < word_count <= 30:
            return 0.7
        elif 5 <= word_count < 10 or 30 < word_count <= 40:
            return 0.4
        else:
            return 0.1

    def _calculate_importance_score(self, features: Dict[str, float]) -> float:
        # Method '_calculate_length_score' may be 'static'
        weights = {
            "position_score": 0.25,
            "length_score": 0.15,
            "has_numbers": 0.1,
            "proper_noun_ratio": 0.1,
            "lexical_diversity": 0.15,
            "keyword_score": 0.15,
            "readability_score": 0.1,
        }

        total_score = 0.0
        for feature_name, weight in weights.items():
            feature_value = features.get(feature_name, 0.0)
            total_score += feature_value * weight

        return total_score

    def summarize(
        self, sentences: List[str], compression_ratio: float
    ) -> List[Sentence]:
        if not sentences:
            return []

        scored_sentences = []
        for idx, sentence in enumerate(sentences):
            features = self._extract_features(sentence, idx, len(sentences))
            importance_score = self._calculate_importance_score(features)

            scored_sentences.append(
                {
                    "text": sentence,
                    "idx": idx,
                    "features": features,
                    "score": importance_score,
                }
            )

        num_to_select = max(1, int(len(sentences) * compression_ratio))

        scored_sentences.sort(key=lambda x: x["score"], reverse=True)

        selected = []
        for item in scored_sentences[:num_to_select]:
            sentence_obj = Sentence(
                text=item["text"],
                position=item["idx"],
                importance_score=item["score"],
                is_important=True,
                features=item["features"],
            )
            selected.append(sentence_obj)

        selected.sort(key=lambda x: x.position)

        return selected
