import os
import re
import string
from docx import Document
from .formatter import set_document_style, replace_multiple_line_breaks_in_docx


def split_long_paragraph(p, max_len):
    # 优先在句号、问号、感叹号处断句
    separators = ["。", "！", "？", ".", "!", "?", "」", "”"]
    # 其次在逗号、分号处断句
    secondary_seps = ["，", "；", ",", ";"]

    if len(p) <= max_len:
        return [p]

    # 寻找最佳切分点
    chunks = []
    while len(p) > max_len:
        # 在最大长度范围内查找标点
        slice_text = p[:max_len]
        split_pos = -1

        # 优先使用主要分隔符
        for sep in separators:
            pos = slice_text.rfind(sep)
            if pos > split_pos:
                split_pos = pos + 1

        # 如果没找到主要分隔符，使用次要分隔符
        if split_pos == -1:
            for sep in secondary_seps:
                pos = slice_text.rfind(sep)
                if pos > split_pos:
                    split_pos = pos + 1

        # 如果实在找不到合适的分隔符，强制切分
        if split_pos <= 0:
            split_pos = max_len

        chunks.append(p[:split_pos].strip())
        p = p[split_pos:].strip()

    if p:
        chunks.append(p)

    return chunks


def preprocess_text(text, max_chars=500, min_chars=10):
    # 清理段落编号并分割文本
    number_pattern = re.compile(r"^\d+\s{2}", re.MULTILINE)
    cleaned_text = number_pattern.sub("", text)
    paragraphs = [p.strip() for p in cleaned_text.splitlines() if p.strip()]

    # 处理段落
    processed = []
    temp_para = ""

    for i, para in enumerate(paragraphs):
        # 处理过长段落
        if len(para) > max_chars:
            # 先处理累积的短段落
            if temp_para:
                processed.append(temp_para)
                temp_para = ""
            # 切分长段落
            processed.extend(split_long_paragraph(para, max_chars))
        # 处理短段落
        elif len(para) < min_chars and i < len(paragraphs) - 1:
            # 累积短段落
            temp_para = temp_para + para if not temp_para else temp_para + " " + para
            # 如果累积段落超过最大长度，添加到结果中
            if len(temp_para) > max_chars:
                processed.extend(split_long_paragraph(temp_para, max_chars))
                temp_para = ""
        else:
            # 处理普通段落
            if temp_para:
                # 将累积的短段落与当前段落合并
                para = temp_para + " " + para if temp_para else para
                temp_para = ""
            processed.append(para)

    # 处理最后可能剩余的短段落
    if temp_para:
        processed.append(temp_para)

    return processed, len(processed)


def count_characters(text):
    """计算文本的字符数(不包括空格和标点)"""
    return len(
        [char for char in text if char.strip() and not char in string.punctuation]
    )


def perview_paragraphs(mode, paragraphs, start_paragraph, translate_count):
    preview_text_start = paragraphs[start_paragraph][:20]
    preview_text_end = paragraphs[start_paragraph + translate_count - 1][-20:]
    total_chars = sum(
        count_characters(paragraphs[i])
        for i in range(start_paragraph, start_paragraph + translate_count)
    )

    print(f"翻译模式: {mode}")
    print(f"起始段落预览: {preview_text_start}...")
    print(f"结束段落预览:...{preview_text_end}")
    print(f"翻译字数：{total_chars}")
    print(f"预计成本：{total_chars * 0.38 / 1000:.2f}元")
    confirm = input("是否继续翻译？(y/n): ")
    if confirm.lower() != "y":
        print("*****已取消翻译*****")
        return

    return total_chars


def save_translations(result_text_docx, translated_paragraphs):
    os.makedirs(os.path.dirname(result_text_docx), exist_ok=True)
    if not os.path.exists(result_text_docx):
        doc = Document()
    else:
        doc = Document(result_text_docx)
    doc = set_document_style(doc, translated_paragraphs)
    doc.save(result_text_docx)
    replace_multiple_line_breaks_in_docx(result_text_docx)
