import time
from loguru import logger
from tqdm import tqdm
from .config import BLT_BASE_URL_2
from .prompts import set_translator_prompt, wrap_prompt
from .utils import preprocess_text, save_translations, perview_paragraphs
from .chatbot import Chatbot


logger.add(
    "translator.log", format="{time:YYYY-MM-DD HH:mm:ss}|{message}", level="INFO"
)


def init_chatbot(
    api_key,
    model="gpt-4o-mini",
    base_url="https://api.bltcy.ai/v1",
    system_prompt=None,
    initial_assistant_message=None,
    max_tokens=1024,
    temperature=0.7,
    max_history_length=10,
) -> Chatbot:
    return Chatbot(
        api_key,
        model,
        base_url,
        system_prompt,
        initial_assistant_message,
        max_tokens,
        temperature,
        max_history_length,
    )


def get_chatbot_response(
    user_prompt, bot, stream=True, print_response=True, debug=True
):
    return bot.get_response(user_prompt, stream, print_response, debug)


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
    min_chars_per_paragraph: int = 10,
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
        min_chars_per_paragraph (int, optional): 每段最小字数. Defaults to 10.
        debug (bool, optional): 是否开启debug模式. Defaults to False.
    """
    start_time = time.time()
    with open(original_text_md, "r", encoding="utf-8") as f:
        paragraphs, num_paragraphs = preprocess_text(
            f.read(),
            max_chars=max_chars_per_paragraph,
            min_chars=min_chars_per_paragraph,
        )

    # 根据模式设置翻译范围
    if mode in ["全部", "all", "All", "a"]:
        translate_count = num_paragraphs
        start_paragraph = 0
    elif mode in ["分段", "segment", "Segment", "s"]:
        translate_count = min(translate_paragraphs, num_paragraphs - start_paragraph)
    else:
        raise ValueError(f"不支持的翻译模式/Unsupported translation mode：{mode}")

    total_chars = perview_paragraphs(mode, paragraphs, start_paragraph, translate_count)
    print("*" * 8 + f" 开 始 翻 译 / TRANSLATING " + "*" * 8)

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
    logger.info("-" * 12 + f" 翻译完成/Translation finished " + "-" * 12)
    logger.info(
        f"翻译文档/Document：{original_text_md}，输出文档/Output：{result_text_docx}"
    )
    logger.info(f"翻译模式/Translation mode：{mode}")
    logger.info(f"从第{start_paragraph}段开始翻译{translate_count}段")
    logger.info(
        f"Translated {translate_count} paragraphs from paragraph {start_paragraph}"
    )
    logger.info(f"翻译段落数/Paragraphs translated：{translate_count}")
    logger.info(f"总耗时（秒）/Total time (s)：{total_time:.2f}")
    logger.info(f"原文字数/Total characters：{total_chars}")
    logger.info(f"每秒字数/Characters per second：{total_chars / total_time:.2f}")
    logger.info(
        f"总成本/Total cost：￥{total_cost_rmb:.2f}(${total_cost_rmb / 7.3:.2f})"
    )
    logger.info(
        f"千字成本/Cost per thousand characters：￥{total_cost_rmb / total_chars * 1000:.2f}(${total_cost_rmb / total_chars * 1000 / 7.3:.2f})"
    )
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
    result_text_docx="results/102_Liu_Cong.docx",
    translate_paragraphs=5,
    start_paragraph=0,
    mode="分段",
    max_chars_per_paragraph=500,
    min_chars_per_paragraph=10,
    debug=False,
    special_instructions="",
):
    system_prompt = set_translator_prompt(
        document=document,
        document_type=document_type,
        original_language=original_language,
        target_language=target_language,
        subject=subject,
        special_instructions=special_instructions,
    )

    if debug:
        logger.debug(
            f"如需修改系统提示词，前往prompts.py/Modify system prompt in prompts.py if needed."
        )
        logger.debug(f"请确认系统提示词/Confirm system prompt：\n{system_prompt}")

    bot = init_chatbot(
        api_key=api_key,
        model=model,
        base_url=base_url,
        system_prompt=system_prompt,
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
        min_chars_per_paragraph,
        debug,
    )
