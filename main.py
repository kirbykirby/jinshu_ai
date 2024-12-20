import os
from translator import init_translator_and_translate, BLT_BASE_URL_2
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    BLT_KEY = os.environ.get("BLT_KEY")
    additional_instructions = """
- Convert dates to Western calendar in parentheses. Examples: the first year of Yongjia (307), the Yongjia period (307-313)
- Use (DATE) if year is uncertain.
- Maintain a tone appropriate for historical context and avoid modern colloquialisms.
- Preserve cultural context and historical authenticity.
- Note significant allusions with * and include brief context in footnotes.
"""
    init_translator_and_translate(
        api_key=BLT_KEY,
        model="claude-3-5-sonnet-latest",
        base_url=BLT_BASE_URL_2,
        document="Book of Jin",
        document_type="historical records",
        original_language="Classical-Chinese",
        target_language="English",
        subject="慕容超",
        original_text_md="original_text/128.md",
        result_text_docx="results/128_Murong_Chao.docx",
        translate_paragraphs=1,
        start_paragraph=0,
        mode="a",
        max_chars_per_paragraph=400,
        min_chars_per_paragraph=15,
        debug=True,
        special_instructions=additional_instructions,
    )
