#!/usr/bin/env python3
import html
import json
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WEEKS = ROOT / "weeks"
ERRORS = []


def fail(message):
    ERRORS.append(message)


def words(value):
    return len(re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?", value or ""))


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path.relative_to(ROOT)}: invalid or missing JSON ({error})")
        return {}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.copy_targets = []
        self.refs = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if values.get("data-copy"):
            self.copy_targets.append(values["data-copy"].removeprefix("#"))
        for name in ("href", "src"):
            if values.get(name):
                self.refs.append(values[name])


required = {
    "index.html",
    "manual.html",
    "channel-setup.html",
    "calendar.html",
    "longs/index.html",
    "shorts/index.html",
    "seo/index.html",
    "music/index.html",
    "style.css",
    "scaler.js",
}
for week in range(1, 5):
    required.add(f"longs/week-{week:02}.html")
    required.add(f"seo/week-{week:02}.html")
    for short in range(1, 4):
        required.add(f"shorts/week-{week:02}/short-{short}.html")

files = {
    str(path.relative_to(DOCS)).replace("\\", "/")
    for path in DOCS.rglob("*")
    if path.is_file()
}
for name in sorted(required - files):
    fail(f"missing required output: docs/{name}")

for filename in sorted(name for name in files if name.endswith(".html")):
    text = (DOCS / filename).read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    if len(parser.ids) != len(set(parser.ids)):
        fail(f"docs/{filename}: duplicate HTML id")
    for target in parser.copy_targets:
        if target not in parser.ids:
            fail(f"docs/{filename}: copy target #{target} does not exist")
    if "<main" not in text or "<h1" not in text:
        fail(f"docs/{filename}: main heading structure is missing")
    if "viewport-fit=cover" not in text:
        fail(f"docs/{filename}: mobile viewport guard is missing")
    if "site-menu" in text:
        has_beginner_links = "manual.html" in text and "channel-setup.html" in text
        if not has_beginner_links and "scaler.js" not in text:
            fail(f"docs/{filename}: menu cannot reach the beginner pages")
    for ref in parser.refs:
        if ref.startswith(("https://", "#", "mailto:", "tel:", "data:")):
            continue
        if ref.startswith("http://"):
            fail(f"docs/{filename}: insecure external link {ref}")
            continue
        clean = ref.split("#", 1)[0].split("?", 1)[0]
        if not clean:
            continue
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(filename), clean))
        if clean.endswith("/"):
            resolved = posixpath.join(resolved, "index.html")
        if resolved not in files:
            fail(f"docs/{filename}: broken local reference {ref} -> {resolved}")

scaler = (DOCS / "scaler.js").read_text(encoding="utf-8") if (DOCS / "scaler.js").exists() else ""
for beginner_page in ("manual.html", "channel-setup.html"):
    if beginner_page not in scaler:
        fail(f"scaler.js: global menu is missing {beginner_page}")

home = (DOCS / "index.html").read_text(encoding="utf-8") if (DOCS / "index.html").exists() else ""
for required_link in ("manual.html", "channel-setup.html", "calendar.html", "longs/index.html", "shorts/index.html", "seo/index.html", "music/index.html"):
    if required_link not in home:
        fail(f"home: missing top-level link {required_link}")

manual = (DOCS / "manual.html").read_text(encoding="utf-8") if (DOCS / "manual.html").exists() else ""
for phrase in ("Is site se video kaise banani hai?", "Long video ka poora order", "Teen Shorts ka poora order", "Agar samajh na aaye"):
    if phrase not in manual:
        fail(f"manual: missing beginner instruction {phrase}")
for phrase in (
    "https://f5tts-prod.duckdns.org/web/",
    "https://tensor.art/",
    "bm_mix_adam_lewis",
    "Speed:</b> 0.8",
    "Juggernaut XL-Ragnarok",
    "DPM++ SDE Karras",
    "Sampling steps:</b> 25",
    "CFG scale:</b> 4",
    "1280 × 720",
    "EasyNegative chip select mat karo",
):
    if phrase not in manual:
        fail(f"manual: exact tool setting/link is missing: {phrase}")

all_html = "\n".join((DOCS / name).read_text(encoding="utf-8") for name in files if name.endswith(".html"))
if re.search(r"\bSaif\b", all_html, flags=re.IGNORECASE):
    fail("site pages: old reporter name Saif remains; use Anas")
for awkward_phrase in (
    "khool",
    "Har hara button dabao",
    "Guess mat karo",
    "Tumhari instruction copy hai",
):
    if awkward_phrase.lower() in all_html.lower():
        fail(f"site wording: awkward phrase remains: {awkward_phrase}")
if re.search(r"\bkhol\b", all_html, flags=re.IGNORECASE):
    fail("site wording: use the natural instruction 'kholo', not 'khol'")

