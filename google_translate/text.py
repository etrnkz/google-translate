"""Text translation module for Google Translate."""

import requests
import json
import urllib.parse


def translate_text(text, source_lang="auto", target_lang="am", cookies=None, headers=None):
    """
    Translate text using Google Translate API.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code (default: "auto")
        target_lang (str): Target language code (default: "am")
        cookies (dict): Optional cookies for the request
        headers (dict): Optional headers for the request
        
    Returns:
        dict: Translation result containing original and translated text
    """
    # Construct the Inner JSON structure
    inner_data = [
        [text, source_lang, target_lang, 1, None, 2],
        []
    ]
    
    inner_json_string = json.dumps(inner_data)
    
    # Construct the Outer RPC structure
    outer_data = [
        [
            ["MkEWBc", inner_json_string, None, "generic"]
        ]
    ]
    
    outer_json_string = json.dumps(outer_data)
    
    # Prepare the Form Data
    form_data = {'f.req': outer_json_string}
    encoded_query = urllib.parse.urlencode(form_data)
    
    # Default headers if not provided
    if headers is None:
        headers = {
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    # Make the request
    response = requests.post(
        'https://translate.google.com/_/TranslateWebserverUi/data/batchexecute',
        cookies=cookies,
        headers=headers,
        data=encoded_query
    )
    
    return parse_translate_response(response.text)


def parse_translate_response(raw_text):
    """Parse the Google Translate API response."""
    if raw_text.startswith(")]}'"):
        clean_json_str = raw_text.split("\n", 1)[1]
    else:
        clean_json_str = raw_text
    
    try:
        outer_data = json.loads(clean_json_str)
        inner_json_str = outer_data[0][2]
        inner_data = json.loads(inner_json_str)
        
        result_block = inner_data[1]
        original_text = result_block[4][0]
        target_lang = result_block[1]
        source_lang = result_block[3]
        translated_text = result_block[0][0][5][0][0]
        
        return {
            "original": original_text,
            "translated": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
    except (IndexError, KeyError, json.JSONDecodeError, TypeError) as e:
        return {"error": f"Error parsing response: {e}"}
