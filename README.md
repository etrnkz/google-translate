## Google Translate API Package

A Python package for interacting with Google Translate services. Supports text (with transliteration), image, document, website, and voice translation.

Three modes available:
- **Browser (headless)** — default, full features, no visible window
- **Browser (headed)** — full features with visible Chrome window (enables transliteration)
- **Direct HTTP** — text-only, no browser required, fastest

### Features

- **Text Translation**: Translate text with auto-detect, transliteration, and suggestions
- **Image Translation**: Extract and translate text from images
- **Document Translation**: Translate images and documents
- **Website Translation**: Translate entire web pages via Google proxy
- **Text to Speech**: Convert text into audio (direct HTTP, no browser)

### Installation

```bash
pip install -r requirements.txt
```

Requires **Chrome/Chromium** installed for browser mode. Direct mode needs only `requests`.

### Usage

#### Text Translation

```python
from google_translate import translate_text

# Browser mode (headless) — full features
result = translate_text("Hello", "en", "es")
print(result['translated'])  # "Hola"

# Browser mode (headed) — shows window, enables transliteration
result = translate_text("Привет", "ru", "en", headless=False)
print(result['translated'])  # "Hello"
print(result['target_transliteration'])  # "Privet"

# Direct HTTP mode — no browser needed
result = translate_text("Hello", "auto", "am", mode="direct")
print(result['translated'])  # Amharic translation
print(result['source_lang'])  # "en" (auto-detected)
```

#### Image Translation

```python
from google_translate import translate_image

result = translate_image("image.png", "auto", "es")
if result.get('success'):
    with open("translated.png", "wb") as f:
        f.write(result['image_data'])
```

#### Document Translation

```python
from google_translate import translate_document

# Images are routed through the image tab
result = translate_document("photo.png", "auto", "es")

# PDF/DOCX files use the docs tab + CDP download
result = translate_document("document.pdf", "auto", "es")
```

#### Website Translation

```python
from google_translate import translate_website

result = translate_website("https://example.com", "auto", "es")
print(result['title'])  # Translated page title
print(result['html'][:500])  # Translated HTML
```

#### Voice Translation

```python
from google_translate import translate_voice

result = translate_voice("hello", "en", "es")
with open("output.mp3", "wb") as f:
    f.write(result['audio_data'])
```

### API Reference

#### `translate_text(text, source_lang="auto", target_lang="es", mode="browser", headless=True)`

**Parameters:**
- `text` (str): Text to translate
- `source_lang` (str): Source language code or "auto"
- `target_lang` (str): Target language code
- `mode` (str): `"browser"` (default) or `"direct"` (no browser)
- `headless` (bool): Run Chrome hidden (default `True`). Only applies in browser mode.

**Returns:** dict with `original`, `translated`, `source_lang`, `target_lang`, `source_transliteration`, `target_transliteration`, `suggestions`

#### `translate_image(image_path, source_lang="auto", target_lang="es", mode="browser", headless=True)`

**Parameters:**
- `image_path` (str): Path to image file
- `source_lang`, `target_lang`, `mode`, `headless`: Same as above

**Returns:** dict with `image_data` (bytes), `success`, `translated_size`, `original_size`

#### `translate_document(file_path, source_lang="auto", target_lang="es", mode="browser", headless=True)`

**Parameters:**
- `file_path` (str): Path to document or image file

**Returns:** dict with translation result

#### `translate_website(url, source_lang="auto", target_lang="es", mode="browser", headless=True)`

**Parameters:**
- `url` (str): URL of the website to translate

**Returns:** dict with `title`, `url`, `html`, `success`

#### `translate_voice(text, source_lang="en", target_lang="am")`

Direct HTTP, no browser needed.

**Returns:** dict with `audio_data` (bytes)

### Requirements

- Python 3.6+
- requests
- DrissionPage>=4.0.0 (for browser mode)
- Chrome/Chromium installed (for browser mode)

### Notes

- Browser mode uses DrissionPage (CDP protocol), not Selenium
- Direct mode uses Google Translate's internal `batchexecute` RPC endpoint
- Rate limiting may apply
- For production, consider the official Google Cloud Translation API
- Zombie Chrome processes can accumulate — run `taskkill /f /im chrome.exe` to clean up
