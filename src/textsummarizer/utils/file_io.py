# Не отсортированы импорты, нет докстрингов

import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Union
import logging

logger = logging.getLogger(__name__)


def read_text_file(filepath: Union[str, Path], encoding: str = "utf-8") -> str:
    path = Path(filepath)

    if not path.exists():
        error_msg = f"Файл не найден: {filepath}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        with open(path, "r", encoding=encoding) as file:
            content = file.read()
        logger.info(f"Файл успешно прочитан: {filepath}")
        return content
    except UnicodeDecodeError as e:
        # (Совет) Под `except` используйте `logger.exception`, чтобы получить в консоли Traceback.
        # Это бывает полезно при отладке
        error_msg = f"Ошибка кодировки файла {filepath}: {e}"
        logger.error(error_msg)
        raise


def write_text_file(
    filepath: Union[str, Path], content: str, encoding: str = "utf-8"
) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding=encoding) as file:
        file.write(content)

    logger.info(f"Текст записан в файл: {filepath}")


def save_json(
    filepath: Union[str, Path], data: Union[Dict, List], indent: int = 2
) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        # file - Expected type 'SupportsWrite[str]', got 'TextIO' instead
        json.dump(data, file, ensure_ascii=False, indent=indent)

    logger.info(f"Данные сохранены в JSON: {filepath}")


def load_json(filepath: Union[str, Path]) -> Union[Dict, List]:
    path = Path(filepath)

    if not path.exists():
        error_msg = f"JSON файл не найден: {filepath}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        logger.info(f"Данные загружены из JSON: {filepath}")
        return data
    except json.JSONDecodeError as e:
        error_msg = f"Ошибка чтения JSON файла {filepath}: {e}"
        logger.error(error_msg)
        raise


def save_csv(filepath: Union[str, Path], data: List[Dict[str, Any]]) -> None:
    if not data:
        logger.warning("Нет данных для сохранения в CSV")
        return

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = data[0].keys()

    with open(path, "w", newline="", encoding="utf-8") as file:
        # file - Expected type 'SupportsWrite[str]', got 'TextIO' instead
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    logger.info(f"Данные сохранены в CSV: {filepath}")
