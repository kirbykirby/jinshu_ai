def clean_md(md_file):
    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 删除前20行和最后2行
    lines = lines[20:-2]

    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue

        # 检查行首是否为数字或《
        if not (line[0].isdigit() or line[0] == "《"):
            continue

        cleaned_lines.append(line)

    with open(md_file, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))


if __name__ == "__main__":
    clean_md("original_text/110_Murong_Jun.md")
