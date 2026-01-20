"""
Utility function to parse AI structured message responses into Python dictionaries.
"""

import json
import re
from typing import Union


def _extract_json_from_markdown(text: str) -> list[str]:
    """
    Extract JSON content from markdown code blocks if present.
    
    Args:
        text: A string that may contain JSON wrapped in markdown code blocks.
        
    Returns:
        A list of extracted JSON strings, or a list with the original text if no code blocks found.
    """
    # Pattern to match ```json ... ``` or ``` ... ``` code blocks
    pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    if matches:
        return [match.strip() for match in matches]
    
    return [text.strip()]


def parse_structured_msg(structured_msg: list) -> Union[dict, list[dict]]:
    """
    Parse a structured message from an AI response into a Python dictionary.
    
    Args:
        structured_msg: A list containing JSON string(s) from an AI response.
                       Supports both raw JSON and markdown-wrapped JSON.
                       Can handle multiple JSON blocks within a single string.
                       Example: ["{\n  \"law\": \"...\",\n  \"maintenance_period\": {...}\n}"]
                       Example: ["```json\n{\"key\": \"value\"}\n```"]
    
    Returns:
        If the result contains a single item, returns the parsed dict.
        If the result contains multiple items, returns a list of parsed dicts.
        
    Raises:
        ValueError: If the input is not a list or is empty.
        json.JSONDecodeError: If any string in the list is not valid JSON.
    
    Example:
        msg = ['{"law": "Some law", "maintenance_period": {"start_date": "2025-12-01"}}']
        result = parse_structured_msg(msg)
        print(result)
        {'law': 'Some law', 'maintenance_period': {'start_date': '2025-12-01'}}
    """
    if not isinstance(structured_msg, list):
        raise ValueError(f"Expected a list, got {type(structured_msg).__name__}")
    
    if not structured_msg:
        raise ValueError("structured_msg list is empty")
    
    parsed_items = []
    for item in structured_msg:
        if isinstance(item, str):
            # Extract JSON from markdown code blocks if present (may return multiple)
            json_strings = _extract_json_from_markdown(item)
            for json_str in json_strings:
                parsed_items.append(json.loads(json_str))
        elif isinstance(item, dict):
            # Already a dict, no parsing needed
            parsed_items.append(item)
        else:
            raise ValueError(f"Unexpected item type in list: {type(item).__name__}")
    
    # Return single dict if only one item, otherwise return list
    if len(parsed_items) == 1:
        return parsed_items[0]
    
    return parsed_items


if __name__ == "__main__":
    # Example usage
    example_msg = [
        """```json

{

  "filters": [

    {

      "type": "all",

      "conditions": [

        {

          "field": "cam1",

          "op": "eq",

          "value": 0

        },

        {

          "field": "cam2",

          "op": "eq",

          "value": 0

        }

      ]

    }

  ]

}

```"""
    ]
    
    result = parse_structured_msg(example_msg)
    print(result)
