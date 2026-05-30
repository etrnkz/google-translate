from ._http import get_client


def translate_text_direct(text, source_lang="auto", target_lang="es"):
    client = get_client()

    src = "auto" if source_lang == "auto" else source_lang
    inner = [[text, src, target_lang, True], [None]]
    result = client.batchexecute("MkEWBc", inner)

    if not result:
        return {"error": "Empty response from translate API"}

    try:
        translated = result[1][0][0][5][0][0] or ""
        detected_lang = result[1][3] if source_lang == "auto" else source_lang

        return {
            "original": text,
            "translated": translated,
            "source_lang": detected_lang,
            "target_lang": target_lang,
            "source_transliteration": None,
            "target_transliteration": None,
            "suggestions": None,
        }

    except (IndexError, TypeError) as e:
        return {"error": "Failed to parse translate response: %s" % str(e)}
