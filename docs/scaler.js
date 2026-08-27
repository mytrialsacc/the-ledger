(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  // Keep the beginner pages available from every working page, including
  // older week files whose static menu predates the manual and channel setup.
  const menu = $('.site-menu nav');
  const script = document.currentScript;
  if (menu && script) {
    const root = new URL('.', script.src);
    let after = $('a', menu);
    for (const [file, label] of [
      ['manual.html', 'Pehle manual parho'],
      ['channel-setup.html', 'Channel setup']
    ]) {
      const existing = $(`a[href$="${file}"]`, menu);
      if (existing) {
        after = existing;
        continue;
      }
      const link = document.createElement('a');
      link.href = new URL(file, root).href;
      link.textContent = label;
      after.insertAdjacentElement('afterend', link);
      after = link;
    }
  }

  document.addEventListener('click', async e => {
    const btn = e.target.closest('[data-copy]');
    if (!btn) return;
    const target = $(btn.getAttribute('data-copy'));
    const text = target ? target.textContent.trim() : '';
    if (!text) return;
    try { await navigator.clipboard.writeText(text); }
    catch {
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

  const voice = $('#voice');
  if (!voice) return;
  voice.addEventListener('change', async e => {
    const file = e.target.files[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    const audio = new Audio(url);
    await new Promise(resolve => audio.addEventListener('loadedmetadata', resolve, { once: true }));
    const actual = audio.duration;
    const allT = $$('[data-t]').map(el => parseFloat(el.dataset.t));
    const predicted = Math.max(...allT) + 8;
    const ratio = actual / predicted;
    $$('[data-t]').forEach(el => {
      const scaled = parseFloat(el.dataset.t) * ratio;
      el.dataset.scaled = scaled;
      el.textContent = fmt(scaled);
      el.classList.add('scaled');
    });
    $('#actual').textContent = fmt(actual);
    $('#status').hidden = false;
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
    const step = Math.max(1, Math.floor(data.length / w));
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#3F6B46';
    for (let x = 0; x < w; x++) {
      let peak = 0;
      for (let i = 0; i < step; i++) peak = Math.max(peak, Math.abs(data[x * step + i] || 0));
      const bh = peak * h * 0.85;
      ctx.fillRect(x, (h - bh) / 2, 1, bh);
    }
    ctx.fillStyle = '#A8362B';
    $$('[data-t]').forEach(el => {
      const t = parseFloat(el.dataset.scaled || el.dataset.t);
      ctx.fillRect((t / duration) * w, 0, 1, h);
    });
    actx.close();
  }
})();
