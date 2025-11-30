from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


class SummaryMethod(Enum):
    FREQUENCY_BASED = "frequency"
    FEATURE_BASED = "feature_based"


@dataclass
class Sentence:
    text: str
    position: int
    features: Dict[str, float] = None
    importance_score: float = 0.0
    is_important: bool = False


@dataclass
class TextStats:
    original_sentences_count: int
    original_words_count: int
    summary_sentences_count: int
    summary_words_count: int
    compression_ratio: float
    avg_sentence_length: float
    lexical_diversity: float
    reading_time_minutes: float


@dataclass
class SummaryResult:
    original_text: str
    summary_text: str
    important_sentences: List[Sentence]
    statistics: TextStats
    method_used: SummaryMethod
