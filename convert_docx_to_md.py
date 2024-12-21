from markitdown import MarkItDown


def convert_docx_to_md(docx_file, md_file):
    md = MarkItDown()
    result = md.convert(docx_file)
    with open(md_file, "w") as f:
        f.write(result.text_content)


if __name__ == "__main__":
    convert_docx_to_md("edited/123_Murong_Chui.docx", "md_files/123_Murong_Chui.md")
