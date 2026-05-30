import base64
import hashlib
import os
import time
from ._browser import make_page, navigate


def translate_image(image_path, source_lang="auto", target_lang="es", mode="browser", headless=True, cookies=None, headers=None):
    if mode != "browser":
        return {"success": False, "error": "Image translation requires browser mode"}
    if not os.path.exists(image_path):
        return {"success": False, "error": "File not found"}

    with open(image_path, 'rb') as f:
        image_data = f.read()

    original_hash = hashlib.md5(image_data).hexdigest()

    page = make_page(headless=headless)

    try:
        navigate(page, 'https://translate.google.com')

        images_btn = page.ele('css:[aria-label="Image translation"]')
        if not images_btn:
            return {"success": False, "error": "Could not find Images button"}
        images_btn.click()
        time.sleep(1)

        file_inputs = page.eles('css:input[type="file"]')
        image_input = None
        for inp in file_inputs:
            accept = inp.attr('accept') or ''
            if 'image' in accept:
                image_input = inp
                break
        if not image_input:
            image_input = file_inputs[-1] if len(file_inputs) > 1 else file_inputs[0]

        abs_path = os.path.abspath(image_path)
        image_input.input(abs_path)
        time.sleep(6)

        result = page.run_js("""
            const imgs = document.querySelectorAll('img');
            for (let i = 0; i < imgs.length; i++) {
                const img = imgs[i];
                if (img.src && img.src.startsWith('blob:') && img.naturalWidth > 0 && img.naturalHeight > 0) {
                    try {
                        const canvas = document.createElement('canvas');
                        canvas.width = img.naturalWidth;
                        canvas.height = img.naturalHeight;
                        canvas.getContext('2d').drawImage(img, 0, 0);
                        return canvas.toDataURL('image/png');
                    } catch(e) {}
                }
            }
            return null;
        """)

        if result and result.startswith('data:image/png;base64,'):
            b64 = result[len('data:image/png;base64,'):]
            translated_data = base64.b64decode(b64)
            translated_hash = hashlib.md5(translated_data).hexdigest()

            return {
                "image_data": translated_data,
                "success": True,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "original_size": len(image_data),
                "translated_size": len(translated_data),
                "original_hash": original_hash,
                "translated_hash": translated_hash,
                "note": "Image identical to original (no text detected or already in target language)" if translated_hash == original_hash else None
            }

        return {
            "success": False,
            "error": "Could not retrieve translated image from page",
            "source_lang": source_lang,
            "target_lang": target_lang
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "source_lang": source_lang,
            "target_lang": target_lang
        }

    finally:
        page.quit()
