// grill-form round page. A round HTML file holds only the round JSON and imports this script; see SKILL.md for the stub.
(() => {
  'use strict';
  const DATA = JSON.parse(document.getElementById('grill-data').textContent);

  const CSS = `
:root { color-scheme: light dark; --bg:#f6f6f3; --fg:#1d1d1b; --muted:#6b6b66; --card:#fff; --line:#d8d8d2; --accent:#2f5fd0; --accent-bg:#e9efff; --warn:#a15c00; --ok:#1f7a3a; }
@media (prefers-color-scheme: dark) { :root { --bg:#151614; --fg:#e8e8e3; --muted:#a0a09a; --card:#1f201d; --line:#3a3b37; --accent:#8fb0ff; --accent-bg:#1f2a44; --warn:#f0b35a; --ok:#7fd49a; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
main { max-width: 900px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { font-size: 1.5rem; margin: 0 0 4px; }
.meta { color: var(--muted); font-size: .9rem; }
.intro { margin: 12px 0 16px; }
.howto { font-size: .9rem; color: var(--muted); border: 1px dashed var(--line); border-radius: 8px; padding: 8px 12px; margin: 0 0 24px; }
.q { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; margin: 0 0 18px; }
.q.answered { border-color: var(--ok); }
.q h2 { font-size: 1.1rem; margin: 0 0 8px; display: flex; gap: 8px; align-items: baseline; }
.q h2 .id { color: var(--accent); }
.q p { margin: 8px 0; }
details { margin: 10px 0; border-left: 3px solid var(--line); padding-left: 12px; }
details summary { cursor: pointer; color: var(--muted); user-select: none; }
details[open] summary { color: var(--fg); margin-bottom: 4px; }
.options { list-style: none; margin: 12px 0 0; padding: 0; }
.options li { margin: 6px 0; }
.options label { display: flex; gap: 10px; align-items: flex-start; padding: 8px 10px; border-radius: 8px; border: 1px solid transparent; cursor: pointer; }
.options label:hover { background: var(--accent-bg); }
.options input { margin: 4px 0 0; flex: 0 0 auto; }
.options input:checked + span { font-weight: 600; }
.badge { display: inline-block; font-size: .75rem; font-weight: 500; padding: 1px 7px; border-radius: 999px; margin-left: 6px; vertical-align: middle; background: var(--accent-bg); color: var(--accent); }
.detail { display: block; color: var(--muted); font-size: .9rem; font-weight: 400; }
.unclear label { border: 1px dashed var(--warn); }
.unclear input:checked + span { color: var(--warn); }
textarea { width: 100%; min-height: 72px; margin-top: 10px; padding: 8px 10px; border-radius: 8px; border: 1px solid var(--line); background: var(--bg); color: var(--fg); font: inherit; resize: vertical; }
.result { margin-top: 24px; }
.result .bar { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.result .progress { flex: 1 1 auto; color: var(--muted); }
.result .status { font-size: .9rem; color: var(--ok); }
#output { min-height: 260px; font-family: ui-monospace, Consolas, monospace; font-size: .9rem; white-space: pre; }
button { font: inherit; padding: 8px 14px; border-radius: 8px; border: 1px solid var(--line); background: var(--bg); color: var(--fg); cursor: pointer; }
button.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
code { background: var(--accent-bg); padding: 0 4px; border-radius: 4px; font-size: .9em; }
pre { background: var(--bg); border: 1px solid var(--line); padding: 10px; border-radius: 8px; overflow-x: auto; }
pre code { background: none; padding: 0; }
`;

  function escapeHtml(s) { return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
  function inline(s) { return escapeHtml(s).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>'); }
  function md(text) {
    if (!text) return '';
    return String(text).replace(/\r\n/g, '\n').split(/\n{2,}/).map(block => {
      if (block.startsWith('```')) return '<pre><code>' + escapeHtml(block.replace(/^```[^\n]*\n?/, '').replace(/\n?```\s*$/, '')) + '</code></pre>';
      const lines = block.split('\n');
      if (lines.every(l => /^\s*[-*] /.test(l))) return '<ul>' + lines.map(l => '<li>' + inline(l.replace(/^\s*[-*] /, '')) + '</li>').join('') + '</ul>';
      return '<p>' + inline(block).replace(/\n/g, '<br>') + '</p>';
    }).join('');
  }

  function renderQuestion(q) {
    const qid = escapeHtml(q.id);
    const options = (q.options || []).map(o => '<li><label><input type="checkbox" data-opt="' + escapeHtml(o.id) + '"><span>' + inline(o.label) + (o.recommended ? '<span class="badge">recommended</span>' : '') + (o.detail ? '<span class="detail">' + inline(o.detail) + '</span>' : '') + '</span></label></li>').join('');
    const unclear = '<li class="unclear"><label><input type="checkbox" data-unclear="1"><span>The question is unclear<span class="detail">Say below what is unclear or what you would need to know first.</span></span></label></li>';
    const context = q.context ? '<details><summary>Context</summary>' + md(q.context) + '</details>' : '';
    return '<section class="q" data-q="' + qid + '"><h2><span class="id">' + qid + '</span><span>' + inline(q.title) + '</span></h2>' + md(q.body) + context + '<ul class="options">' + options + unclear + '</ul><textarea placeholder="Own answer, nuance or comment (optional)"></textarea></section>';
  }

  function render() {
    const style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);
    document.title = DATA.topic + ' · round ' + DATA.round;
    const n = DATA.questions.length;
    const parts = ['<h1>' + inline(DATA.topic) + '</h1><div class="meta">Round ' + DATA.round + ' · ' + n + ' question' + (n === 1 ? '' : 's') + '</div>'];
    if (DATA.intro) parts.push('<div class="intro">' + md(DATA.intro) + '</div>');
    parts.push('<div class="howto">Tick every option that applies, or write your own answer under a question. When done, press <strong>Generate</strong> at the bottom and paste the Markdown it shows into the chat.</div>');
    for (const q of DATA.questions) parts.push(renderQuestion(q));
    parts.push('<div class="result"><div class="bar"><span class="progress" id="progress"></span><span class="status" id="status"></span><button id="copy" type="button">Copy</button><button id="generate" class="primary" type="button">Generate</button></div><textarea id="output" readonly hidden></textarea></div>');
    const main = document.createElement('main');
    main.innerHTML = parts.join('');
    document.body.appendChild(main);
    main.addEventListener('change', refresh);
    main.addEventListener('input', refresh);
    document.getElementById('generate').addEventListener('click', generate);
    document.getElementById('copy').addEventListener('click', copy);
    refresh();
  }

  function readAnswer(section) {
    const selected = [...section.querySelectorAll('input[data-opt]:checked')].map(i => i.dataset.opt);
    const unclear = !!section.querySelector('input[data-unclear]:checked');
    const custom = section.querySelector('textarea').value.trim();
    return (selected.length || unclear || custom) ? { selected, unclear, custom } : null;
  }
  function sectionOf(qid) { return [...document.querySelectorAll('section.q')].find(s => s.dataset.q === qid); }

  function refresh() {
    let answered = 0;
    for (const section of document.querySelectorAll('section.q')) {
      const done = readAnswer(section) !== null;
      section.classList.toggle('answered', done);
      if (done) answered++;
    }
    document.getElementById('progress').textContent = answered + ' of ' + DATA.questions.length + ' answered';
  }

  function answersMarkdown() {
    const lines = ['# grill-form answers · ' + DATA.topic + ' · round ' + DATA.round, ''];
    for (const q of DATA.questions) {
      const a = readAnswer(sectionOf(q.id));
      lines.push('## ' + q.id + ' — ' + q.title);
      if (!a) { lines.push('- (no answer)', ''); continue; }
      const picked = (q.options || []).filter(o => a.selected.includes(o.id)).map(o => o.id + ') ' + o.label);
      if (picked.length) lines.push('- Selected: ' + picked.join('; '));
      if (a.unclear) lines.push('- The question is unclear');
      if (a.custom) lines.push('- Own answer: ' + a.custom.replace(/\n/g, '\n  '));
      lines.push('');
    }
    return lines.join('\n');
  }

  function generate() {
    const output = document.getElementById('output');
    output.value = answersMarkdown();
    output.hidden = false;
    output.focus();
    output.select();
    document.getElementById('status').textContent = 'Select all and paste into the chat';
  }
  async function copy() {
    generate();
    try { await navigator.clipboard.writeText(document.getElementById('output').value); document.getElementById('status').textContent = 'Copied. Paste into the chat.'; }
    catch (e) { document.getElementById('status').textContent = 'Clipboard refused; copy the selected text by hand.'; }
  }

  // The round stub has no <body>: the script runs while the parser is still in <head>, so wait for the document to exist.
  if (document.body) render(); else document.addEventListener('DOMContentLoaded', render);
})();
