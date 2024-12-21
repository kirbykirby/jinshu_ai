from markitdown import MarkItDown


def convert_docx_to_md(docx_file, md_file):
    md = MarkItDown()
    result = md.convert(docx_file)
    with open(md_file, "w") as f:
        f.write(result.text_content)
