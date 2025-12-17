import pytest
import tempfile
import json
from pathlib import Path


@pytest.fixture
def sample_text_short():
    return "Это первое предложение. Это второе предложение. А это третье."


@pytest.fixture
def sample_text_long():
    return """
    Искусственный интеллект (ИИ) - это область компьютерных наук, которая занимается созданием
    интеллектуальных машин, способных выполнять задачи, обычно требующие человеческого интеллекта.
    Эти задачи включают распознавание речи, принятие решений, визуальное восприятие и перевод языков.

    Машинное обучение - это подраздел искусственного интеллекта, который использует алгоритмы
    для анализа данных, изучения закономерностей и принятия решений с минимальным вмешательством человека.
    Глубокое обучение - это тип машинного обучения, который использует нейронные сети с множеством слоев.

    Применение ИИ широко распространено в различных областях: медицина, финансы, транспорт, образование.
    Например, в медицине ИИ помогает в диагностике заболеваний, а в финансах - в обнаружении мошенничества.
    """


@pytest.fixture
def sample_text_with_numbers():
    return (
        "В 2023 году было проведено 15 исследований. Результаты показали рост на 25%."
    )


@pytest.fixture
def sample_sentences_list():
    return [
        "Искусственный интеллект - это важная область исследований.",
        "Машинное обучение является подразделом ИИ.",
        "Глубокое обучение использует нейронные сети.",
        "Применение ИИ широко распространено.",
        "В медицине ИИ помогает в диагностике.",
    ]


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_text_file(temp_dir):
    filepath = temp_dir / "test.txt"
    content = "Это тестовый текст.\nОн состоит из нескольких предложений.\nТретье предложение."
    filepath.write_text(content, encoding="utf-8")
    return filepath


@pytest.fixture
def frequency_summarizer():
    from src.textsummarizer.methods.frequency_based import FrequencyBasedSummarizer

    return FrequencyBasedSummarizer(use_stopwords=True)


@pytest.fixture
def feature_summarizer():
    from src.textsummarizer.methods.feature_based import FeatureBasedSummarizer

    return FeatureBasedSummarizer()
