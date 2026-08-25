# CODEX BRIEF — The Ledger Content Machine

Read this whole file before touching the repo. Everything you need is here.

---

## 1. MISSION

Build a static GitHub Pages site that turns a weekly Excel row into a printable "work sheet" for Dua (mobile-only, no English, no editing skill). One long video + three shorts per week. You generate all scripts and prompts yourself, embed them in per-week HTML pages, and deploy. Dua only copies, pastes, and drags things at timestamps you calculate for her.

---

## 2. LANGUAGE — HARD RULE

**Every word you write for the user or on any page is in Roman Urdu.** Every button label, every heading, every instruction, every commit message, every reply to Saif.

**These four things stay in English, always:**
- Video script content
- Image prompts
- Voice server input
- Excel column names

Never translate an image prompt into Urdu. Never translate the script into Urdu. Never write Urdu inside a script.

---

## 3. REPO STRUCTURE — BUILD EXACTLY THIS

```
/
├── data/
│   └── plan.xlsx                    ← Saif maintains. Don't rewrite.
├── weeks/
│   └── week-01/
│       ├── long.json                ← you write
│       ├── short-1.json
│       ├── short-2.json
│       └── short-3.json
├── docs/                            ← GitHub Pages serves from here
│   ├── index.html                   ← home, 3 big buttons
│   ├── calendar.html                ← full 8-week table
│   ├── style.css                    ← shared, one file
│   ├── scaler.js                    ← shared voice-upload logic
│   ├── longs/
│   │   ├── index.html               ← cards for week-01, week-02...
│   │   └── week-01.html
│   └── shorts/
│       ├── index.html
│       └── week-01/
│           ├── short-1.html
│           ├── short-2.html
│           └── short-3.html
├── scripts/
│   └── render.mjs                   ← optional Node helper, not required
├── .github/workflows/
│   └── deploy.yml
├── CODEX_BRIEF.md                   ← this file
└── README.md                        ← Roman Urdu, for Saif
```

`docs/` is the deploy source. Everything Dua sees is inside it. `weeks/*.json` is your working memory — read it back when regenerating or fixing a week.

---

## 4. DATA SOURCE — plan.xlsx

Tab: `Content Calendar`, row 5 = week 1, row 12 = week 8.

You read four columns per week: `E` (Long Title), `C` (Sub-Type), `D` (Structure Variant), `G` (Opening Line). Also `H`, `I`, `J` for the three short titles.

Use `xlsx` npm package or read the file directly. If you can't parse it, tell Saif in Roman Urdu and ask him to paste the row values.

---

## 5. WORKFLOW — when Saif says "week N banao"

Do this in order, without asking:

1. Read row N from `plan.xlsx`. Extract the 7 fields above.
2. Generate `long.json`: script (English), 40 image prompts (English), predicted duration, per-image timings.
3. Generate `short-1.json`, `short-2.json`, `short-3.json`: each with script, 8 image references (image numbers 1–40 to reuse from the long), timings.
4. Render `docs/longs/week-0N.html` from the long template in section 13.
5. Render `docs/shorts/week-0N/short-{1,2,3}.html` from the short template.
6. Update `docs/longs/index.html` and `docs/shorts/index.html` to include the new week card.
7. Git add, commit with message `Week N tayyar`, push.
8. Reply to Saif in Roman Urdu: which files were written, deploy status, anything that needs his eyes.

**Never** generate all 8 weeks at once. One week per instruction.

---

## 6. SCRIPT GENERATION — RULES YOU FOLLOW

You are writing for "The Ledger". A middle-aged American narrator, quiet and unhurried, reading from a case file. Text is fed to a TTS engine and played over still photographs with slow zoom. Nothing on screen moves. The sentences carry everything.

**Every story is a COMPOSITE.** Built from patterns that recur in this kind of fraud. Never a specific real event. No real names of people, banks, or companies.

**Voice rules — not suggestions:**

1. Vary sentence length deliberately. Long that builds, short that lands. Never three long in a row, never three short.
2. Concrete over abstract. Not "a significant sum" but "forty one thousand dollars in the first year alone".
3. Trust silence. End a passage on a plain fact and stop. No summary line. No "and that is how..." No telling the viewer how to feel.
4. **Banned words, absolute:** shocking, unbelievable, devastating, heartbreaking, chilling, little did they know, what happened next, the truth is, in a world where, just like that.
5. No rhetorical questions anywhere. Not one.
6. Use first names plainly and repeatedly. Never "the victim".
7. Exact figures, exact dates, exact durations. Round numbers feel invented.
8. No financial advice, ever. Narrator observes patterns. Never tells the viewer what to do.

