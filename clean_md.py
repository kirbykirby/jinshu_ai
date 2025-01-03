from loguru import logger
import time


def clean_md(md_file):
    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    logger.info(
        "本脚本只能清洗这里的数据：https://ctext.org/wiki.pl?if=gb&res=788577&remap=gb"
    )
    logger.info("清洗逻辑：1.删除前20行和最后2行 2.确定行首为数字或《 ")

    if lines[0][0].isdigit() or lines[0][0] == "《":
        logger.warning("文档似乎已经清洗过了，是否继续清洗？(y/n): ")
        if_clean = input()
        if if_clean.lower() == "n":
            logger.info("取消清洗文档！")
            return

    start_time = time.time()
    logger.info("开始清洗文档！")

    # 删除前20行和最后2行
    lines = lines[20:-2]

    cleaned_lines = []
    current_text = ""

    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue

        # 如果行首是数字或《，说明是新段落的开始
        if line[0].isdigit() or line[0] == "《":
            # 保存之前的文本
            if current_text:
                cleaned_lines.append(current_text)
            current_text = line
        else:
            # 不是新段落的开始，则与当前文本合并
            current_text += line

    # 添加最后一段文本
    if current_text:
        cleaned_lines.append(current_text)

    with open(md_file, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))

    duration = time.time() - start_time
    logger.info(f"清洗完成，耗时：{duration * 1000:.2f}毫秒")
    get_md_word_count(md_file)


def get_md_word_count(md_file):
    with open(md_file, "r", encoding="utf-8") as f:
        text = f.read()
    logger.info(f"清洗后的文档字数/Character count after cleaning：{len(text)}")
    return len(text)


if __name__ == "__main__":
    clean_md("1_SOURCE/097.md")
