"""Wispbyte keep-alive.

Wispbyte archives a server after 30 days of account inactivity. Any
authenticated page view counts as activity, so loading /client/servers on a
schedule is enough to keep it from being archived.

WISPBYTE_MODE picks how to authenticate:

  cookie  (default) replay a session captured from a real browser. Works.
  login             submit the login form with a stored password. Uses
                    camoufox (anti-detect Firefox) to pass Cloudflare
                    Turnstile automatically - no API key or extension
                    needed.

LOGIN_ACCOUNTS holds every account, one per line. A line may carry the
password, the cookie, or both, so the mode can be flipped without editing it:

    email:password|connect.sid=s%3A...     both
    email:password                          login mode only
    connect.sid=s%3A...                     cookie mode only

The cookie half is the raw Cookie request header from DevTools. Everything on
the line is masked before use and never reaches the log.

Session lifetime
----------------
connect.sid is a rolling express-session with a 15-day expiry: every request
re-issues the same session id with the clock reset, so running more often than
that keeps it alive indefinitely and the stored secret never goes stale. The
twice-weekly schedule survives three consecutive failures; weekly would
tolerate one.

Do not log out in the browser - Wispbyte destroys the session server-side and
the stored cookie dies with it. Close the tab instead. To keep several
accounts alive, capture each from a separate browser profile so they are all
signed in at the same time.

Output and log safety
---------------------
The workflow writes time.txt on the wispbyte-login branch: a UTC timestamp and
`login: success|failure`. This script exits non-zero if any account fails, so
the run goes red - a green run means the accounts really were touched.

Every value in LOGIN_ACCOUNTS is passed to ::add-mask:: before use, and
accounts appear in the log only as acct1/a1b2c3, a truncated hash, never an
address.
"""

import asyncio
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

from playwright.async_api import async_playwright

try:
    from camoufox.async_api import AsyncCamoufox
    HAS_CAMOUFOX = True
except ImportError:
    HAS_CAMOUFOX = False

SERVERS_URL = "https://wispbyte.com/client/servers"
AUTH_MARKER = 'a[href*="/client/dashboard"]'   # absent on the logged-out page
EMAIL_FIELD = "#email"
PASSWORD_FIELD = "#password"
SUBMIT_BUTTON = 'form button[type="submit"]'
TURNSTILE_FIELD = '[name="cf-turnstile-response"]'
PAGE_DUMP_CHARS = 1500

MODE = os.getenv("WISPBYTE_MODE", "cookie").strip().lower() or "cookie"

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")

# Cloudflare pins these to the IP and user-agent that earned them, so a runner
# replaying a desktop's copies just looks wrong. Drop them and let CF reissue.
IP_BOUND_COOKIES = {"cf_clearance", "__cf_bm", "__cflb"}


def mask(value):
    """Tell the Actions runner to redact `value` from every later log line."""
    value = (value or "").strip()
    if len(value) >= 3:
        print("::add-mask::" + value, flush=True)


def parse_cookie_header(header):
    """Turn a raw `Cookie:` header into Playwright cookie dicts."""
    cookies = []
    for pair in header.split(";"):
        pair = pair.strip()
        if not pair or "=" not in pair:
            continue
        name, value = (p.strip() for p in pair.split("=", 1))
        if not name or name in IP_BOUND_COOKIES:
            continue
        cookies.append({"name": name, "value": value,
                        "domain": ".wispbyte.com", "path": "/"})
    return cookies


def split_line(line):
    """One LOGIN_ACCOUNTS line -> (email, password, cookie_header).

    `creds|cookie`, or just one half. A lone line is read as a cookie when it
    looks like one, otherwise as `email:password` / `email,password`.
    """
    creds, pipe, cookie = (p.strip() for p in line.partition("|"))
    if not pipe:
        if "=" in creds and "@" not in creds.split("=", 1)[0]:
            creds, cookie = "", creds        # lone cookie header
        else:
            cookie = ""                       # lone credential pair

    email = password = ""
    if creds:
        sep = ":" if ":" in creds else ("," if "," in creds else None)
        if sep:
            email, password = (p.strip() for p in creds.split(sep, 1))
        else:
            email = creds                     # bare label, no password
    return email, password, cookie