**TTS formatting — critical:**

- Every number, currency, date in words. "eighty four thousand dollars", "nineteen seventy eight", "six forty in the morning". No digits, no `$`, no `%`.
- No dashes of any kind. Full stop or comma only.
- No brackets, asterisks, headings, bullets, markdown.
- No abbreviations. Spell out.
- Paragraphs of two to four sentences with a blank line between them.
- No ellipses.

**Long script shape:** 950–1100 words. Runs 6:30–7:30 at 145 wpm.

Internally six movements. Never labelled on the page:

- One (~130 words): a cold, specific moment with no context. Use the OPENING LINE from Excel as first sentence or open on it.
- Two (~180 words): the world and people before anything went wrong. Make the central person likeable. Viewer must trust him.
- Three (~200 words): how he came to be near the money. Every step looked reasonable.
- Four (~180 words): the first thing that did not add up, and why nobody followed it.
- Five (~200 words): discovery and collapse. Full figures here.
- Six (~160 words): how the scheme worked mechanically. Three signals that were missed, stated as observations not warnings. This section contains at least one insight not stated anywhere else. Ends on one flat sentence with no lesson.

The STRUCTURE VARIANT column tells you how to enter and order the story. Follow it exactly. It overrides default order but all six movements still present.

---

## 7. IMAGE PROMPT GENERATION — RULES

You produce **exactly 40** prompts per long, numbered `01` to `40`, in the order they appear on screen.

**Every prompt is:** a place, an object, or a wide human figure whose face is not readable. Never a close portrait. Never a recognisable real person. Never text, signs, logos, or numbers visible in the frame.

**Every prompt contains, in this order:** subject, setting, period markers, time of day, quality of light, lens and film character, colour grade.

**Vary shot scale.** Across every group of three: one wide, one medium, one close detail.

**Hold one look across all forty.** Decide the grade in prompt 01 and don't drift. Warm, muted, film-photographic.

**Suffix — append to every single prompt, exactly:**

```
35mm film photography, shallow depth of field, natural light, muted desaturated color grade, fine grain, no text, no watermark, photorealistic
```

**One negative prompt** for the whole set. Saved once per week in the JSON.

For **short** image references, don't generate new prompts. Pick 8 image numbers from the long's 40 that fit the excerpt. Store as `[4, 7, 12, 18, 23, 29, 34, 38]` in `short-N.json`.

---

## 8. TIMING MATH

Narrator speed: **145 words per minute** = 2.417 words per second.

For the long: after writing the script, split it into 40 roughly equal word-chunks. For each chunk, compute:

```
start_time_seconds = words_before_this_chunk / 2.417
```

Store as `[{ image: 1, t: 0.0, line: "On a Tuesday morning..." }, ...]` in `long.json`. `line` is the first ten words of the chunk in English, for reference and waveform snapping.

For shorts: same logic, 8 chunks over ~50 seconds.

**These are predictions.** The page rescales them at runtime when Dua uploads her voice file. Section 13 has the code.

---

## 9. SHORT SCRIPTS

3 shorts per long. Each 130–160 words, 45–55 seconds at 145 wpm.

- **Short 1** — the cold open moment. Mystery-driven. Ends on its own beat.
- **Short 2** — the mechanism reveal from movement six. Educational. Viewer walks away having learned one thing.
- **Short 3** — a single character detail from movement two or four. Human, quiet, specific.

Same voice rules, same TTS formatting, same banned words. First sentence must be a concrete situation, not a tease. Last sentence one flat fact, no CTA. Never "watch the full video", never "keep watching".

Image references reused from the long's 40 (see section 7).

---

## 10. DESIGN SYSTEM

One `style.css`. No frameworks. Mobile-first, breakpoint at 640px.

**Tokens:**

```css
:root {
  --ink: #0F1419;
  --paper: #F2EDE1;
  --paper-2: #E5DECC;
  --green: #3F6B46;
  --stamp: #A8362B;
  --dim: #8A93A0;
  --rule: #2A3441;
  --pad: 18px;
}
```

**Fonts** (Google Fonts):
- Display serif: `IBM Plex Serif` (700)
- Body: `IBM Plex Sans` (400, 500, 600, 700)
- Mono: `IBM Plex Mono` (400, 500, 600)

