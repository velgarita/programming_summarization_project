import pytest
from src.textsummarizer.statistics import StatisticsCalculator
from src.textsummarizer.entities import ReadabilityMetrics


class TestStatisticsCalculator:
    def test_calculate_stats_empty_texts(self):
        calculator = StatisticsCalculator()
        stats = calculator.calculate_stats("", "")

        assert stats.original_sentences_count == 0
        assert stats.original_words_count == 0
        assert stats.summary_sentences_count == 0
        assert stats.summary_words_count == 0
        assert stats.compression_ratio == 0.0
        assert stats.reading_time_minutes == 0.0

        assert isinstance(stats.original_readability, ReadabilityMetrics)
        assert isinstance(stats.summary_readability, ReadabilityMetrics)

    def test_calculate_stats_short_texts(self, sample_text_short):
        calculator = StatisticsCalculator()

        original = sample_text_short
        summary = "Это первое предложение. Это второе предложение."

        stats = calculator.calculate_stats(original, summary)

        assert stats.original_sentences_count == 3
        assert stats.summary_sentences_count == 2
        assert stats.compression_ratio > 0

        assert stats.reading_time_minutes >= 0

        assert stats.original_readability.total_sentences == 3
        assert stats.original_readability.total_words > 0
        assert stats.summary_readability.total_sentences == 2
        assert stats.summary_readability.total_words > 0

    def test_calculate_stats_identical_texts(self, sample_text_short):
        calculator = StatisticsCalculator()
        stats = calculator.calculate_stats(sample_text_short, sample_text_short)

        assert stats.compression_ratio == 0.0

        assert stats.original_sentences_count == stats.summary_sentences_count
        assert stats.original_words_count == stats.summary_words_count

    def test_calculate_stats_compression_ratio(self):
        calculator = StatisticsCalculator()

        original = "Одно два три четыре пять шесть семь восемь девять десять"
        summary = "Одно два три"

        stats = calculator.calculate_stats(original, summary)

        expected_ratio = 1 - (3 / 10)
        assert abs(stats.compression_ratio - expected_ratio) < 0.01

    def test_calculate_stats_readability_metrics(self, sample_text_long):
        calculator = StatisticsCalculator()
        stats = calculator.calculate_stats(sample_text_long, sample_text_long[:100])

        assert stats.original_readability.flesch_score != 0
        assert stats.original_readability.avg_sentence_length > 0
        assert stats.original_readability.avg_word_length > 0
        assert 0 <= stats.original_readability.lexical_diversity <= 1
        assert stats.original_readability.total_sentences > 0
        assert stats.original_readability.total_words > 0
        assert stats.original_readability.unique_words > 0

        assert stats.summary_readability.flesch_score != 0
        assert stats.summary_readability.total_sentences > 0
        assert stats.summary_readability.total_words > 0

    def test_calculate_stats_with_numbers(self, sample_text_with_numbers):
        calculator = StatisticsCalculator()
        stats = calculator.calculate_stats(sample_text_with_numbers, "Текст с числами.")

        assert stats.original_sentences_count > 0
        assert stats.original_words_count > 0
        assert stats.original_readability.total_words > 0
