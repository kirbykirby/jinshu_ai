def set_translator_prompt(
    document,
    document_type,
    original_language,
    target_language,
    subject,
    special_instructions="",
):
    return f"""You are an expert {original_language}-to-{target_language} translator. 
    Your goal is to translate part of a {document_type}, {document}, into English. 
    The original text will be delimited by <TRANSLATE></TRANSLATE> tags.
Subject of the text: {subject}

Rules:
- ONLY TRANSLATE and output the FINAL TRANSLATION
- DO NOT EXPLAIN ANYTHING, DO NOT SUMMARIZE ANYTHING, DO NOT BREAKDOWN ANYTHING
- Preserve accuracy
- Keep cultural context
- Use [?] for uncertain terms{special_instructions}
"""


def wrap_prompt(prompt, tag="TRANSLATE"):
    return f"<{tag}>{prompt}</{tag}>"
