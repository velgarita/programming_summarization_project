# Не отсортированы импорты, нет докстрингов

from typing import List
from .entities import SummaryMethod, SummaryResult
from .methods import FrequencyBasedSummarizer, FeatureBasedSummarizer
from .statistics import StatisticsCalculator
from .utils.text_processing import split_into_sentences
from .utils.file_io import save_json
from pathlib import Path


class TextSummarizer:
    def __init__(self, method: SummaryMethod = SummaryMethod.FEATURE_BASED):
        self.method = method

        if method == SummaryMethod.FREQUENCY_BASED:
            self.summarizer = FrequencyBasedSummarizer()
        else:  # FEATURE_BASED
            self.summarizer = FeatureBasedSummarizer()

        self.stats_calculator = StatisticsCalculator()

    def summarize(self, text: str, compression_ratio: float = 0.3) -> SummaryResult:
        if not 0 < compression_ratio <= 1:
            raise ValueError("compression_ratio должен быть в диапазоне (0, 1]")

        sentences = split_into_sentences(text)

        if not sentences:
            return SummaryResult(
                original_text=text,
                summary_text="",
                important_sentences=[],
                statistics=self.stats_calculator.calculate_stats(text, ""),
                method_used=self.method,
            )

        important_sentences = self.summarizer.summarize(sentences, compression_ratio)

        summary_text = " ".join(sent.text for sent in important_sentences)

        statistics = self.stats_calculator.calculate_stats(text, summary_text)

        return SummaryResult(
            original_text=text,
            summary_text=summary_text,
            important_sentences=important_sentences,
            statistics=statistics,
            method_used=self.method,
        )

    def save_result(self, result: SummaryResult, output_dir: str) -> None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        summary_file = output_path / "summary.txt"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(result.summary_text)

        stats_dict = {
            "original_sentences_count": result.statistics.original_sentences_count,
            "original_words_count": result.statistics.original_words_count,
            "summary_sentences_count": result.statistics.summary_sentences_count,
            "summary_words_count": result.statistics.summary_words_count,
            "compression_ratio": result.statistics.compression_ratio,
            "reading_time_minutes": result.statistics.reading_time_minutes,
            "original_readability": {
                "flesch_score": result.statistics.original_readability.flesch_score,
                "avg_sentence_length": result.statistics.original_readability.avg_sentence_length,
                "avg_word_length": result.statistics.original_readability.avg_word_length,
                "lexical_diversity": result.statistics.original_readability.lexical_diversity,
                "total_sentences": result.statistics.original_readability.total_sentences,
                "total_words": result.statistics.original_readability.total_words,
                "unique_words": result.statistics.original_readability.unique_words,
            },
            "summary_readability": {
                "flesch_score": result.statistics.summary_readability.flesch_score,
                "avg_sentence_length": result.statistics.summary_readability.avg_sentence_length,
                "avg_word_length": result.statistics.summary_readability.avg_word_length,
                "lexical_diversity": result.statistics.summary_readability.lexical_diversity,
                "total_sentences": result.statistics.summary_readability.total_sentences,
                "total_words": result.statistics.summary_readability.total_words,
                "unique_words": result.statistics.summary_readability.unique_words,
            },
            "method_used": result.method_used.value,
        }

        stats_file = output_path / "statistics.json"
        from .utils.file_io import save_json

        save_json(stats_file, stats_dict)

        sentences_info = []
        for sent in result.important_sentences:
            sentences_info.append(
                {
                    "text": sent.text,
                    "position": sent.position,
                    "importance_score": sent.importance_score,
                    "features": sent.features,
                }
            )

        sentences_file = output_path / "sentences_info.json"
        save_json(sentences_file, sentences_info)
