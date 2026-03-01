"""Image translation module for Google Translate."""

import requests
import base64
import json
import urllib.parse


def translate_image(image_path, source_lang="auto", target_lang="am", cookies=None, headers=None):
    """
    Translate text in an image using Google Translate.
    
    Note: Image translation requires valid session cookies from Google Translate.
    The cookies may expire quickly, so this function may not work reliably
    without fresh cookies from an active browser session.
    
    Args:
        image_path (str): Path to the image file
        source_lang (str): Source language code (default: "auto")
        target_lang (str): Target language code (default: "am")
        cookies (dict): Optional cookies for the request
        headers (dict): Optional headers for the request
        
    Returns:
        dict: Contains image_data (bytes) and metadata
    """
    # Read and encode the image
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    # Construct the Inner JSON structure
    inner_data = [
        [base64_image, "image/png"],
        source_lang,
        target_lang
    ]
    
    inner_json_string = json.dumps(inner_data)
    
    # Construct the Outer RPC structure
    outer_data = [
        [
            ["WqWDPb", inner_json_string, None, "generic"]
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
        'rpcids': 'WqWDPb',
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
    
    # Parse the response to extract translated image
    image_data = parse_image_response(response.text)
    
    return {
        "image_data": image_data,
        "status_code": response.status_code,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "original_size": len(image_bytes)
    }


def parse_image_response(raw_text):
    """Parse the Google Translate image API response to extract translated image data."""
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
        # Structure: [["wrb.fr", "WqWDPb", "[[\"base64_image\", \"mime_type\"]]", ...]]
        inner_json_str = outer_data[0][2]
        inner_data = json.loads(inner_json_str)
        
        # Extract base64 image string
        # Structure: [[base64_string, mime_type], ...]
        base64_image = inner_data[0][0]
        
        # Decode base64 to image bytes
        image_bytes = base64.b64decode(base64_image)
        
        return image_bytes
    except (IndexError, KeyError, json.JSONDecodeError, TypeError) as e:
        print(f"Parse error: {e}")
        return None
