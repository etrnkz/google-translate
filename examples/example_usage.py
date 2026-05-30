"""Example usage of the google_translate package."""

from google_translate import (
    translate_text,
    translate_image,
    translate_document,
    translate_website,
    translate_voice,
)


def example_text_browser():
    result = translate_text("Hello, how are you?", "en", "es")
    print("=== Text (Browser, Headless) ===")
    print(f"Original: {result['original']}")
    print(f"Translated: {result['translated']}")
    print(f"Source: {result['source_lang']} -> {result['target_lang']}")
    if result.get('suggestions'):
        print(f"Suggestions: {result['suggestions']}")
    print()


def example_text_browser_headed():
    result = translate_text("Hello", "en", "ru", headless=False)
    print("=== Text (Browser, Headed — shows window) ===")
    print(f"Translated: {result['translated']}")
    if result.get('target_transliteration'):
        print(f"Transliteration: {result['target_transliteration']}")
    print()


def example_text_direct():
    result = translate_text("Hello", "auto", "am", mode="direct")
    print("=== Text (Direct HTTP — no browser) ===")
    print(f"Translated: {result['translated']}")
    print(f"Auto-detected: {result['source_lang']}")
    print()


def example_image():
    result = translate_image("path/to/image.png", "auto", "es")
    if result.get('success'):
        with open("translated_image.png", "wb") as f:
            f.write(result['image_data'])
        print(f"Translated image saved ({result['translated_size']} bytes)")
    else:
        print(f"Error: {result.get('error')}")
    print()


def example_document():
    result = translate_document("path/to/document.pdf", "auto", "es")
    print("=== Document ===")
    print(result)
    print()


def example_website():
    result = translate_website("https://example.com", "auto", "es")
    if result.get('success'):
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"HTML: {len(result['html'])} chars")
    else:
        print(f"Error: {result.get('error')}")
    print()


def example_voice():
    result = translate_voice("hello", "en", "es")
    if result['audio_data']:
        with open("output.mp3", "wb") as f:
            f.write(result['audio_data'])
        print("Audio saved to output.mp3")
    else:
        print("Failed to generate audio")
    print()


if __name__ == "__main__":
    example_text_browser()
    # example_text_browser_headed()
    # example_text_direct()
    # example_image()
    # example_document()
    # example_website()
    # example_voice()