for week in range(1, 5):
    folder = WEEKS / f"week-{week:02}"
    long_data = read_json(folder / "long.json")
    long_script = long_data.get("script", "")
    long_words = words(long_script)
    if not 900 <= long_words <= 1200:
        fail(f"week {week:02} long: expected 900-1200 words, got {long_words}")
    prompts = long_data.get("prompts", [])
    if len(prompts) != 40:
        fail(f"week {week:02} long: expected 40 image prompts, got {len(prompts)}")
    for index, prompt in enumerate(prompts, 1):
        value = prompt.get("prompt", "").lower()
        for guard in ("no text", "no watermark", "photorealistic"):
            if guard not in value:
                fail(f"week {week:02} long prompt {index}: missing {guard}")
    long_page_path = DOCS / "longs" / f"week-{week:02}.html"
    long_page = long_page_path.read_text(encoding="utf-8") if long_page_path.exists() else ""
    if long_data.get("title", "") not in html.unescape(long_page):
        fail(f"week {week:02} long: JSON title is missing from page")
    if len(re.findall(r'id="p\d{2}"', long_page)) != 40:
        fail(f"week {week:02} long page: expected 40 prompt boxes")
    if long_script and long_script not in html.unescape(long_page):
        fail(f"week {week:02} long: page script does not match JSON")

    short_titles = []
    for short in range(1, 4):
        short_data = read_json(folder / f"short-{short}.json")
        short_script = short_data.get("script", "")
        short_words = words(short_script)
        if not 100 <= short_words <= 170:
            fail(f"week {week:02} short {short}: expected 100-170 words, got {short_words}")
        if len(short_data.get("image_refs", [])) != 8:
            fail(f"week {week:02} short {short}: expected 8 image references")
        timings = short_data.get("timings", [])
        if len(timings) != 8:
            fail(f"week {week:02} short {short}: expected 8 timing cues")
        if any(float(item.get("t", -1)) < 0 for item in timings):
            fail(f"week {week:02} short {short}: invalid timing cue")
        if any(float(a.get("t", 0)) >= float(b.get("t", 0)) for a, b in zip(timings, timings[1:])):
            fail(f"week {week:02} short {short}: timing cues are not increasing")
        short_page_path = DOCS / "shorts" / f"week-{week:02}" / f"short-{short}.html"
        short_page = short_page_path.read_text(encoding="utf-8") if short_page_path.exists() else ""
        if short_data.get("title", "") not in html.unescape(short_page):
            fail(f"week {week:02} short {short}: JSON title is missing from page")
        if short_script and short_script not in html.unescape(short_page):
            fail(f"week {week:02} short {short}: page script does not match JSON")
        if len(re.findall(r"data-t=", short_page)) != 16:
            fail(f"week {week:02} short {short}: page should show each of 8 timings twice")
        short_titles.append(short_data.get("title", ""))

    seo = read_json(folder / "seo.json")
    if len(seo.get("youtube_shorts", [])) != 3:
        fail(f"week {week:02} SEO: expected 3 YouTube Shorts packs")
    if len(seo.get("tiktok", [])) != 3:
        fail(f"week {week:02} SEO: expected 3 TikTok packs")
    if len(seo.get("sources", [])) < 7:
        fail(f"week {week:02} SEO: official source list is incomplete")
    youtube = seo.get("youtube", {})
    for field in ("title", "description", "keywords", "tags", "hashtags", "thumbnail", "upload"):
        if not youtube.get(field):
            fail(f"week {week:02} SEO: YouTube long pack missing {field}")
    for platform in ("youtube_shorts", "tiktok"):
        for index, pack in enumerate(seo.get(platform, []), 1):
            if pack.get("short") != index:
                fail(f"week {week:02} SEO {platform} pack {index}: short number mismatch")
            for field in ("title", "hashtags"):
                if not pack.get(field):
                    fail(f"week {week:02} SEO {platform} pack {index}: missing {field}")
    seo_page_path = DOCS / "seo" / f"week-{week:02}.html"
    seo_page = seo_page_path.read_text(encoding="utf-8") if seo_page_path.exists() else ""
    if seo_page.count('class="seo-card"') != 7:
        fail(f"week {week:02} SEO page: expected 1 long + 3 YouTube Shorts + 3 TikTok cards")
    for title in [youtube.get("title", ""), *short_titles]:
        if title and title not in html.unescape(seo_page):
            fail(f"week {week:02} SEO page: missing video title {title}")

music = read_json(WEEKS / "music.json")
if len(music.get("weeks", [])) != 4:
    fail("music: expected one music plan for each of four weeks")
for item in music.get("weeks", []):
    track = item.get("track", {})
    if not track.get("source_url", "").startswith("https://pixabay.com/music/"):
        fail(f"music week {item.get('week')}: exact Pixabay source page is missing")
    if not track.get("filename", "").endswith(".mp3"):
        fail(f"music week {item.get('week')}: MP3 filename is missing")

music_page = (DOCS / "music" / "index.html").read_text(encoding="utf-8") if (DOCS / "music" / "index.html").exists() else ""
if music_page.count('class="music-card"') != 4:
    fail("music page: expected four week cards")

css = (DOCS / "style.css").read_text(encoding="utf-8") if (DOCS / "style.css").exists() else ""
for guard in ("min-width: 320px", "prefers-reduced-motion", "#ff7665", "--dim: #56616d"):
    if guard not in css:
        fail(f"style.css: responsive/accessibility guard missing: {guard}")

if ERRORS:
    print(f"VALIDATION FAILED ({len(ERRORS)} issues)")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("VALIDATION PASSED: 4 longs, 12 shorts, 4 SEO packs, music, beginner pages, copy targets and local links")
