"""Example usage of the google_translate package."""

from google_translate import translate_text, translate_image, translate_document, translate_voice


def example_text_translation():
    """Example of text translation."""
    print("=== Text Translation Example ===")
    
    result = translate_text(
        text="Hello, how are you?",
        source_lang="en",
        target_lang="es"
    )
    
    if "error" not in result:
        print(f"Original: {result['original']}")
        print(f"Translated: {result['translated']}")
        print(f"From {result['source_lang']} to {result['target_lang']}")
    else:
        print(f"Error: {result['error']}")
    print()


def example_image_translation():
    """Example of image translation."""
    print("=== Image Translation Example ===")
    
    # Note: You need to provide an actual image path
    image_path = "path/to/your/image.png"
    
    result = translate_image(
        image_path=image_path,
        source_lang="auto",
        target_lang="es"
    )
    
    if "error" not in result:
        print(f"Status Code: {result['status_code']}")
        print("Translation successful!")
    else:
        print(f"Error: {result['error']}")
    print()


def example_document_translation():
    """Example of document translation."""
    print("=== Document Translation Example ===")
    
    # Note: You need to provide an actual document path
    doc_path = "path/to/your/document.pdf"
    
    result = translate_document(
        file_path=doc_path,
        source_lang="auto",
        target_lang="am"
    )
    
    if "error" not in result:
        print(f"Status Code: {result['status_code']}")
        print("Translation successful!")
    else:
        print(f"Error: {result['error']}")
    print()


def example_voice_translation():
    """Example of voice translation."""
    print("=== Voice Translation Example ===")
    
    result = translate_voice(
        text="I love you more than anything",
        source_lang="en",
        target_lang="am"
    )
    
    if result['audio_data']:
        # Save the audio file
        output_file = "output_audio.mp3"
        with open(output_file, "wb") as f:
            f.write(result['audio_data'])
        print(f"Audio saved to {output_file}")
        print(f"Text: {result['text']}")
        print(f"From {result['source_lang']} to {result['target_lang']}")
    else:
        print("Failed to generate audio")
    print()


if __name__ == "__main__":
    # Run examples
    example_text_translation()
    # example_image_translation()  # Uncomment and provide image path
    # example_document_translation()  # Uncomment and provide document path
    # example_voice_translation()  # Uncomment to generate audio
