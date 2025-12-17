import pytest
from src.textsummarizer.core import TextSummarizer
from src.textsummarizer.entities import SummaryMethod


class TestTextSummarizer:
    def test_initialization_default_method(self):
        summarizer = TextSummarizer()
        assert summarizer.method == SummaryMethod.FEATURE_BASED

    def test_initialization_frequency_method(self):
        summarizer = TextSummarizer(method=SummaryMethod.FREQUENCY_BASED)
        assert summarizer.method == SummaryMethod.FREQUENCY_BASED

    def test_initialization_feature_method(self):
        summarizer = TextSummarizer(method=SummaryMethod.FEATURE_BASED)
        assert summarizer.method == SummaryMethod.FEATURE_BASED

    def test_summarize_empty_text(self):
        summarizer = TextSummarizer()
        result = summarizer.summarize("", compression_ratio=0.3)

        assert result.summary_text == ""
        assert len(result.important_sentences) == 0
        assert result.statistics.original_sentences_count == 0
        assert result.statistics.original_words_count == 0

    def test_summarize_short_text(self, sample_text_short):
        summarizer = TextSummarizer()
        result = summarizer.summarize(sample_text_short, compression_ratio=0.5)

        assert result.summary_text != ""
        assert len(result.important_sentences) > 0
        assert len(result.summary_text.split()) <= len(sample_text_short.split())

    def test_summarize_invalid_compression_ratio(self):
        summarizer = TextSummarizer()

        with pytest.raises(
            ValueError, match="compression_ratio должен быть в диапазоне"
        ):
            summarizer.summarize("Текст", compression_ratio=0)

        with pytest.raises(
            ValueError, match="compression_ratio должен быть в диапазоне"
        ):
            summarizer.summarize("Текст", compression_ratio=1.5)

    def test_summarize_different_methods(self, sample_text_short):
        text = sample_text_short

        feature_summarizer = TextSummarizer(method=SummaryMethod.FEATURE_BASED)
        feature_result = feature_summarizer.summarize(text, compression_ratio=0.5)

        frequency_summarizer = TextSummarizer(method=SummaryMethod.FREQUENCY_BASED)
        frequency_result = frequency_summarizer.summarize(text, compression_ratio=0.5)

        assert feature_result.summary_text != ""
        assert frequency_result.summary_text != ""

        assert feature_result.method_used == SummaryMethod.FEATURE_BASED
        assert frequency_result.method_used == SummaryMethod.FREQUENCY_BASED

    def test_save_result(self, sample_text_short, temp_dir):
        summarizer = TextSummarizer()
        result = summarizer.summarize(sample_text_short, compression_ratio=0.5)

        output_dir = temp_dir / "output"
        summarizer.save_result(result, str(output_dir))

        assert (output_dir / "summary.txt").exists()
        assert (output_dir / "statistics.json").exists()
        assert (output_dir / "sentences_info.json").exists()

        summary_content = (output_dir / "summary.txt").read_text(encoding="utf-8")
        assert summary_content == result.summary_text
