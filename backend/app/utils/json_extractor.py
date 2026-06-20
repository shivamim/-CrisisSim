"""
json_extractor.py — Robust JSON extraction from LLM responses
==============================================================
Handles markdown code blocks, nested objects, and partial JSON.
"""

import json
import re
from typing import Any, Dict


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """Extract a JSON object from text that may contain markdown, extra text, etc."""
    if not text:
        return {}

    # Try direct parse first
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        pass

    # Try to find JSON in code blocks
    code_block_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1).strip())
        except (json.JSONDecodeError, TypeError):
            pass

    # Try to find JSON object by tracking brace depth
    start = text.find('{')
    if start == -1:
        return {}

    depth = 0
    in_string = False
    escape_next = False

    for i in range(start, len(text)):
        char = text[i]

        if escape_next:
            escape_next = False
            continue

        if char == '\\' and in_string:
            escape_next = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i + 1])
                except (json.JSONDecodeError, TypeError):
                    # Try finding next '{'
                    next_start = text.find('{', i + 1)
                    if next_start == -1:
                        return {}
                    start = next_start
                    depth = 0
                    continue

    return {}
