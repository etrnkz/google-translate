"""Voice translation module for Google Translate."""

import requests
import base64
import json
import urllib.parse


def translate_voice(text, source_lang="en", target_lang="am", cookies=None, headers=None):
    """
    Generate translated audio from text using Google Translate.
    
    Args:
        text (str): Text to convert to speech
        source_lang (str): Source language code (default: "en")
        target_lang (str): Target language code (default: "am")
        cookies (dict): Optional cookies for the request
        headers (dict): Optional headers for the request
        
    Returns:
        dict: Contains audio_data (bytes) and metadata
    """
    # Construct the Inner JSON structure
    inner_data = [
        text,
        source_lang,
        None,
        target_lang,
        [0]
    ]
    
    inner_json_string = json.dumps(inner_data)
    
    # Construct the Outer RPC structure
    outer_data = [
        [
            ["jQ1olc", inner_json_string, None, "generic"]
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
    
    params = {
        'rpcids': 'jQ1olc',
        'source-path': '/',
        'bl': 'boq_translate-webserver_20260225.06_p3',
        'hl': 'en-US',
        'soc-app': '1',
        'soc-platform': '1',
        'soc-device': '1',
        'rt': 'c',
    }
    
    # Make the request
    response = requests.post(
        'https://translate.google.com/_/TranslateWebserverUi/data/batchexecute',
        params=params,
        cookies=cookies,
        headers=headers,
        data=encoded_query
    )
    
    # Parse the response to extract audio
    audio_data = parse_voice_response(response.text)
    
    return {
        "audio_data": audio_data,
        "status_code": response.status_code,
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }


def parse_voice_response(raw_text):
    """Parse the Google Translate voice API response to extract audio data."""
    try:
        # Remove the anti-XSSI prefix and get the JSON line
        if raw_text.startswith(")]}'"):
            lines = raw_text.split("\n")
            # The JSON array is typically on line 3 (index 3)
            clean_json_str = lines[3] if len(lines) > 3 else lines[-1]
        else:
            clean_json_str = raw_text
        
        # Parse the outer JSON array
        outer_data = json.loads(clean_json_str)
        
        # Navigate to the inner JSON string
        # Structure: [["wrb.fr", "jQ1olc", "[\"base64_audio\"]", ...]]
        inner_json_str = outer_data[0][2]
        inner_data = json.loads(inner_json_str)
        
        # Extract base64 audio string (it's the first element)
        base64_audio = inner_data[0]
        
        # Fix padding if necessary
        missing_padding = len(base64_audio) % 4
        if missing_padding:
            base64_audio += '=' * (4 - missing_padding)
        
        # Decode base64 to audio bytes
        audio_bytes = base64.b64decode(base64_audio)
        
        return audio_bytes
    except (IndexError, KeyError, json.JSONDecodeError, TypeError) as e:
        print(f"Parse error: {e}")
        return None
