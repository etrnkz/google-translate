"""Document translation module for Google Translate."""

import requests
import base64
import json
import mimetypes
import urllib.parse
import os


def translate_document(file_path, source_lang="auto", target_lang="am", cookies=None, headers=None):
    """
    Translate a document using Google Translate.
    
    Args:
        file_path (str): Path to the document file
        source_lang (str): Source language code (default: "auto")
        target_lang (str): Target language code (default: "am")
        cookies (dict): Optional cookies for the request
        headers (dict): Optional headers for the request
        
    Returns:
        dict: Translation result
    """
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    # Read the file and encode it in Base64
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    b64_content = base64.b64encode(file_content).decode('utf-8')
    
    # Determine MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    # Construct the Inner JSON structure
    inner_data = [
        [b64_content, mime_type],
        source_lang,
        target_lang
    ]
    
    inner_json_string = json.dumps(inner_data)
    
    # Construct the Outer RPC structure
    outer_data = [
        [
            ["LBEnTe", inner_json_string, None, "generic"]
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-goog-ext-387202953-jspb': '["/DataService.GetDocumentTranslation"]',
        }
    
    params = {
        'rpcids': 'LBEnTe',
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
    
    # Parse the response
    result = {"status_code": response.status_code, "raw_response": response.text}
    
    try:
        if response.status_code == 200 and response.text.startswith(")]}'"):
            lines = response.text.split("\n")
            for line in lines:
                if line.strip().startswith('['):
                    data = json.loads(line)
                    if len(data) > 0 and len(data[0]) > 2 and data[0][2]:
                        inner_json_str = data[0][2]
                        inner_data = json.loads(inner_json_str)
                        
                        # Similar structure to image translation
                        if inner_data and len(inner_data) > 0:
                            doc_data = inner_data[0]
                            if isinstance(doc_data, list) and len(doc_data) > 0:
                                base64_doc = doc_data[0]
                                mime_type = doc_data[1] if len(doc_data) > 1 else "text/plain"
                                
                                # Decode base64 document
                                doc_bytes = base64.b64decode(base64_doc)
                                result["success"] = True
                                result["document_data"] = doc_bytes
                                result["mime_type"] = mime_type
                                result["size"] = len(doc_bytes)
                                
                                # Try to decode as text
                                try:
                                    result["document_text"] = doc_bytes.decode('utf-8')
                                except:
                                    result["document_text"] = None
                                break
            
            # If no data was parsed, check for error codes
            if "success" not in result:
                result["success"] = False
                result["note"] = "Document translation may not be supported for this file type or requires additional parameters"
    except Exception as e:
        result["error"] = str(e)
    
    return result