**Layout:** max-width 660px, centered. `padding: 0 var(--pad)`.

**Buttons:** full width on mobile, 46px min height, 3px border-radius, no gradients, no shadows except one dark card shadow.

**Cards:** cream `--paper` background on dark `--ink` body. Repeating faint horizontal rules inside body (ruled-paper feel). Red `--stamp` for numbered corner, green `--green` for action.

**Type scale:** h1 clamp(30px, 8.5vw, 44px), h2 20px, body 15.5px with 1.6 line-height, mono 11.5px.

**Rules:**
- No emoji ever.
- No decorative dividers. If you need separation, use `border-top: 1px solid var(--rule)`.
- No animation on load. Respect `prefers-reduced-motion`.
- Every interactive element has a visible `:focus` outline (2px solid `--green`, offset 1px).

Keep it disciplined. Dua's problem is confusion, not aesthetic starvation.

---

## 11. HOME PAGE — docs/index.html

Three big tap targets and nothing else. Full mobile viewport.

```html
<!DOCTYPE html>
<html lang="ur-Latn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>The Ledger — Kaam</title>
  <link rel="stylesheet" href="style.css">
</head>
<body class="home">
  <header>
    <span class="brand">The Ledger</span>
  </header>
  <main>
    <h1>Aaj kya karna hai?</h1>
    <nav class="tiles">
      <a href="calendar.html"><span class="num">01</span><span class="lbl">Weekly Calendar</span></a>
      <a href="longs/index.html"><span class="num">02</span><span class="lbl">Long Videos</span></a>
      <a href="shorts/index.html"><span class="num">03</span><span class="lbl">Short Videos</span></a>
    </nav>
  </main>
</body>
</html>
```

Three tiles fill the screen vertically on mobile. No footer. No explanation.

---

## 12. CALENDAR PAGE

Read plan.xlsx and render a simple table: week number, publish date, long title, short titles. No workflow here — this is reference. Add a small "khool" (open) link in each row that goes to the long page.

Keep it under 200 lines of HTML. If someone wants detail, they tap through.

---

## 13. LONG VIDEO PAGE — full template

This is the important one. Dua spends most of her time here.

The page has **four sections** in order:

1. **Script** — copy button, F5-TTS link
2. **Awaaz upload** — file input that rescales all timings and draws waveform
3. **40 image prompts** — each with copy button, its own timestamp shown
4. **CapCut steps** — numbered list of "playhead 0:47 par → Image 05 lagao"

**Timestamps everywhere are wrapped in `<span data-t="47.3">0:47</span>`.** The scaler.js reads `data-t` (predicted seconds), updates the visible text, and stores scaled seconds in `data-scaled`.

**Template — `docs/longs/week-0N.html`. Placeholders in `{{ }}`:**

