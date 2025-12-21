# Не отсортированы импорты, почти нигде нет докстрингов

# Этот файл должен лежать в корне `src`, поскольку не является частью модуля `textsummarizer`.
# И `__main__.py` в таком случае писать не нужно было. Вместо этого нужно было запускать `cli.py` напрямую.

import click
import logging
from pathlib import Path
from typing import Optional
from .core import TextSummarizer
from .entities import SummaryMethod
from .utils.file_io import read_text_file, write_text_file, save_json
# Вы вынесли `read_text_file`, `write_text_file`, `save_json` в `utils/__init__.py`,
# поэтому можете импортировать их напрямую из `utils`
from .utils.vizualization import (
    plot_sentence_scores,
    plot_summary_comparison,
    plot_readability_metrics,
)
# То же самое

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--input", "-i", required=True, help="Входной текстовый файл")
@click.option(
    "--output", "-o", help="Выходной файл с саммари (по умолчанию: input_summary.txt)"
)
@click.option(
    "--method",
    "-m",
    type=click.Choice(["frequency", "feature"]),
    default="feature",
    help="Метод саммаризации (frequency или feature)",
)
@click.option(
    "--ratio",
    "-r",
    type=float,
    default=0.3,
    help="Коэффициент сжатия (0.0-1.0, по умолчанию 0.3)",
)
@click.option("--stats", "-s", is_flag=True, help="Сохранять статистику в JSON")
@click.option("--visualize", "-v", is_flag=True, help="Создавать визуализации")
@click.option("--output-dir", "-d", help="Директория для выходных файлов")
def summarize(input, output, method, ratio, stats, visualize, output_dir):
    try:
        logger.info(f"Чтение файла: {input}")
        text = read_text_file(input)

        summary_method = (
            SummaryMethod.FREQUENCY_BASED
            if method == "frequency"
            else SummaryMethod.FEATURE_BASED
        )

        summarizer = TextSummarizer(method=summary_method)

        logger.info(f"Саммаризация методом: {method}, коэффициент сжатия: {ratio}")
        result = summarizer.summarize(text, compression_ratio=ratio)

        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = Path(input).parent

        if output:
            summary_file = Path(output)
        else:
            input_stem = Path(input).stem
            summary_file = output_path / f"{input_stem}_summary.txt"

        write_text_file(summary_file, result.summary_text)
        logger.info(f"Саммари сохранен в: {summary_file}")

        if stats:
            stats_file = output_path / f"{Path(input).stem}_stats.json"
            stats_data = {
                "original_sentences_count": result.statistics.original_sentences_count,
                "original_words_count": result.statistics.original_words_count,
                "summary_sentences_count": result.statistics.summary_sentences_count,
                "summary_words_count": result.statistics.summary_words_count,
                "compression_ratio": result.statistics.compression_ratio,
                "reading_time_minutes": result.statistics.reading_time_minutes,
                "method_used": result.method_used.value,
                "original_readability": {
                    "flesch_score": result.statistics.original_readability.flesch_score,
                    "avg_sentence_length": result.statistics.original_readability.avg_sentence_length,
                    "avg_word_length": result.statistics.original_readability.avg_word_length,
                    "lexical_diversity": result.statistics.original_readability.lexical_diversity,
                },
                "summary_readability": {
                    "flesch_score": result.statistics.summary_readability.flesch_score,
                    "avg_sentence_length": result.statistics.summary_readability.avg_sentence_length,
                    "avg_word_length": result.statistics.summary_readability.avg_word_length,
                    "lexical_diversity": result.statistics.summary_readability.lexical_diversity,
                },
            }
            save_json(stats_file, stats_data)
            logger.info(f"Статистика сохранена в: {stats_file}")

        if visualize:
            vis_dir = output_path / "visualizations"
            vis_dir.mkdir(exist_ok=True)

            sentences = [sent.text for sent in result.important_sentences]
            scores = [sent.importance_score for sent in result.important_sentences]

            if sentences and scores:
                plot_sentence_scores(
                    sentences, scores, save_path=str(vis_dir / "sentence_scores.png")
                )

                original_stats = {
                    "total_sentences": result.statistics.original_readability.total_sentences,
                    "total_words": result.statistics.original_readability.total_words,
                    "unique_words": result.statistics.original_readability.unique_words,
                }
                summary_stats = {
                    "total_sentences": result.statistics.summary_readability.total_sentences,
                    "total_words": result.statistics.summary_readability.total_words,
                    "unique_words": result.statistics.summary_readability.unique_words,
                }
                plot_summary_comparison(
                    original_stats,
                    summary_stats,
                    save_path=str(vis_dir / "summary_comparison.png"),
                )

                readability_metrics = {
                    "Индекс Флеша": result.statistics.original_readability.flesch_score,
                    "Длина предложения": result.statistics.original_readability.avg_sentence_length,
                    "Длина слова": result.statistics.original_readability.avg_word_length,
                    "Лексическое разнообразие": result.statistics.original_readability.lexical_diversity,
                }
                plot_readability_metrics(
                    readability_metrics,
                    save_path=str(vis_dir / "readability_metrics.png"),
                )

            logger.info(f"Визуализации сохранены в: {vis_dir}")

        click.echo(f"\n{'='*50}")
        click.echo("Саммаризация завершена успешно!")
        click.echo(
            f"Оригинальный текст: {result.statistics.original_sentences_count} предложений, "
            f"{result.statistics.original_words_count} слов"
        )
        click.echo(
            f"Саммари: {result.statistics.summary_sentences_count} предложений, "
            f"{result.statistics.summary_words_count} слов"
        )
        click.echo(f"Коэффициент сжатия: {result.statistics.compression_ratio:.1%}")
        click.echo(
            f"Индекс Флеша (оригинал): {result.statistics.original_readability.flesch_score:.1f}"
        )
        click.echo(
            f"Индекс Флеша (саммари): {result.statistics.summary_readability.flesch_score:.1f}"
        )
        click.echo(f"{'='*50}")

    except Exception as e:
        logger.error(f"Ошибка при выполнении саммаризации: {e}")
        raise click.ClickException(f"Ошибка: {e}")


