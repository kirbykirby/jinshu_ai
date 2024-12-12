import os
import re
import string
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


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


def create_paragraph_style():
    style = {
        "first_line_indent": Cm(0.74),
        "line_spacing": 1,
        "alignment": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "font_size": Pt(10.5),
        "font_name_ascii": "Cambria",  # 西文字体
        "font_name_east_asia": "等线",  # 中文字体
    }
    return style


def set_document_style(doc, translated_paragraphs):
    # 设置页面边距
    for section in doc.sections:
        for margin in ["left_margin", "right_margin"]:
            setattr(section, margin, Cm(3.18))
        for margin in ["top_margin", "bottom_margin"]:
            setattr(section, margin, Cm(2.54))

    style = create_paragraph_style()

    for text in translated_paragraphs:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = style["line_spacing"]
        p.paragraph_format.first_line_indent = style["first_line_indent"]
        p.alignment = style["alignment"]

        run = p.add_run(text)
        run.font.size = style["font_size"]

        # 分别设置中英文字体
        run.font.name = style["font_name_ascii"]  # 西文字体
        run._element.rPr.rFonts.set(
            qn("w:ascii"), style["font_name_ascii"]
        )  # ASCII字符
        run._element.rPr.rFonts.set(
            qn("w:hAnsi"), style["font_name_ascii"]
        )  # 高位ASCII字符
        run._element.rPr.rFonts.set(
            qn("w:eastAsia"), style["font_name_east_asia"]
        )  # 中文字符

        # 禁用中文断行时的字符间距调整
        p.paragraph_format.word_wrap = True
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)

    return doc


def post_process_paragraphs(paragraphs):
    """对翻译后的段落进行后处理，添加0.74cm首行缩进"""
    processed = []
    indent = "\u3000\u3000"  # 使用两个全角空格约等于0.74cm

    for p in paragraphs:
        # 如果段落开头没有缩进，添加缩进
        if not p.startswith(indent):
            p = indent + p
        processed.append(p)

    return processed


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
    print(f"结束段落预览: {preview_text_end}...")
    print(f"翻译字数：{total_chars}")
    print(f"预计成本：{total_chars * 0.36 / 1000:.2f}元")
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


def replace_multiple_line_breaks_in_docx(file_path, output_path=None):
    # 打开文档
    doc = Document(file_path)

    # 如果没有指定输出路径，则覆盖原文件
    if output_path is None:
        output_path = file_path

    # 遍历所有段落
    for paragraph in doc.paragraphs:
        # 获取段落的XML元素
        p = paragraph._element
        # 查找所有的手动换行符（line break）
        br_elements = p.findall(
            ".//w:br",
            {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"},
        )

        # 如果找到连续的换行符，替换为段落分隔符
        for i in range(len(br_elements) - 1):
            current_br = br_elements[i]
            next_br = br_elements[i + 1]
            # 检查两个br元素是否相邻
            if current_br.getnext() == next_br:
                # 创建新段落元素
                new_p = OxmlElement("w:p")
                # 在当前换行符位置插入新段落
                current_br.getparent().insert(
                    current_br.getparent().index(current_br), new_p
                )
                # 移除连续的两个换行符
                current_br.getparent().remove(current_br)
                next_br.getparent().remove(next_br)

    # 保存文档
    doc.save(output_path)
