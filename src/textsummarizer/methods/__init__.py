from .base import BaseSummarizer  # Не используется "снаружи" -> не должно быть доступно юзеру (инкапсуляция)
from .frequency_based import FrequencyBasedSummarizer
from .feature_based import FeatureBasedSummarizer

__all__ = ["BaseSummarizer", "FrequencyBasedSummarizer", "FeatureBasedSummarizer"]
