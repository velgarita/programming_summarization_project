from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class SummaryMethod(Enum):
    FREQUENCY_BASED = "frequency"
    FEATURE_BASED = "feature_based"


@dataclass
class Sentence:
    text: str
    position: int
    features: Optional[Dict[str, float]] = None
    importance_score: float = 0.0
    is_important: bool = False

    def __post_init__(self):
        if self.features is None:
            self.features = {}


@dataclass
class ReadabilityMetrics:
    flesch_score: float
    avg_sentence_length: float
    avg_word_length: float
    lexical_diversity: float
    total_sentences: int
    total_words: int
    unique_words: int


@dataclass
class TextStats:
    original_sentences_count: int
    original_words_count: int
    summary_sentences_count: int
    summary_words_count: int
    compression_ratio: float
    reading_time_minutes: float
    original_readability: ReadabilityMetrics
    summary_readability: ReadabilityMetrics


@dataclass
class SummaryResult:
    original_text: str
    summary_text: str
    important_sentences: List[Sentence]
    statistics: TextStats
    method_used: SummaryMethod