```html
<!DOCTYPE html>
<html lang="ur-Latn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Week {{N}} — Long</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body class="work">

<header class="bar">
  <a href="../index.html" class="back">‹ Ghar</a>
  <span class="brand">Week {{N}} — Long</span>
</header>

<main>

<h1>{{TITLE}}</h1>
<p class="lede">Neeche se shuru karo. Har hara button dabao aur agli step par jao.</p>

<!-- ============ 1. SCRIPT ============ -->
<section class="step">
  <div class="head"><span class="num">01</span><h2>Script copy karo</h2></div>
  <pre class="script" id="script">{{SCRIPT_ENGLISH}}</pre>
  <button class="copy" data-copy="#script">Script copy karo</button>
  <a class="link" href="https://f5tts-prod.duckdns.org/web/" target="_blank" rel="noopener">
    F5-TTS kholo aur script paste karo
  </a>
  <p class="tip">Awaaz ban jaye to download karo. Naam rakho <b>voice</b>.</p>
</section>

<!-- ============ 2. VOICE UPLOAD ============ -->
<section class="step">
  <div class="head"><span class="num">02</span><h2>Awaaz yahan upload karo</h2></div>
  <label class="drop" for="voice">
    <span class="drop-cta">Awaaz file chuno</span>
    <span class="drop-sub">Jab upload hogi, saare waqt khud sahi ho jayenge</span>
    <input type="file" id="voice" accept="audio/*">
  </label>
  <div class="status" id="status" hidden>
    <p>Awaaz ki asli lambai: <b><span id="actual">—</span></b></p>
    <p>Waqt update ho gaye. Ab neeche ki taraf jao.</p>
    <canvas id="waveform" width="600" height="80"></canvas>
  </div>
</section>

<!-- ============ 3. IMAGE PROMPTS ============ -->
<section class="step">
  <div class="head"><span class="num">03</span><h2>Chalees images banao</h2></div>
  <a class="link" href="https://tensor.art/" target="_blank" rel="noopener">
    Tensor.art kholo, size <b>16:9</b> karo
  </a>
  <p class="tip">Har prompt copy karo, Tensor.art par paste karo, image download karo. Naam rakho <b>01</b>, phir <b>02</b>, aakhir tak <b>40</b>.</p>

  <ol class="prompts">
    {{#IMAGES}}
    <li>
      <div class="row">
        <span class="pnum">Image {{NN}}</span>
        <span class="pt" data-t="{{T}}">{{T_HUMAN}}</span>
      </div>
      <pre class="prompt" id="p{{NN}}">{{PROMPT}}</pre>
      <button class="copy small" data-copy="#p{{NN}}">Copy karo</button>
    </li>
    {{/IMAGES}}
  </ol>

  <details class="neg">
    <summary>Negative prompt (har image ke saath paste karo)</summary>
    <pre id="neg">{{NEGATIVE}}</pre>
    <button class="copy small" data-copy="#neg">Negative copy karo</button>
  </details>
</section>

<!-- ============ 4. CAPCUT ============ -->
<section class="step">
  <div class="head"><span class="num">04</span><h2>CapCut mein jodo</h2></div>
  <ol class="capcut">
    <li>CapCut kholo. Naya project. Aspect ratio <b>16:9</b>.</li>
    <li>Neeche <b>Audio</b> par jao. Apni <b>voice</b> file lagao, zero se shuru.</li>
    <li>Neeche timing chart hai. Har row par likha hai: kis waqt par kaunsi image lagegi.</li>
    <li>Playhead (red line) ko diye hue waqt par le jao. Us jagah <b>+</b> se image add karo. Number wahi ho jo row mein likha hai.</li>
    <li>Har image par Animation → Combo → koi dheema zoom lagao.</li>
    <li>Export 1080p, 30fps.</li>
  </ol>

  <table class="timing">
    <thead>
      <tr><th>#</th><th>Playhead yahan</th><th>Image lagao</th></tr>
    </thead>
    <tbody>
      {{#IMAGES}}
      <tr>
        <td>{{NN}}</td>
        <td><span data-t="{{T}}">{{T_HUMAN}}</span></td>
        <td><b>Image {{NN}}</b></td>
      </tr>
      {{/IMAGES}}
    </tbody>
  </table>
</section>

</main>

<script src="../scaler.js"></script>
</body>
</html>
```

**File — `docs/scaler.js`** (write exactly this):