def load_accounts():
    """-> list of dicts, in file order, with everything already masked."""
    raw = os.getenv("LOGIN_ACCOUNTS", "")
    mask(raw)

    accounts = []
    for line in (l.strip() for l in raw.splitlines()):
        if not line or line.startswith("#"):
            continue
        mask(line)

        email, password, cookie = split_line(line)
        for secret in (email, password, cookie):
            mask(secret)
        if email:
            mask(email.split("@", 1)[0])

        cookies = parse_cookie_header(cookie) if cookie else []
        for c in cookies:
            mask(c["value"])

        if not (cookies or (email and password)):
            continue
        seed = email or cookie
        accounts.append({
            "label": "acct%d/%s" % (len(accounts) + 1,
                                    hashlib.sha256(seed.encode()).hexdigest()[:6]),
            "email": email, "password": password, "cookies": cookies,
        })
    return accounts


async def open_browser(playwright):
    browser = await playwright.chromium.launch(headless=True, args=[
        "--no-sandbox", "--disable-setuid-sandbox",
        "--disable-dev-shm-usage", "--disable-gpu",
    ])
    context = await browser.new_context(viewport={"width": 1920, "height": 1080},
                                        user_agent=USER_AGENT)
    return browser, context


async def report_page(label, page, result):
    """Shared post-navigation check: authenticated, and what is on the page?"""
    authed = await page.query_selector(AUTH_MARKER) is not None
    at_login = await page.query_selector(PASSWORD_FIELD) is not None

    if authed and not at_login:
        result.update(success=True, detail="authenticated, activity registered")
        print("[%s] authenticated" % label, flush=True)
    elif at_login and not result["detail"]:
        result["detail"] = "not authenticated - login form served"

    body = re.sub(r"\n{2,}", "\n", (await page.inner_text("body"))[:PAGE_DUMP_CHARS]).strip()
    print("[%s] page ---\n%s\n--- end page" % (label, body), flush=True)

    if "IN STORAGE" in body or "Archived" in body:
        print("::warning::%s has an archived server - open its console and hit "
              "'Retrieve my files'" % label, flush=True)


async def touch_with_cookies(account):
    label = account["label"]
    result = {"label": label, "success": False, "detail": ""}
    async with async_playwright() as p:
        browser, context = await open_browser(p)
        await context.add_cookies(account["cookies"])
        page = await context.new_page()
        page.set_default_timeout(60000)
        try:
            print("[%s] loading dashboard with %d cookie(s)"
                  % (label, len(account["cookies"])), flush=True)
            await page.goto(SERVERS_URL, wait_until="load", timeout=60000)
            await page.wait_for_load_state("domcontentloaded", timeout=30000)
            await asyncio.sleep(6)
            await report_page(label, page, result)
            if not result["success"] and "login form" in result["detail"]:
                result["detail"] = "session expired - recapture the cookie"
                print("[%s] SESSION DEAD - recapture the cookie" % label, flush=True)
        except Exception as exc:
            result["detail"] = str(exc).splitlines()[0][:160]
            print("[%s] error: %s" % (label, result["detail"]), flush=True)
        await context.close()
        await browser.close()
    return result


async def touch_with_login(account):
    """Submit the real login form using camoufox to pass Turnstile.

    Camoufox is an anti-detect Firefox that passes Cloudflare Turnstile
    automatically. Falls back to plain Playwright if camoufox is not
    installed (will likely fail on Turnstile).

    Success is confirmed by the dashboard nav appearing. It deliberately does
    not test the URL: Wispbyte renders the login form in place at
    /client/servers without redirecting, so any URL check is true on the login
    page too and would report success while signed out.
    """
    label = account["label"]
    result = {"label": label, "success": False, "detail": "",
              "email": account["email"]}

    if HAS_CAMOUFOX:
        return await _login_camoufox(account, label, result)
    return await _login_playwright(account, label, result)


