import json
import re
import requests
import urllib.parse


class HttpClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.bl = None

    def _handle_consent(self):
        r = self.session.get('https://translate.google.com', allow_redirects=True)
        if 'consent' not in r.url:
            return self._extract_bl(r.text)

        forms_raw = []
        start_idx = 0
        while True:
            form_start = r.text.find('<form', start_idx)
            if form_start == -1:
                break
            form_end = r.text.find('</form>', form_start)
            if form_end == -1:
                break
            forms_raw.append(r.text[form_start:form_end + 7])
            start_idx = form_end + 7

        if not forms_raw:
            return self._extract_bl(r.text)

        action_match = re.search(r'action="([^"]*)"', forms_raw[0])
        if not action_match:
            return self._extract_bl(r.text)

        inputs = re.findall(
            r'<input[^>]*name="([^"]*)"[^>]*value="([^"]*)"[^>]*>',
            forms_raw[0]
        )
        form_data = {n: v for n, v in inputs}
        self.session.post(action_match.group(1), data=form_data)

        r2 = self.session.get('https://translate.google.com')
        return self._extract_bl(r2.text)

    def _extract_bl(self, html):
        m = re.search(r'boq_translate-webserver_[^"\']*', html)
        self.bl = m.group(0) if m else 'boq_translate-webserver_20260527.06_p1'
        return self.bl

    def ensure_ready(self):
        if not self.bl:
            self._handle_consent()
        return self.bl is not None

    def batchexecute(self, rpcid, payload):
        self.ensure_ready()

        body = json.dumps([[[rpcid, json.dumps(payload), None, "generic"]]])

        params = {
            'rpcids': rpcid,
            'source-path': '/',
            'bl': self.bl,
            'hl': 'en-US',
            'soc-app': '1',
            'soc-platform': '1',
            'soc-device': '1',
            'rt': 'c',
        }

        resp = self.session.post(
            'https://translate.google.com/_/TranslateWebserverUi/data/batchexecute',
            params=params,
            headers={'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'},
            data={'f.req': body}
        )

        return self._parse_response(resp.text)

    def _parse_response(self, raw):
        if not raw.startswith(")]}'"):
            return None

        lines = raw.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('[['):
                try:
                    outer = json.loads(line)
                    if len(outer) > 0 and len(outer[0]) > 2:
                        return json.loads(outer[0][2])
                except (json.JSONDecodeError, IndexError):
                    continue
        return None


_default_client = None


def get_client():
    global _default_client
    if _default_client is None:
        _default_client = HttpClient()
    return _default_client
