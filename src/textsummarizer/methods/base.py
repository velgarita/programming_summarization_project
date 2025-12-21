# Не отсортированы импорты, нет докстрингов

from abc import ABC, abstractmethod
from typing import List
from ..entities import Sentence


class BaseSummarizer(ABC):
    @abstractmethod
    def summarize(
        self, sentences: List[str], compression_ratio: float
    ) -> List[Sentence]:
        pass

    def _prepare_text(self, text: str) -> List[str]:  # Method '_prepare_text' may be 'static'
        import re

        # Удаляем пунктуацию, приводим к нижнему регистру
        text = re.sub(r"[^\w\s]", " ", text)
        words = text.lower().split()
        return words