async def _login_camoufox(account, label, result):
    async with AsyncCamoufox(headless=True) as browser:
        page = await browser.new_page()
        page.set_default_timeout(60000)
        try:
            print("[%s] opening login form (camoufox)" % label, flush=True)
            await page.goto(SERVERS_URL, wait_until="load", timeout=60000)
            await page.wait_for_load_state("domcontentloaded", timeout=30000)
            await asyncio.sleep(5)

            if await page.query_selector(AUTH_MARKER) is not None:
                result.update(success=True, detail="already authenticated")
            else:
                await page.wait_for_selector(EMAIL_FIELD, timeout=20000)
                await page.fill(EMAIL_FIELD, account["email"])
                await page.fill(PASSWORD_FIELD, account["password"])

                token = ""
                for _ in range(90):
                    el = await page.query_selector(TURNSTILE_FIELD)
                    if el:
                        token = (await el.get_attribute("value")) or ""
                    if token:
                        break
                    await asyncio.sleep(1)
                print("[%s] turnstile token: %s"
                      % (label, "solved" if token else "NOT SOLVED"), flush=True)
                if not token:
                    result["detail"] = "Turnstile not solved after 90s"

                await asyncio.sleep(2)
                await page.evaluate(
                    "s => document.querySelector(s).click()", SUBMIT_BUTTON)
                try:
                    await page.wait_for_selector(AUTH_MARKER, timeout=45000)
                except Exception:
                    pass

            await report_page(label, page, result)

            if result["success"]:
                await _start_and_ping(label, page, result)
        except Exception as exc:
            result["detail"] = str(exc).splitlines()[0][:160]
            print("[%s] error: %s" % (label, result["detail"]), flush=True)
    return result


async def _start_and_ping(label, page, result):
    """Unlock captcha, start the server, and curl its health endpoint."""
    try:
        rewarded = await page.evaluate("""async () => {
            const r = await fetch('/client/api/server/start-captcha/rewarded',
                {method: 'POST', credentials: 'include',
                 headers: {'Content-Type': 'application/json'}, body: '{}'});
            return await r.json();
        }""")
        print("[%s] captcha unlock: %s"
              % (label, "ok" if rewarded.get("success") else rewarded), flush=True)

        status = await page.evaluate("""async () => {
            const r = await fetch('/client/api/servers/status', {credentials: 'include'});
            return await r.json();
        }""")
        servers = status.get("servers", [])
        if not servers:
            print("[%s] no servers found" % label, flush=True)
            return

        srv = servers[0]
        server_id = srv["identifier"]

        if srv["current_state"] not in ("running", "starting"):
            started = await page.evaluate("""async (sid) => {
                const r = await fetch('/client/api/server/start',
                    {method: 'POST', credentials: 'include',
                     headers: {'Content-Type': 'application/json'},
                     body: JSON.stringify({serverId: sid})});
                return await r.json();
            }""", server_id)
            print("[%s] server start: %s" % (label, started.get("message", started)),
                  flush=True)
        else:
            print("[%s] server already %s" % (label, srv["current_state"]), flush=True)

        result["server_id"] = server_id
    except Exception as exc:
        print("[%s] start/ping error: %s" % (label, str(exc)[:120]), flush=True)


async def _login_playwright(account, label, result):
    """Fallback when camoufox is not installed."""
    async with async_playwright() as p:
        browser, context = await open_browser(p)
        page = await context.new_page()
        page.set_default_timeout(60000)
        try:
            print("[%s] opening login form (playwright, no camoufox)" % label, flush=True)
            await page.goto(SERVERS_URL, wait_until="load", timeout=60000)
            await page.wait_for_load_state("domcontentloaded", timeout=30000)
            await asyncio.sleep(5)

            if await page.query_selector(AUTH_MARKER) is not None:
                result.update(success=True, detail="already authenticated")
            else:
                await page.wait_for_selector(EMAIL_FIELD, timeout=20000)
                await page.fill(EMAIL_FIELD, account["email"])
                await page.fill(PASSWORD_FIELD, account["password"])

                token = ""
                for _ in range(20):
                    token = await page.evaluate(
                        "s => (document.querySelector(s) || {}).value || ''", TURNSTILE_FIELD)
                    if token:
                        break
                    await asyncio.sleep(1)
                print("[%s] turnstile token: %s"
                      % (label, "issued" if token else "NOT ISSUED"), flush=True)
                if not token:
                    result["detail"] = ("Turnstile issued no token - install camoufox "
                                        "or use WISPBYTE_MODE=cookie")

                await page.click(SUBMIT_BUTTON)
                try:
                    await page.wait_for_selector(AUTH_MARKER, timeout=45000)
                except Exception:
                    pass

            await report_page(label, page, result)
        except Exception as exc:
            result["detail"] = str(exc).splitlines()[0][:160]
            print("[%s] error: %s" % (label, result["detail"]), flush=True)
        await context.close()
        await browser.close()
    return result


