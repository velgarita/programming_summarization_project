from .entities import TextStats, ReadabilityMetrics
from .utils.text_processing import (
    split_into_sentences,
    preprocess_text,
    tokenize_words,
    calculate_readability_metrics,
)


class StatisticsCalculator:
    def calculate_stats(self, original: str, summary: str) -> TextStats:
        original_sentences = split_into_sentences(original)
        summary_sentences = split_into_sentences(summary)

        original_processed = preprocess_text(
            original, lowercase=True, remove_punctuation=True, remove_numbers=False
        )
        summary_processed = preprocess_text(
            summary, lowercase=True, remove_punctuation=True, remove_numbers=False
        )

        original_words = tokenize_words(original_processed)
        summary_words = tokenize_words(summary_processed)

        original_word_count = len(original_words)
        summary_word_count = len(summary_words)

        compression_ratio = (
            1 - (summary_word_count / original_word_count)
            if original_word_count > 0
            else 0.0
        )

        reading_time_minutes = original_word_count / 200

        original_readability_dict = calculate_readability_metrics(original)
        summary_readability_dict = calculate_readability_metrics(summary)

        original_readability = ReadabilityMetrics(
            flesch_score=original_readability_dict.get("flesch_score", 0),
            avg_sentence_length=original_readability_dict.get("avg_sentence_length", 0),
            avg_word_length=original_readability_dict.get("avg_word_length", 0),
            lexical_diversity=original_readability_dict.get("lexical_diversity", 0),
            total_sentences=original_readability_dict.get("total_sentences", 0),
            total_words=original_readability_dict.get("total_words", 0),
            unique_words=original_readability_dict.get("unique_words", 0),
        )

        summary_readability = ReadabilityMetrics(
            flesch_score=summary_readability_dict.get("flesch_score", 0),
            avg_sentence_length=summary_readability_dict.get("avg_sentence_length", 0),
            avg_word_length=summary_readability_dict.get("avg_word_length", 0),
            lexical_diversity=summary_readability_dict.get("lexical_diversity", 0),
            total_sentences=summary_readability_dict.get("total_sentences", 0),
            total_words=summary_readability_dict.get("total_words", 0),
            unique_words=summary_readability_dict.get("unique_words", 0),
        )

        return TextStats(
            original_sentences_count=len(original_sentences),
            original_words_count=original_word_count,
            summary_sentences_count=len(summary_sentences),
            summary_words_count=summary_word_count,
            compression_ratio=compression_ratio,
            reading_time_minutes=reading_time_minutes,
            original_readability=original_readability,
            summary_readability=summary_readability,
        )
