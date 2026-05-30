import base64
import hashlib
import os
import time
from ._browser import make_page, navigate


def translate_document(file_path, source_lang="auto", target_lang="es", mode="browser", headless=True, cookies=None, headers=None):
    if mode != "browser":
        return {"success": False, "error": "Document translation requires browser mode"}
    if not os.path.exists(file_path):
        return {"success": False, "error": "File not found"}

    ext = os.path.splitext(file_path)[1].lower()
    is_image = ext in ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp')

    with open(file_path, 'rb') as f:
        file_data = f.read()

    page = make_page(headless=headless)

    try:
        if is_image:
            return _translate_image_via_tab(page, file_path, file_data, source_lang, target_lang)
        else:
            return _translate_document_via_tab(page, file_path, file_data, source_lang, target_lang)

    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        page.quit()


def _translate_image_via_tab(page, file_path, file_data, source_lang, target_lang):
    original_hash = hashlib.md5(file_data).hexdigest()

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

    image_input.input(os.path.abspath(file_path))
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
            "document_data": translated_data,
            "success": True,
            "mime_type": "image/png",
            "size": len(translated_data),
            "original_size": len(file_data),
            "source_lang": source_lang,
            "target_lang": target_lang,
            "note": "Image translated via image tab"
        }

    return {
        "success": False,
        "error": "Could not retrieve translated image from page",
    }


def _translate_document_via_tab(page, file_path, file_data, source_lang, target_lang):
    navigate(page, 'https://translate.google.com/?sl=%s&tl=%s&op=docs' % (source_lang, target_lang))

    file_inputs = page.eles('css:input[type="file"]')
    if not file_inputs:
        return {"success": False, "error": "Could not find file upload input"}

    file_inputs[0].input(os.path.abspath(file_path))
    time.sleep(6)

    page.run_cdp('Page.setDownloadBehavior', behavior='allow', downloadPath=os.path.abspath('.'))

    for i in range(15):
        time.sleep(1)
        buttons = page.eles('tag:button')
        for b in buttons:
            if 'download' in (b.text or '').strip().lower():
                page.run_js("""
                    const buttons = document.querySelectorAll('button');
                    for (const b of buttons) {
                        if (b.textContent.trim().toLowerCase().includes('download')) {
                            b.click(); break;
                        }
                    }
                """)
                time.sleep(3)
                dl_files = [f for f in os.listdir('.') if not os.path.isdir(f) and
                            (f.startswith('downloads') or '.crdownload' not in f)]
                dl_files = [f for f in dl_files if not f.endswith('.crdownload') and
                            os.path.getctime(os.path.join('.', f)) > time.time() - 30]
                dl_files = [f for f in dl_files if f != os.path.basename(file_path)]
                if dl_files:
                    dl_files.sort(key=lambda f: os.path.getmtime(os.path.join('.', f)), reverse=True)
                    with open(dl_files[0], 'rb') as f:
                        doc_data = f.read()
                    try:
                        os.remove(dl_files[0])
                    except:
                        pass
                    return {
                        "success": True,
                        "document_data": doc_data,
                        "mime_type": "application/octet-stream",
                        "size": len(doc_data),
                        "source_lang": source_lang,
                        "target_lang": target_lang,
                        "note": "Document downloaded as translated file"
                    }

    translated_text = page.run_js("""
        const el = document.querySelector('[jsname="W297wb"]');
        if (el && el.textContent.trim()) return el.textContent.trim();
        const tas = document.querySelectorAll('textarea');
        for (const ta of tas) {
            if (ta.value.trim()) return ta.value.trim();
        }
        return '';
    """)

    if translated_text:
        return {
            "success": True,
            "document_text": translated_text,
            "mime_type": "text/plain",
            "size": len(translated_text.encode('utf-8')),
            "source_lang": source_lang,
            "target_lang": target_lang,
            "note": "Document translated as text"
        }

    return {
        "success": False,
        "error": "Could not extract translated document content",
        "note": "Try providing signed-in session cookies for PDF/DOCX files"
    }
