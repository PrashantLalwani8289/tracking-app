import json
import re


def extract_json_from_text(text):
    # Define regular expression pattern to extract JSON-like content
    pattern = r"{[^{}]+}"
    # Search for JSON-like content in the text
    match = re.search(pattern, text)

    if match:
        # Extract the JSON-like content
        json_text = match.group(0)
        # Load the JSON data
        json_data = json.loads(json_text)
        return json_data
    else:
        return None
