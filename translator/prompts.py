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
- Provide ONLY the FINAL TRANSLATION without explanations, summaries, or breakdowns.
- Ensure accuracy and preserve cultural context.
- Use [?] for uncertain terms.{special_instructions}
"""


def wrap_prompt(prompt, tag="TRANSLATE"):
    return f"<{tag}>{prompt}</{tag}>"
