from typing import List, Dict, Set
import math
from collections import Counter
from .base import BaseSummarizer
from ..entities import Sentence
from ..utils.text_processing import preprocess_text, tokenize_words


class FrequencyBasedSummarizer(BaseSummarizer):
    def __init__(self, use_stopwords: bool = True):
        self.use_stopwords = use_stopwords
        self._stopwords = self._load_stopwords() if use_stopwords else set()

    def _load_stopwords(self) -> Set[str]:
        russian_stopwords = {
            "и",
            "в",
            "во",
            "не",
            "что",
            "он",
            "на",
            "я",
            "с",
            "со",
            "как",
            "а",
            "то",
            "все",
            "она",
            "так",
            "его",
            "но",
            "да",
            "ты",
            "к",
            "у",
            "же",
            "вы",
            "за",
            "бы",
            "по",
            "только",
            "ее",
            "мне",
            "было",
            "вот",
            "от",
            "меня",
            "еще",
            "нет",
            "о",
            "из",
            "ему",
            "теперь",
            "когда",
            "даже",
            "ну",
            "вдруг",
            "ли",
            "если",
            "уже",
            "или",
            "ни",
            "быть",
            "был",
            "него",
            "до",
            "вас",
            "нибудь",
            "опять",
            "уж",
            "вам",
            "ведь",
            "там",
            "потом",
            "себя",
            "ничего",
            "ей",
            "может",
            "они",
            "тут",
            "где",
            "есть",
            "надо",
            "ней",
            "для",
            "мы",
            "тебя",
            "их",
            "чем",
            "была",
            "сам",
            "чтоб",
            "без",
            "будто",
            "чего",
            "раз",
            "тоже",
            "себе",
            "под",
            "будет",
            "ж",
            "тогда",
            "кто",
            "этот",
            "того",
            "потому",
            "этого",
            "какой",
            "совсем",
            "ним",
            "здесь",
            "этом",
            "один",
            "почти",
            "мой",
            "тем",
            "чтобы",
            "нее",
            "сейчас",
            "были",
            "куда",
            "зачем",
            "всех",
            "никогда",
            "можно",
            "при",
            "наконец",
            "два",
            "об",
            "другой",
            "хоть",
            "после",
            "над",
            "больше",
            "тот",
            "через",
            "эти",
            "нас",
            "про",
            "всего",
            "них",
            "какая",
            "много",
            "разве",
            "три",
            "эту",
            "моя",
            "впрочем",
            "хорошо",
            "свою",
            "этой",
            "перед",
            "иногда",
            "лучше",
            "чуть",
            "том",
            "нельзя",
            "такой",
            "им",
            "более",
            "всегда",
            "конечно",
            "всю",
            "между",
        }
        return russian_stopwords

    def _calculate_tf_isf_scores(self, sentences: List[str]) -> List[float]:
        sentence_words = []
        word_document_freq = Counter()

        for sentence in sentences:
            processed_text = preprocess_text(
                sentence, lowercase=True, remove_punctuation=True, remove_numbers=False
            )

            words = tokenize_words(processed_text)
            if self.use_stopwords:
                words = [w for w in words if w not in self._stopwords]

            sentence_words.append(words)
            unique_words = set(words)
            for word in unique_words:
                word_document_freq[word] += 1

        num_sentences = len(sentences)
        scores = []

        for words in sentence_words:
            if not words:
                scores.append(0.0)
                continue

            word_counts = Counter(words)
            total_words = len(words)

            sentence_score = 0.0
            for word, count in word_counts.items():
                tf = count / total_words
                isf = math.log(num_sentences / (1 + word_document_freq[word]))
                sentence_score += tf * isf

            scores.append(sentence_score)

        return scores

    def summarize(
        self, sentences: List[str], compression_ratio: float
    ) -> List[Sentence]:
        if not sentences:
            return []

        scores = self._calculate_tf_isf_scores(sentences)
        num_to_select = max(1, int(len(sentences) * compression_ratio))
        scored_sentences = list(zip(sentences, scores, range(len(sentences))))
        scored_sentences.sort(key=lambda x: x[1], reverse=True)

        selected = []
        for i, (text, score, original_idx) in enumerate(
            scored_sentences[:num_to_select]
        ):
            sentence_obj = Sentence(
                text=text,
                position=original_idx,
                importance_score=score,
                is_important=True,
                features={"tf_isf_score": score},
            )
            selected.append(sentence_obj)

        selected.sort(key=lambda x: x.position)

        return selected
