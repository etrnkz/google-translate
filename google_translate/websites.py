import time
from urllib.parse import quote
from ._browser import make_page, navigate


def translate_website(url, source_lang="auto", target_lang="es", mode="browser", headless=True, cookies=None, headers=None):
    if mode != "browser":
        return {"success": False, "error": "Website translation requires browser mode"}
    page = make_page(headless=headless)

    try:
        translate_url = 'https://translate.google.com/translate?hl=en&sl=%s&tl=%s&u=%s&prev=search' % (
            source_lang, target_lang, quote(url, safe='')
        )
        navigate(page, translate_url)

        for _ in range(7):
            time.sleep(1)
            current_title = page.run_js("return document.title;")
            if current_title and 'translate' not in current_title.lower():
                time.sleep(2)
                break

        page_title = page.run_js("return document.title;") or page.title
        page_html = page.run_js("return document.documentElement.outerHTML;")
        page_url = page.run_js("return location.href;") or page.url

        if not page_html:
            time.sleep(3)
            page_html = page.run_js("return document.documentElement.outerHTML;")

        return {
            "success": True,
            "title": page_title,
            "url": page_url,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "html": page_html or ""
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        page.quit()
