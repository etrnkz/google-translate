import time
import json
from ._browser import make_page, navigate
from .text_direct import translate_text_direct


def translate_text(text, source_lang="auto", target_lang="es", mode="browser", headless=True, cookies=None, headers=None):
    if mode == "direct":
        return translate_text_direct(text, source_lang, target_lang)

    page = make_page(headless=headless)
    try:
        navigate(page, 'https://translate.google.com/?sl=%s&tl=%s&op=translate' % (source_lang, target_lang))

        textarea = page.ele('css:textarea')
        if not textarea:
            return {"error": "Could not find input textarea"}

        textarea.click()
        time.sleep(0.3)
        textarea.input(text)
        time.sleep(4)

        raw = page.run_js("""
            const allEls = document.querySelectorAll('[jsname]');
            const data = {};
            for (const el of allEls) {
                const jsname = el.getAttribute('jsname');
                const t = el.textContent.trim();
                if (t && t.length > 0 && t.length < 500) {
                    if (!data[jsname]) data[jsname] = [];
                    if (data[jsname].indexOf(t) === -1)
                        data[jsname].push(t);
                }
            }
            return JSON.stringify(data);
        """)

        parsed = json.loads(raw)

        translated = ''
        transliteration = ''
        suggestions = []

        if 'W297wb' in parsed and parsed['W297wb']:
            translated = parsed['W297wb'][0]

        if 'jTaUub' in parsed and parsed['jTaUub']:
            transliteration = parsed['jTaUub'][0]
        if not transliteration and 'toZopb' in parsed and parsed['toZopb']:
            transliteration = parsed['toZopb'][0]

        if 'lKng5e' in parsed and parsed['lKng5e']:
            for s in parsed['lKng5e']:
                if s != text and s != translated:
                    suggestions.append(s)

        detected_source = source_lang
        if source_lang == 'auto':
            if 'k0o5Tb' in parsed and parsed['k0o5Tb']:
                for k in parsed['k0o5Tb']:
                    if k != 'Detect language':
                        detected_source = k.replace(' - Detected', '')
                        break

        return {
            "original": text,
            "translated": translated,
            "source_lang": detected_source if source_lang == 'auto' else source_lang,
            "target_lang": target_lang,
            "source_transliteration": None,
            "target_transliteration": transliteration or None,
            "suggestions": suggestions or None
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        page.quit()
