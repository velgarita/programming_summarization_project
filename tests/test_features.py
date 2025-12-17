import pytest
from src.textsummarizer.methods.frequency_based import FrequencyBasedSummarizer
from src.textsummarizer.methods.feature_based import FeatureBasedSummarizer


class TestFrequencyBasedSummarizer:
    def test_initialization(self, frequency_summarizer):
        assert frequency_summarizer.use_stopwords is True

    def test_initialization_without_stopwords(self):
        summarizer = FrequencyBasedSummarizer(use_stopwords=False)
        assert summarizer.use_stopwords is False

    def test_load_stopwords(self, frequency_summarizer):
        stopwords = frequency_summarizer._load_stopwords()
        assert isinstance(stopwords, set)
        assert len(stopwords) > 0
        assert "и" in stopwords
        assert "в" in stopwords

    def test_calculate_tf_isf_scores(self, frequency_summarizer, sample_sentences_list):
        scores = frequency_summarizer._calculate_tf_isf_scores(sample_sentences_list)

        assert len(scores) == len(sample_sentences_list)
        assert all(isinstance(score, float) for score in scores)

    def test_summarize_empty_list(self, frequency_summarizer):
        result = frequency_summarizer.summarize([], compression_ratio=0.3)
        assert result == []

    def test_summarize_single_sentence(self, frequency_summarizer):
        sentences = ["Одно предложение."]
        result = frequency_summarizer.summarize(sentences, compression_ratio=0.5)

        assert len(result) == 1
        assert result[0].text == sentences[0]
        assert result[0].is_important is True

    def test_summarize_multiple_sentences(
        self, frequency_summarizer, sample_sentences_list
    ):
        compression_ratio = 0.4
        result = frequency_summarizer.summarize(
            sample_sentences_list, compression_ratio
        )

        expected_count = max(1, int(len(sample_sentences_list) * compression_ratio))
        assert len(result) == expected_count

        assert all(sentence.is_important for sentence in result)

        positions = [sentence.position for sentence in result]
        assert positions == sorted(positions)


class TestFeatureBasedSummarizer:
    def test_initialization(self, feature_summarizer):
        assert feature_summarizer._position_weights["first"] == 1.0
        assert feature_summarizer._position_weights["last"] == 0.8
        assert feature_summarizer._position_weights["middle"] == 0.3

    def test_extract_features(self, feature_summarizer, sample_sentences_list):
        features = feature_summarizer._extract_features(
            sample_sentences_list[0], idx=0, total_sentences=len(sample_sentences_list)
        )

        expected_features = [
            "position_score",
            "length_score",
            "has_numbers",
            "proper_noun_ratio",
            "lexical_diversity",
            "keyword_score",
            "readability_score",
        ]

        for feature in expected_features:
            assert feature in features
            assert isinstance(features[feature], float)

    def test_calculate_position_score(self, feature_summarizer):
        assert feature_summarizer._calculate_position_score(0, 10) == 1.0
        assert feature_summarizer._calculate_position_score(9, 10) == 0.8

        score = feature_summarizer._calculate_position_score(5, 10)
        assert score >= 0.0
        assert score <= 1.0

        score_edge_1 = feature_summarizer._calculate_position_score(1, 10)
        score_edge_8 = feature_summarizer._calculate_position_score(8, 10)
        assert abs(score_edge_1 - score_edge_8) < 0.001

    def test_calculate_length_score(self, feature_summarizer):
        assert feature_summarizer._calculate_length_score(15) == 1.0
        assert feature_summarizer._calculate_length_score(20) == 1.0
        assert feature_summarizer._calculate_length_score(25) == 1.0

        assert feature_summarizer._calculate_length_score(10) == 0.7
        assert feature_summarizer._calculate_length_score(30) == 0.7

        assert feature_summarizer._calculate_length_score(5) == 0.4
        assert feature_summarizer._calculate_length_score(40) == 0.4

        assert feature_summarizer._calculate_length_score(1) == 0.1
        assert feature_summarizer._calculate_length_score(50) == 0.1

    def test_calculate_importance_score(self, feature_summarizer):
        features = {
            "position_score": 1.0,
            "length_score": 1.0,
            "has_numbers": 1.0,
            "proper_noun_ratio": 1.0,
            "lexical_diversity": 1.0,
            "keyword_score": 1.0,
            "readability_score": 1.0,
        }

        score = feature_summarizer._calculate_importance_score(features)
        assert 0 <= score <= 1.0
        assert score > 0

    def test_summarize(self, feature_summarizer, sample_sentences_list):
        compression_ratio = 0.4
        result = feature_summarizer.summarize(sample_sentences_list, compression_ratio)

        expected_count = max(1, int(len(sample_sentences_list) * compression_ratio))
        assert len(result) == expected_count

        for sentence in result:
            assert sentence.text in sample_sentences_list
            assert sentence.position >= 0
            assert 0 <= sentence.importance_score <= 1.0
            assert sentence.is_important is True
            assert isinstance(sentence.features, dict)
