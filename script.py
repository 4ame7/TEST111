import json
import logging
import os
import sys
import pytesseract
from pdf2image import convert_from_path
images = convert_from_path("input.pdf", use_pdftocairo=True)
images = convert_from_path(
    "R:\bank.pdf",
    use_pdftocairo=True,  # Использовать Ghostscript вместо Poppler
    strict_poppler=False  # Игнорировать отсутствие Poppler
)
def check_tesseract_support(lang):
    """Проверка поддержки языка в Tesseract."""
    try:
        langs = pytesseract.get_languages()
        if lang not in langs:
            raise ValueError(f"Язык '{lang}' не поддерживается. Доступные языки: {langs}")
    except Exception as e:
        logging.error(f"Ошибка при проверке языков Tesseract: {e}")
        raise


def ocr_pdf_to_json(pdf_path, output_json, lang='eng'):
    """Извлечение текста из PDF с OCR и сохранение в JSON."""
    # Проверка существования файла
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Файл {pdf_path} не найден.")

    # Проверка поддержки языка
    check_tesseract_support(lang)

    # Конвертация PDF в изображения
    try:
        images = convert_from_path(pdf_path)
    except Exception as e:
        raise RuntimeError(f"Ошибка конвертации PDF: {e}")

    extracted_text = {}

    # Обработка каждой страницы
    for page_num, image in enumerate(images, start=1):
        try:
            text = pytesseract.image_to_string(image, lang=lang)
            extracted_text[f"page_{page_num}"] = text.strip()
        except pytesseract.TesseractError as e:
            logging.error(f"Ошибка OCR на странице {page_num}: {e}")
            extracted_text[f"page_{page_num}"] = ""
        except Exception as e:
            logging.error(f"Ошибка обработки страницы {page_num}: {e}")
            extracted_text[f"page_{page_num}"] = ""

    # Сохранение в JSON
    try:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(extracted_text, f, ensure_ascii=False, indent=4)
        logging.info(f"Текст сохранён в {output_json}")
    except Exception as e:
        raise IOError(f"Ошибка записи JSON: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <путь_к_pdf> <выходной_json>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_json = sys.argv[2]

    try:
        ocr_pdf_to_json(pdf_path, output_json, lang='eng')
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        sys.exit(1)