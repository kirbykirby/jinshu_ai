import os
from translator import init_translator_and_translate, BLT_BASE_URL_2
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    BLT_KEY = os.environ.get("BLT_KEY")
    additional_instructions = """
- Convert dates to the Western calendar in parentheses (e.g., the first year of Yongjia (307), the Yongjia period (307-313)) or use (DATE) if uncertain.
- Maintain a tone appropriate for historical context and avoid modern colloquialisms.
"""
    init_translator_and_translate(
        api_key=BLT_KEY,
        model="claude-3-5-sonnet-latest",
        base_url=BLT_BASE_URL_2,
        document="Book of Jin",
        document_type="historical records",
        original_language="Classical-Chinese",
        target_language="English",
        subject="慕容垂",
        original_text_md="original_text/123.md",
        result_text_docx="results/123_Murong_Chui.docx",
        translate_paragraphs=15,
        start_paragraph=29,
        mode="全部",
        max_chars_per_paragraph=400,
        min_chars_per_paragraph=15,
        debug=True,
        special_instructions=additional_instructions,
    )
