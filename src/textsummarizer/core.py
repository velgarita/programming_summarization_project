from typing import Dict, List


class FeatureExtractor:
    
    def extract_features(self, sentence: str, entire_text: List[str]) -> Dict[str, float]:
        features = {}
        features['sentence_length'] = len(sentence.split())
        features['unique_words_ratio'] = self._unique_words_ratio(sentence)
        features['contains_digits'] = self._contains_digits(sentence)
        features['tf_isf_score'] = self._calculate_tf_isf(sentence, entire_text)
        features['noun_ratio'] = self._pos_ratio(sentence, 'NOUN')
        features['verb_ratio'] = self._pos_ratio(sentence, 'VERB')
        features['proper_noun_count'] = self._count_proper_nouns(sentence)
        return features

class TextSummarizer:
    
    def __init__(self, method: SummaryMethod):
        self.method = method
        self.feature_extractor = FeatureExtractor()
        self.classifier = None
        
    def summarize(self, text: str, compression_ratio: float = 0.3) -> SummaryResult:
        sentences = self._split_into_sentences(text)
        features = self._extract_sentence_features(sentences)
        important_sentences = self._select_important_sentences(sentences, features, compression_ratio)
        summary_text = self._construct_summary(important_sentences)
        statistics = self._calculate_statistics(text, summary_text)
        
        return SummaryResult(
            original_text=text,
            summary_text=summary_text,
            important_sentences=important_sentences,
            statistics=statistics,
            method_used=self.method
        )

class StatisticsCalculator:
    
    def calculate_comparison_stats(self, original: str, summary: str) -> TextStats:
        original_sentences = self._split_into_sentences(original)
        summary_sentences = self._split_into_sentences(summary)
        
        return TextStats(
            original_sentences_count=len(original_sentences),
            original_words_count=len(original.split()),
            summary_sentences_count=len(summary_sentences),
            summary_words_count=len(summary.split()),
            compression_ratio=1 - (len(summary.split()) / len(original.split())),
            avg_sentence_length=self._avg_sentence_length(original_sentences),
            lexical_diversity=self._lexical_diversity(original),
            reading_time_minutes=self._estimate_reading_time(original)
        )