```js
(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  // Copy buttons
  $$('[data-copy]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const target = $(btn.getAttribute('data-copy'));
      const text = target ? target.textContent.trim() : '';
      if (!text) return;
      try {
        await navigator.clipboard.writeText(text);
      } catch {
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        ta.remove();
      }
      const original = btn.textContent;
      btn.textContent = 'Copy ho gaya';
      btn.classList.add('done');
      setTimeout(() => { btn.textContent = original; btn.classList.remove('done'); }, 1400);
    });
  });

  // Voice upload → rescale timestamps + waveform
  const voice = $('#voice');
  if (!voice) return;

  voice.addEventListener('change', async e => {
    const file = e.target.files[0];
    if (!file) return;

    // Get actual duration
    const url = URL.createObjectURL(file);
    const audio = new Audio(url);
    await new Promise(res => audio.addEventListener('loadedmetadata', res, { once: true }));
    const actual = audio.duration;

    // Predicted = largest data-t on the page (last image start ≈ total duration)
    const allT = $$('[data-t]').map(el => parseFloat(el.dataset.t));
    const predicted = Math.max(...allT) + 8; // last image gets ~8 more seconds
    const ratio = actual / predicted;

    // Rescale every visible timestamp
    $$('[data-t]').forEach(el => {
      const original = parseFloat(el.dataset.t);
      const scaled = original * ratio;
      el.dataset.scaled = scaled;
      el.textContent = fmt(scaled);
      el.classList.add('scaled');
    });

    // Show status
    $('#actual').textContent = fmt(actual);
    $('#status').hidden = false;

    // Waveform
    await drawWaveform(file, actual);
  });

  function fmt(s) {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${m}:${String(sec).padStart(2, '0')}`;
  }

  async function drawWaveform(file, duration) {
    const canvas = $('#waveform');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;

    const ab = await file.arrayBuffer();
    const AC = window.AudioContext || window.webkitAudioContext;
    const actx = new AC();
    const buf = await actx.decodeAudioData(ab);
    const data = buf.getChannelData(0);
    const step = Math.floor(data.length / w);

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#3F6B46';
    for (let x = 0; x < w; x++) {
      let peak = 0;
      for (let i = 0; i < step; i++) {
        const v = Math.abs(data[x * step + i] || 0);
        if (v > peak) peak = v;
      }
      const bh = peak * h * 0.85;
      ctx.fillRect(x, (h - bh) / 2, 1, bh);
    }

    // Image boundary markers
    ctx.fillStyle = '#A8362B';
    $$('[data-t]').forEach(el => {
      const t = parseFloat(el.dataset.scaled || el.dataset.t);
      const x = (t / duration) * w;
      ctx.fillRect(x, 0, 1, h);
    });
  }
})();
```

**How this solves Dua's English problem:** she uploads voice → every `<span data-t>` becomes the real, scaled timestamp. The CapCut table then reads "Playhead `0:47` par → Image 05 lagao". She matches a number on the CapCut timeline to a number on the page. Zero listening. Zero English.

The waveform is a bonus. Red vertical lines show where each image should start. If she zooms in on the CapCut timeline she can see the same waveform peaks. Visual cross-check.

---

## 14. SHORT VIDEO PAGE

Same structure as long, three changes:

1. Aspect ratio is **9:16** everywhere (Tensor.art size instruction, CapCut instruction, and the section 3 header says "Aath vertical images").
2. Only 8 image slots.
3. Section 3 says: **"Long ke folder se in numbers wali images copy karo: 04, 07, 12, 18, 23, 29, 34, 38"** — the numbers come from `short-N.json`. Dua duplicates them in her gallery under a new folder for this short. Fresh generation only if a re-used image crops badly after CapCut vertical crop.

Everything else — copy buttons, voice upload, timing table, waveform — identical to long.

---

## 15. GITHUB PAGES DEPLOY

`.github/workflows/deploy.yml`:

```yaml
name: Deploy
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs
  deploy:
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

Repo Settings → Pages → Source: GitHub Actions. Nothing else needs configuring.

---

## 16. README.md — for Saif, Roman Urdu

```
# The Ledger

Har hafte ke liye:

1. `data/plan.xlsx` mein us hafte ki row check karo.
2. Codex ko likho: **"Week 3 banao"** (ya jo bhi number ho).
3. Codex script likhega, prompts banayega, HTML render karega, GitHub Actions deploy kar dega.
4. Dua ka link: `https://<username>.github.io/<repo>/`

Bas.
```

---

## 17. CHECKLIST — before you reply "ho gaya"

- [ ] Long script is 950–1100 words, no digits, no dashes, no banned words.
- [ ] Exactly 40 image prompts. Each ends with the standard suffix.
- [ ] Every `<span data-t>` has a numeric attribute in seconds.
- [ ] Voice upload input works on mobile Safari and Chrome (tested via viewport meta tag and `accept="audio/*"`).
- [ ] `docs/longs/index.html` and `docs/shorts/index.html` show the new week card.
- [ ] Every button label is Roman Urdu. Every heading is Roman Urdu. Every explanatory line is Roman Urdu.
- [ ] Script content and image prompts remain in English.
- [ ] No emoji. No decorative dividers. No bullet-heavy walls of text.
- [ ] Page passes: open in Chrome DevTools mobile 375px width, scroll through, tap every button. Nothing overflows. Every tap target ≥ 44px.
- [ ] Commit message in Roman Urdu: `Week N tayyar`.

If anything above fails, fix it before pushing.

---

## 18. WHEN THINGS GO WRONG

Saif might say things like "week 3 mein short 2 ka script chhota hai" or "image 12 galat aa rahi". You:

- Read `weeks/week-03/short-2.json` first. Don't guess.
- Fix that one artifact only. Regenerate that one file.
- Re-render only that page.
- Commit: `Week 3 short 2 theek kiya`.

Never rebuild the whole week for a small fix.

---

That is everything. Start with `docs/index.html`, `docs/style.css`, `docs/scaler.js`. Then generate week 1. Reply in Roman Urdu when done.