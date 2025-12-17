import pytest
from pathlib import Path
from src.textsummarizer.core import TextSummarizer
from src.textsummarizer.entities import SummaryMethod
from src.textsummarizer.utils.file_io import save_json, load_json


class TestIntegration:
    def test_full_pipeline_feature_based(self, sample_text_long):
        summarizer = TextSummarizer(method=SummaryMethod.FEATURE_BASED)
        result = summarizer.summarize(sample_text_long, compression_ratio=0.3)

        assert result.summary_text != ""
        assert len(result.important_sentences) > 0
        assert result.method_used == SummaryMethod.FEATURE_BASED

        stats = result.statistics
        assert stats.original_sentences_count > stats.summary_sentences_count
        assert stats.original_words_count > stats.summary_words_count
        assert stats.compression_ratio > 0

        assert stats.original_readability.total_sentences > 0
        assert stats.summary_readability.total_sentences > 0

    def test_full_pipeline_frequency_based(self, sample_text_long):
        summarizer = TextSummarizer(method=SummaryMethod.FREQUENCY_BASED)
        result = summarizer.summarize(sample_text_long, compression_ratio=0.3)

        assert result.summary_text != ""
        assert len(result.important_sentences) > 0
        assert result.method_used == SummaryMethod.FREQUENCY_BASED

        stats = result.statistics
        assert stats.original_sentences_count > stats.summary_sentences_count
        assert stats.original_words_count > stats.summary_words_count

    def test_pipeline_with_saving(self, sample_text_short, temp_dir):
        summarizer = TextSummarizer()
        result = summarizer.summarize(sample_text_short, compression_ratio=0.5)

        output_dir = temp_dir / "test_output"
        summarizer.save_result(result, str(output_dir))

        summary_file = output_dir / "summary.txt"
        stats_file = output_dir / "statistics.json"
        sentences_file = output_dir / "sentences_info.json"

        assert summary_file.exists()
        assert stats_file.exists()
        assert sentences_file.exists()

        summary_content = summary_file.read_text(encoding="utf-8")
        assert summary_content == result.summary_text

        stats_content = load_json(stats_file)
        assert (
            stats_content["original_sentences_count"]
            == result.statistics.original_sentences_count
        )
        assert stats_content["method_used"] == result.method_used.value

        sentences_content = load_json(sentences_file)
        assert len(sentences_content) == len(result.important_sentences)

    def test_different_compression_ratios(self, sample_text_long):
        summarizer = TextSummarizer()

        for ratio in [0.1, 0.3, 0.5, 0.7]:
            result = summarizer.summarize(sample_text_long, compression_ratio=ratio)

            expected_min = max(
                1, int(result.statistics.original_sentences_count * ratio * 0.8)
            )
            expected_max = max(
                1, int(result.statistics.original_sentences_count * ratio * 1.2)
            )

            actual_count = len(result.important_sentences)

            assert (
                expected_min <= actual_count <= expected_max
            ), f"Ratio {ratio}: expected {expected_min}-{expected_max}, got {actual_count}"

    def test_text_with_special_characters(self):
        text = """
        Текст с различными символами:
        Кавычки "вот такие", скобки (вот такие), тире — вот такое.
        Также есть числа: 123, 45.6, и спецсимволы: @#$%^&*.
        """

        summarizer = TextSummarizer()
        result = summarizer.summarize(text, compression_ratio=0.5)

        assert result.summary_text != ""
        assert result.statistics.original_sentences_count > 0
        assert result.statistics.original_words_count > 0

    def test_very_short_text(self):
        text = "Всего одно предложение."

        summarizer = TextSummarizer()
        result = summarizer.summarize(text, compression_ratio=0.5)

        assert result.summary_text != ""
        assert len(result.important_sentences) == 1
        assert result.statistics.compression_ratio == 0.0
