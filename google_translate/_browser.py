import random
import time
from DrissionPage import ChromiumPage, ChromiumOptions


def make_page(headless=True):
    co = ChromiumOptions()
    co.set_local_port(random.randint(20000, 60000))
    if headless:
        co.headless()
    co.set_argument('--no-sandbox')
    co.set_argument('--disable-gpu')
    return ChromiumPage(addr_or_opts=co)


def navigate(page, url):
    page.get(url)
    time.sleep(2)
    for attempt in range(3):
        if 'consent' not in page.url:
            return
        time.sleep(1)
        page.run_js("""
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.textContent.trim().toLowerCase().includes('reject')) {
                    btn.click();
                    return 'clicked';
                }
            }
            return 'not found';
        """)
        time.sleep(2)
