"""
Utility function to parse AI structured message responses into Python dictionaries.
"""

import json
from typing import Union


def parse_structured_msg(structured_msg: list) -> Union[dict, list[dict]]:
    """
    Parse a structured message from an AI response into a Python dictionary.
    
    Args:
        structured_msg: A list containing JSON string(s) from an AI response.
                       Example: ["{\n  \"law\": \"...\",\n  \"maintenance_period\": {...}\n}"]
    
    Returns:
        If the list contains a single item, returns the parsed dict.
        If the list contains multiple items, returns a list of parsed dicts.
        
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
            parsed_items.append(json.loads(item))
        elif isinstance(item, dict):
            # Already a dict, no parsing needed
            parsed_items.append(item)
        else:
            raise ValueError(f"Unexpected item type in list: {type(item).__name__}")
    
    # Return single dict if only one item, otherwise return list
    if len(parsed_items) == 1:
        return parsed_items[0]
    
    return parsed_items