@cli.command()
@click.option("--text", "-t", help="Текст для анализа")
@click.option("--file", "-f", help="Файл с текстом для анализа")
def analyze(text, file):
    try:
        if text:
            input_text = text
        elif file:
            input_text = read_text_file(file)
        else:
            raise click.BadParameter("Необходимо указать --text или --file")

        from .utils.text_processing import split_into_sentences

        sentences = split_into_sentences(input_text)

        from .utils.text_processing import calculate_readability_metrics

        metrics = calculate_readability_metrics(input_text)

        click.echo(f"\n{'='*50}")
        click.echo("Анализ текста:")
        click.echo(f"Количество предложений: {len(sentences)}")
        click.echo(f"Количество слов: {metrics.get('total_words', 0)}")
        click.echo(f"Уникальных слов: {metrics.get('unique_words', 0)}")
        click.echo(
            f"Индекс Флеша (читабельность): {metrics.get('flesch_score', 0):.1f}"
        )
        click.echo(
            f"Средняя длина предложения: {metrics.get('avg_sentence_length', 0):.1f} слов"
        )
        click.echo(
            f"Лексическое разнообразие: {metrics.get('lexical_diversity', 0):.3f}"
        )

        click.echo(f"\nПримеры предложений:")
        for i, sent in enumerate(sentences[:3], 1):
            click.echo(f"  {i}. {sent[:80]}{'...' if len(sent) > 80 else ''}")
        if len(sentences) > 3:
            click.echo(f"  ... и еще {len(sentences) - 3} предложений")
        click.echo(f"{'='*50}")

    except Exception as e:
        logger.error(f"Ошибка при анализе текста: {e}")
        raise click.ClickException(f"Ошибка: {e}")


@cli.command()
def version():
    """Показывает версию пакета."""
    click.echo("TextSummarizer v0.1.0")


def main():
    """Точка входа CLI."""
    cli()


if __name__ == "__main__":
    main()
