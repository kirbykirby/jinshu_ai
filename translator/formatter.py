from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


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


def reformat_docx(file_path, output_path=None, first_line_indent=0.74):
    doc = Document(file_path)

    # 如果没有指定输出路径，则覆盖原文件
    if output_path is None:
        output_path = file_path

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
                # 添加段落属性
                pPr = OxmlElement('w:pPr')

                # 添加缩进设置
                ind = OxmlElement('w:ind')
                ind.set(qn('w:firstLine'), str(int(first_line_indent * 567)))

                # 添加段落间距和行距设置
                spacing = OxmlElement('w:spacing')
                spacing.set(qn('w:after'), '100')  # 段后5磅（5pt = 100 twentieths of a point）
                spacing.set(qn('w:line'), '240')  # 单倍行距（240 = 12pt）
                spacing.set(qn('w:lineRule'), 'auto')  # 设置行距规则为自动

                pPr.append(ind)
                pPr.append(spacing)
                new_p.append(pPr)

                # 在当前换行符位置插入新段落
                current_br.getparent().insert(
                    current_br.getparent().index(current_br), new_p
                )
                # 移除连续的两个换行符
                current_br.getparent().remove(current_br)
                next_br.getparent().remove(next_br)

        # 为现有段落添加缩进和间距设置
        if not paragraph.style.name.startswith('Heading'):  # 不对标题应用设置
            pPr = p.get_or_add_pPr()
            ind = pPr.get_or_add_ind()
            ind.set(qn('w:firstLine'), str(int(first_line_indent * 567)))

            # 添加段落间距和行距设置
            spacing = pPr.get_or_add_spacing()
            spacing.set(qn('w:after'), '100')  # 段后5磅
            spacing.set(qn('w:line'), '240')  # 单倍行距
            spacing.set(qn('w:lineRule'), 'auto')  # 行距规则为自动

    doc.save(output_path)
