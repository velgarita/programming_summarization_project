__version__ = "0.1.0"  # Раз у вас есть `pyproject.toml`, указывайте версию там.
# Начинайте не с нулевой, а с первой версии - 1.0.0

from .core import TextSummarizer
from .entities import SummaryMethod, SummaryResult

__all__ = [
    "TextSummarizer",
    "SummaryMethod",
    "SummaryResult",
]