async def main():
    if MODE not in ("cookie", "login"):
        print("error: WISPBYTE_MODE must be 'cookie' or 'login', got %r" % MODE, flush=True)
        return 1

    accounts = load_accounts()
    if not accounts:
        print("error: LOGIN_ACCOUNTS is empty or malformed. Expected one account per "
              "line as 'email:password', 'connect.sid=...', or both joined by '|'.",
              flush=True)
        return 1

    need = "cookies" if MODE == "cookie" else "password"
    usable = [a for a in accounts if a[need]]
    for a in accounts:
        if not a[need]:
            print("::warning::%s has no %s for mode=%s - skipped"
                  % (a["label"], need, MODE), flush=True)
    if not usable:
        print("error: no account in LOGIN_ACCOUNTS has a %s for mode=%s" % (need, MODE),
              flush=True)
        return 1

    if MODE == "login" and not HAS_CAMOUFOX:
        print("::warning::WISPBYTE_MODE=login without camoufox - Turnstile will "
              "likely block the login; install camoufox[geoip] or use cookie mode.",
              flush=True)

    start = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print("start %s UTC, mode=%s, %d account(s): %s" % (
        start, MODE, len(usable), ", ".join(a["label"] for a in usable)), flush=True)

    runner = touch_with_cookies if MODE == "cookie" else touch_with_login
    results = await asyncio.gather(*(runner(a) for a in usable))
    end = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    failed = [r for r in results if not r["success"]]
    print("\nWispbyte keep-alive report (mode=%s)\n%s -> %s UTC\n%d ok | %d failed" % (
        MODE, start, end, len(results) - len(failed), len(failed)), flush=True)
    for r in results:
        print("  %s %s  %s" % ("OK  " if r["success"] else "FAIL", r["label"], r["detail"]),
              flush=True)

    if MODE == "login":
        await _ping_servers(results, usable)

    return 1 if failed else 0


SERVER_ADDRESSES = {
    "6942dd38": "78.154.103.21:11812",
    "df7cac21": "78.154.103.29:11445",
}


async def _ping_servers(results, accounts):
    """Wait for servers to boot, then ping via /exec."""
    pings = []
    for r in results:
        sid = r.get("server_id", "")
        addr = SERVER_ADDRESSES.get(sid, "")
        if not addr:
            continue
        acct = next((a for a in accounts if a["email"] == r.get("email", "")), None)
        if not acct:
            continue
        token = hashlib.sha256(
            ("%s:%s" % (acct["email"], acct["password"])).encode()).hexdigest()
        pings.append((r["label"], addr, token))

    if not pings:
        return

    print("\nWaiting 45s for servers to boot...", flush=True)
    await asyncio.sleep(45)

    print("\nServer ping (/exec):", flush=True)
    for label, addr, token in pings:
        url = "http://%s/exec" % addr
        try:
            data = json.dumps({"cmd": "echo ok"}).encode()
            req = urllib.request.Request(url, data=data, method="POST",
                                         headers={"Content-Type": "application/json",
                                                  "Authorization": "Bearer " + token})
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = json.loads(resp.read())
                ok = body.get("exit") == 0 and "ok" in body.get("stdout", "")
                print("  %s %s (%s) -> %s"
                      % ("ALIVE" if ok else "WARN ", label, addr,
                         body.get("stdout", "").strip()[:60]),
                      flush=True)
        except Exception as exc:
            print("  DOWN  %s (%s) -> %s"
                  % (label, addr, str(exc).splitlines()[0][:100]), flush=True)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
