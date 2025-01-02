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


EXTRACT_FILTER_VALUES_PROMPT = """
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

COMPOSE_RESPONSE_PROMPT = """
Your task is to compose a comprehensive response to the user's query based on the provided information about available pets.
The response must be written in the language specified by the language code "{lang}" and should be clear, relevant, and helpful.

User Query:
{message}

Available Pets (JSON format):
{pets}

Response Format:
1. General Answer: Provide a concise, helpful general response addressing the user's query.
2. Individual Pet Answers: For each pet, create a specific answer tailored to the query, following this format:
   {{
     "pet_id": "<The ID of the pet>",
     "image": "<URL of the pet's image>",
     "url": "<URL of the pet's profile>",
     "answer": "<Your specific answer about the pet>"
   }}

Final Output Format (as a JSON object):
{{
  "general_answer": "<Your general answer here>",
  "individual_pet_answers": [
    {{
      "pet_id": "<The ID of the pet>",
      "image": "<URL of the pet's image>",
      "url": "<URL of the pet's profile>",
      "answer": "<Your specific answer about the pet>"
    }}
    // Repeat for each pet
  ]
}}

Instructions:
- Ensure the general answer addresses the user's query broadly while being informative and concise.
- Tailor each individual pet answer to the specific details of the pet and the context of the user's query.
- Format the entire response strictly as a JSON object.

Compose your response in {lang}.
"""
