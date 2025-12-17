__version__ = "0.1.0"

from .core import TextSummarizer
from .entities import SummaryMethod, SummaryResult

__all__ = [
    "TextSummarizer",
    "SummaryMethod",
    "SummaryResult",
]
