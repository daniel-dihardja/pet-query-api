DETECT_LANGUAGE_PROMPT = """
Your task is to detect the language of the following user message and return only the ISO 639-1 language code (e.g., "en" for English, "de" for German, "es" for Spanish).

<message>
{message}
</message>

Output strictly the two-letter language code with no additional text, quotes, or formatting.
"""


TRANSLATE_USER_QUERY_PROMPT = """
Your task is to accurately translate the following message from {lang} to German (de).

<message>
{message}
</message>

Provide only the translated text without any additional comments or formatting.
"""
