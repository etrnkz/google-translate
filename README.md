## Google Translate API Package

A Python package for interacting with Google Translate services by reverse engineering the complex google rpc api requests, supports text, image, document, and voice translation.

#### Features

- **Text Translation**: Translate text between multiple languages
- **Image Translation**: Extract and translate text from images
- **Document Translation**: Translate entire documents (PDF, DOCX, etc.)
- **Text to Speech**: Convert text into audio

### Installation

```bash
pip install -r requirements.txt
```

### Usage

#### Text Translation

```python
from google_translate import translate_text

result = translate_text(
    text="Hello, how are you?",
    source_lang="en",
    target_lang="es"
)

print(result['translated'])  # "Hola, ¿cómo estás?"
```

#### Image Translation

```python
from google_translate import translate_image

result = translate_image(
    image_path="path/to/image.png",
    source_lang="auto",
    target_lang="es"
)

# Check if successful
if result.get('success') and result.get('image_data'):
    # Save the translated image
    with open("translated_image.png", "wb") as f:
        f.write(result['image_data'])
    print(f"Translated image saved! Size: {result['size']} bytes")
else:
    print(f"Error: {result.get('error', 'Unknown error')}")
```

#### Document Translation

```python
from google_translate import translate_document

result = translate_document(
    file_path="path/to/document.pdf",
    source_lang="auto",
    target_lang="am"
)

print(result)
```

#### Voice Translation

```python
from google_translate import translate_voice

result = translate_voice(
    text="hello there ",
    source_lang="en",
    target_lang="en"
)

# Save the audio file
with open("output.mp3", "wb") as f:
    f.write(result['audio_data'])
```

### API Reference

#### `translate_text(text, source_lang="auto", target_lang="am", cookies=None, headers=None)`

Translates text from one language to another.

**Parameters:**
- `text` (str): The text to translate
- `source_lang` (str): Source language code (default: "auto" for auto-detection)
- `target_lang` (str): Target language code (default: "am" for Amharic)
- `cookies` (dict, optional): Custom cookies for the request
- `headers` (dict, optional): Custom headers for the request

**Returns:**
- dict: Contains `original`, `translated`, `source_lang`, and `target_lang`

#### `translate_image(image_path, source_lang="auto", target_lang="es", cookies=None, headers=None)`

Image Translation

**Parameters:**
- `image_path` (str): Path to the image file
- `source_lang` (str): Source language code
- `target_lang` (str): Target language code
- `cookies` (dict, optional): Custom cookies for the request
- `headers` (dict, optional): Custom headers for the request

**Returns:**
- dict: Translation result

#### `translate_document(file_path, source_lang="auto", target_lang="am", cookies=None, headers=None)`

Translates an entire document.

**Parameters:**
- `file_path` (str): Path to the document file
- `source_lang` (str): Source language code
- `target_lang` (str): Target language code
- `cookies` (dict, optional): Custom cookies for the request
- `headers` (dict, optional): Custom headers for the request

**Returns:**
- dict: Translation result

#### `translate_voice(text, source_lang="en", target_lang="am", cookies=None, headers=None)`

Generates  audio from text.

**Parameters:**
- `text` (str): Text to convert to speech
- `source_lang` (str): Source language code
- `target_lang` (str): Target language code
- `cookies` (dict, optional): Custom cookies for the request
- `headers` (dict, optional): Custom headers for the request

**Returns:**
- dict: Contains `audio_data` (bytes) and other metadata


### Requirements

- Python 3.6+
- requests

### Notes

- This package uses Google Translate's internal API endpoints(translate.google.com)
- Rate limiting may apply or google may update their api one day
- For production use, consider using the official Google Cloud Translation API


### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
