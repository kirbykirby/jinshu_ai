def set_translator_prompt(
        document,
        document_type,
        original_language,
        target_language,
        subject,
        special_instructions="",
):
    return f"""
You are an expert {original_language}-to-{target_language} translator tasked with translating a section of a {document_type}, {document}, about {subject}. 
The original text will be provided within <TRANSLATE></TRANSLATE> tags.

Rules:
- Provide ONLY the FINAL TRANSLATION without additional texts,explanations, summaries, or breakdowns.{special_instructions}
"""


Jinshu_translator_prompt = """
- Convert dates to Western calendar in parentheses. Examples: the first year of Yongjia (307), the Yongjia period (307-313)
- Use (DATE) if year is uncertain.
- Maintain a tone appropriate for historical context and avoid modern colloquialisms.
- Preserve cultural context and historical authenticity.
- Note significant allusions with * and include brief context in footnotes.
"""


def wrap_prompt(prompt, tag="TRANSLATE"):
    return f"<{tag}>{prompt}</{tag}>"


def find_subject(md_file_path):
    """
    找出markdown文件中单独一行的《》标记作为主题，并标记各段落所属的主题范围
    输出主题和相应的分段序号
    """
    results = []
    current_subject = None
    current_line_nums = []

    with open(md_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 0):
        line = line.strip()

        if not line:
            continue

        if (
                line.startswith("《")
                and line.endswith("》")
                and len(line.strip("《》").split()) == 1
        ):
            if current_subject:
                results.append((current_subject[1:-1], current_line_nums))
            current_subject = line
            current_line_nums = [i]  # 包含主题行的行号
        else:
            if current_subject:
                current_line_nums.append(i)

    if current_subject:
        results.append((current_subject[1:-1], current_line_nums))

    return results


if __name__ == "__main__":
    results = find_subject("../1_SOURCE/045.md")
    print(results)
