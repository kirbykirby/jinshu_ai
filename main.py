import os
from translator import init_translator_and_translate, BLT_BASE_URL_2, Jinshu_translator_prompt
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    BLT_KEY = os.environ.get("BLT_KEY")
    init_translator_and_translate(
        api_key=BLT_KEY,
        model="claude-3-5-sonnet-latest",
        base_url=BLT_BASE_URL_2,
        document="Book of Jin",
        document_type="historical records",
        original_language="Classical-Chinese",
        target_language="English",
        subject="四夷",
        original_text_md="original_text/097.md",
        result_text_docx="results/097_Four_Barbarians.docx",
        translate_paragraphs=1,
        start_paragraph=0,
        mode="a",
        max_chars_per_paragraph=400,
        min_chars_per_paragraph=15,
        debug=True,
        special_instructions=Jinshu_translator_prompt,
    )
