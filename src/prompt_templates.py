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


EXTRACT_FILTER_VALUES = """
Your task is to identify and extract filter values from the user's message and return them in a JSON format.

### Filters to Extract:
- **type**: Specifies the type of pet.
  - Possible values: "hund" (dog), "katze" (cat).

### User Message:
<message>
{message}
</message>

### Expected Output Format:
Return the extracted filter values as a JSON object. If a filter value is not mentioned in the message, set its value to `null`.

Example Output:
{{
    "type": "katze"
}}
"""
