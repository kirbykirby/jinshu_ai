import os
import time
from loguru import logger
from tqdm import tqdm
from translator import (
    Chatbot,
    init_chatbot,
    BLT_BASE_URL_2,
    set_translator_prompt,
    wrap_prompt,
    preprocess_text,
    save_translations,
    perview_paragraphs,
    reformat_docx,
)
from dotenv import load_dotenv

load_dotenv()
BLT_KEY = os.environ.get("BLT_KEY")
logger.add("translator.log", format="{time}|{message}")


def translate_paragraph(bot: Chatbot, paragraph: str, debug: bool = False):
    response, stat = bot.get_response(
        wrap_prompt(paragraph), stream=True, print_response=debug, debug=debug
    )
    return response.strip(), stat


def translate(
        bot: Chatbot,
        original_text_md: str,
        result_text_docx: str,
        translate_paragraphs: int = 5,
        start_paragraph: int = 0,
        mode: str = "分段",
        max_chars_per_paragraph: int = 500,
        debug: bool = False,
):
    """
    翻译指定md文件，并将翻译结果保存到docx文件

    Args:
        bot: Translator bot instance
        original_text_md (str): md文件路径
        result_text_docx (str): docx文件路径
        translate_paragraphs (int, optional): 翻译的段落数. Defaults to 5.
        start_paragraph (int, optional): 开始翻译的段落数. Defaults to 0.
        mode (str, optional): 翻译模式 ["全部"|"分段"]. Defaults to "分段".
        max_chars_per_paragraph (int, optional): 每段最大字数. Defaults to 500.
        debug (bool, optional): 是否开启debug模式. Defaults to False.
    """
    start_time = time.time()
    with open(original_text_md, "r", encoding="utf-8") as f:
        paragraphs, num_paragraphs = preprocess_text(
            f.read(), max_chars=max_chars_per_paragraph
        )

    # 根据模式设置翻译范围
    if mode == "全部":
        translate_count = num_paragraphs
        start_paragraph = 0
        print(f"将翻译全部{translate_count}段")
    else:  # 分段模式
        translate_count = min(translate_paragraphs, num_paragraphs - start_paragraph)
        print(f"将从第{start_paragraph}段开始翻译{translate_count}段")

    total_chars = perview_paragraphs(mode, paragraphs, start_paragraph, translate_count)
    print("*****开始翻译*****")

    total_cost_rmb = 0
    translated_paragraphs = []
    for i in tqdm(
            range(start_paragraph, start_paragraph + translate_count),
            desc="翻译进度",
            total=translate_count,
            unit="段",
    ):
        translated_paragraph, stat = translate_paragraph(bot, paragraphs[i], debug)
        translated_paragraphs.append(translated_paragraph)
        total_cost_rmb = stat["total_cost_rmb"]

    save_translations(result_text_docx, translated_paragraphs)
    total_time = time.time() - start_time
    logger.info("-" * 12 + f" 翻译完成 " + "-" * 12)
    logger.info(f"翻译模式：{mode}")
    logger.info(f"从第{start_paragraph}段开始翻译{translate_count}段")
    logger.info(f"翻译段落数：{translate_count}")
    logger.info(f"总耗时：{total_time:.2f}秒")
    logger.info(f"原文字数：{total_chars}")
    logger.info(f"每秒字数：{total_chars / total_time:.2f}")
    logger.info(f"总成本：{total_cost_rmb:.2f}元")
    logger.info(f"千字成本：{total_cost_rmb / total_chars * 1000:.2f}元/千字")
    logger.info("-" * 30)


def init_translator_and_translate(
        api_key,
        model="claude-3-5-sonnet-latest",
        base_url=BLT_BASE_URL_2,
        document="Book of Jin",
        document_type="historical records",
        original_language="Classical Chinese",
        target_language="English",
        subject="Liu Cong",
        original_text_md="original_text/102_Liu_Cong.md",
        result_text_docx="results/Liu_Cong.docx",
        translate_paragraphs=5,
        start_paragraph=0,
        mode="分段",
        max_chars_per_paragraph=500,
        debug=False,
        special_instructions="",
):
    bot = init_chatbot(
        api_key=api_key,
        model=model,
        base_url=base_url,
        system_prompt=set_translator_prompt(
            document=document,
            document_type=document_type,
            original_language=original_language,
            target_language=target_language,
            subject=subject,
            special_instructions=special_instructions,
        ),
        initial_assistant_message=None,
        max_tokens=1024,
        temperature=0.2,
        max_history_length=10,
    )
    translate(
        bot,
        original_text_md,
        result_text_docx,
        translate_paragraphs,
        start_paragraph,
        mode,
        max_chars_per_paragraph,
        debug,
    )


if __name__ == "__main__":
    additional_instructions = """
    - Convert Chinese era to Western calendar or use (DATE) if uncertain
    - Maintain a tone suitable for historical context
    - Avoid modern colloquialisms
    """
    init_translator_and_translate(
        api_key=BLT_KEY,
        model="claude-3-5-sonnet-latest",
        base_url=BLT_BASE_URL_2,
        document="Book of Jin",
        document_type="historical records",
        original_language="Classical Chinese",
        target_language="English",
        subject="Murong Huang",
        original_text_md="original_text/109_Murong_Huang.md",
        result_text_docx="results/Murong_Huang.docx",
        translate_paragraphs=1,
        start_paragraph=53,
        mode="全部",
        max_chars_per_paragraph=500,
        debug=True,
        special_instructions=additional_instructions,
    )
