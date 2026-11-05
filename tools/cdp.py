"""Minimal Chrome DevTools Protocol helper (stdlib only), shared by the QA scripts in tools/.

Committed copy of .impeccable/tools/cdp.py (plan AD16). Launches a throwaway headless Chrome on a
free port with its own temp profile (prefix "gromush-qa-") and returns a websocket session.
Scripts terminate it in a finally block; if headless Chromes ever pile up, clean them with:
pkill -f 'remote-debugging-port.*gromush-qa-'
Env: CHROME (path to the Chrome binary), FONT_SIZE (real default font size, 32 = 200 % text).
"""
import base64, json, os, re, socket, struct, subprocess, tempfile, time, urllib.request

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


class WS:
    def __init__(self, url):
        host_port, path = url[len("ws://"):].split("/", 1)
        host, port = host_port.split(":")
        self.s = socket.create_connection((host, int(port)), timeout=90)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (f"GET /{path} HTTP/1.1\r\nHost: {host_port}\r\nUpgrade: websocket\r\n"
               f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
        self.s.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        self.id = 0

    def send(self, method, params=None):
        self.id += 1
        msg = json.dumps({"id": self.id, "method": method, "params": params or {}}).encode()
        hdr = bytearray([0x81])
        n = len(msg)
        if n < 126:
            hdr.append(0x80 | n)
        elif n < 65536:
            hdr.append(0x80 | 126); hdr += struct.pack(">H", n)
        else:
            hdr.append(0x80 | 127); hdr += struct.pack(">Q", n)
        mask = os.urandom(4)
        hdr += mask
        self.s.sendall(bytes(hdr) + bytes(b ^ mask[i % 4] for i, b in enumerate(msg)))
        want = self.id
        while True:
            m = self.recv()
            if m.get("id") == want:
                return m.get("result", m)

    def _exact(self, n):
        b = b""
        while len(b) < n:
            chunk = self.s.recv(n - len(b))
            if not chunk:
                raise ConnectionError
            b += chunk
        return b

    def recv(self):
        data = b""
        while True:
            h = self._exact(2)
            fin, op, n = h[0] & 0x80, h[0] & 0x0F, h[1] & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._exact(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._exact(8))[0]
            data += self._exact(n)
            if fin:
                return json.loads(data.decode())


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def launch(reduced_motion=False, extra_args=()):
    """Start headless Chrome; returns (process, websocket) on the first page tab."""
    port = free_port()
    profile = tempfile.mkdtemp(prefix='gromush-qa-')
    if os.environ.get("FONT_SIZE"):
        # The real browser setting (chrome://settings/fonts) in the throwaway profile. Page.setFontSizes
        # below alone is not enough: Page.captureScreenshot with captureBeyondViewport (experimental)
        # re-applies the profile's preferences and renders at 16 px again (seen on Chrome, 2026-11).
        n = int(os.environ["FONT_SIZE"])
        os.makedirs(os.path.join(profile, "Default"), exist_ok=True)
        with open(os.path.join(profile, "Default", "Preferences"), "w") as f:
            json.dump({"webkit": {"webprefs": {"default_font_size": n, "default_fixed_font_size": n}}}, f)
    args = [CHROME, *extra_args, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--remote-debugging-port={port}", f"--user-data-dir={profile}", "about:blank"]
    if reduced_motion:
        args.insert(3, "--force-prefers-reduced-motion")
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(75):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
            tab = next(t for t in tabs if t["type"] == "page")
            break
        except Exception:
            time.sleep(0.2)
    else:
        proc.terminate(); raise RuntimeError("Chrome did not start")
    ws = WS(tab["webSocketDebuggerUrl"])
    ws.send("Page.enable")
    ws.send("Page.bringToFront")  # keeps rAF running in headless
    ws.send("Emulation.setFocusEmulationEnabled", {"enabled": True})
    if os.environ.get("FONT_SIZE"):  # real browser default font size, e.g. 32 for 200% text
        n = int(os.environ["FONT_SIZE"])
        ws.send("Page.setFontSizes", {"fontSizes": {"standard": n, "fixed": n}})
    return proc, ws


def viewport(ws, width, height=900):
    ws.send("Emulation.setDeviceMetricsOverride",
            {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": width < 600})


def to_url(target):
    """Accept a file path or an http(s) URL."""
    return target if re.match(r"^https?://", target) else "file://" + os.path.abspath(target)


def evaluate(ws, expr):
    r = ws.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return r.get("result", {}).get("value", r.get("exceptionDetails", {}).get("text"))


WAIT_LOAD = """new Promise(r=>{const done=()=>document.fonts.ready.then(()=>setTimeout(r,250));
document.readyState==='complete'?done():addEventListener('load',done,{once:true})})"""


def navigate(ws, target, settle=0.0):
    """Navigate and wait for the load event and web fonts (then `settle` extra seconds)."""
    ws.send("Page.navigate", {"url": to_url(target)})
    time.sleep(0.3)
    evaluate(ws, WAIT_LOAD)
    if settle:
        time.sleep(settle)


def stop(proc):
    """Terminate Chrome and wait for it, so no headless instance is left behind."""
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
