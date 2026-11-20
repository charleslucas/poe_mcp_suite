#!/usr/bin/env node
/**
 * make-page.cjs — build the final "what to do" page from a VERIFIED links file.
 *
 * Never retype a trade payload: this script reads the markdown that
 * `generate_trade_urls` wrote (already verified) and injects it into
 * page-template.html. It also re-decodes every link it emits, so a corrupted
 * file cannot reach the user.
 *
 *   node make-page.cjs --links trade_links.md --meta page-meta.json \
 *     --pob "<build.xml>" --itemset BUDGET --out final.html
 *
 * With --pob/--itemset every row's "item" label is derived from the item's own
 * text in the build: base name plus the defence lines PoB writes (`Armour:`,
 * `Evasion:`, `Energy Shield:`, `Ward:`), and the implicit lines for jewellery.
 * A hand-typed label is a guess: a hybrid base recalled as one defence type is
 * wrong in a way that reads perfectly plausible. Derive, don't recall.
 *
 * page-meta.json:
 * {
 *   "title": "<build> — <budget> budget build",
 *   "subtitle": "<class><level> · loadout BUDGET",
 *   "stats": [{ "label": "FullDPS", "value": "28.1M" }],
 *   "rate": 220,                          // chaos per divine
 *   "prices": {                           // keyed by a prefix of the link label
 *     "Body": { "slot": "Body", "note": "…", "chaos": 2200, "pos": 10 }
 *   },                                    // "item" is optional: --pob derives it
 *   "extra_chaos": 1217,                  // uniques/gems priced from poe.ninja
 *   "extras": [{ "slot": "Gems", "item": "…", "what": "…", "price": "5.8 div", "link": "https://…", "pos": 20 }],
 *   "steps": ["…"], "never": ["…"],
 *   "upgrades": [{ "what": "…", "price": "6.8 div", "gain": "+8% DPS" }],
 *   "checks": ["…"],
 *   "total_note": "rares — prices via the links"
 * }
 *
 * `pos` is the row's place in the purchase order (Step 6 of the playbook): the
 * links file arrives in PoB slot order, so rows and extras are merged and sorted
 * by `pos` instead. Same position = original order kept; missing = last.
 */
const fs = require('fs');
const path = require('path');
const z = require('zlib');

function arg(name, fallback) {
  const i = process.argv.indexOf('--' + name);
  return i > -1 ? process.argv[i + 1] : fallback;
}

const linksFile = arg('links');
const metaFile = arg('meta');
const outFile = arg('out', 'final.html');
const template = arg('template', path.join(__dirname, 'page-template.html'));
const pobFile = arg('pob');
const itemSet = arg('itemset');
if (!linksFile || !metaFile) {
  console.error('usage: make-page.cjs --links <verified.md> --meta <meta.json> [--pob <build.xml> --itemset <name>] [--out final.html]');
  process.exit(1);
}
if (pobFile && !itemSet) {
  console.error('--pob needs --itemset (the PoB item-set title, e.g. BUDGET)');
  process.exit(1);
}

const meta = JSON.parse(fs.readFileSync(metaFile, 'utf8'));
const rate = meta.rate || 210;
const fmt = (chaos) => (chaos >= rate ? (chaos / rate).toFixed(1) + ' div' : chaos + 'c');
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Walk the links file: "## Label" followed by a URL line. */
function readLinks(md) {
  const out = [];
  for (const block of md.split(/^## /m).slice(1)) {
    const lines = block.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
    const url = lines.find((l) => l.startsWith('http'));
    if (lines[0] && url) out.push({ label: lines[0], url });
  }
  return out;
}

/** Decode a link; returns the query or throws. */
function decode(url) {
  const payload = url.split('?')[0].split('/').pop();
  return JSON.parse(z.gunzipSync(Buffer.from(payload.replace(/-/g, '+').replace(/_/g, '/'), 'base64')).toString());
}

const DEF_LINES = [['Armour', 'AR'], ['Evasion', 'EV'], ['Energy Shield', 'ES'], ['Ward', 'W']];

/** One PoB item block ("Rarity: …", name, base, def lines, "Implicits: N", mods). */
function parsePobItem(text) {
  const lines = text.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  const ri = lines.findIndex((l) => l.startsWith('Rarity: '));
  const rarity = ri > -1 ? lines[ri].slice(8).trim().toUpperCase() : '';
  const rest = lines.slice(ri + 1);

  // A rare/unique block is "name" then "base"; a magic/normal block has no name
  // line and goes straight to the base followed by "Unique ID: …".
  const hasName = rest[1] && !/^(Unique ID:|Item Level:|Quality:|Sockets:|LevelReq:|Implicits:)/.test(rest[1]);
  const name = hasName ? rest[0] : '';
  const base = hasName ? rest[1] : rest[0] || '';

  const def = DEF_LINES.filter(([word]) => rest.some((l) => l.startsWith(word + ': '))).map(([, short]) => short);

  const ii = rest.findIndex((l) => /^Implicits: \d+/.test(l));
  const implicitCount = ii > -1 ? parseInt(rest[ii].slice(10), 10) : 0;
  const implicits = implicitCount > 0 ? rest.slice(ii + 1, ii + 1 + implicitCount) : [];

  return { rarity, name, base, def: def.join('/'), implicits };
}

/** `rare · EV/ES (<base>)`, `<unique name> (EV/ES, <base>)`, `rare jewel · <base>`. */
function itemLabel(item) {
  const base = item.base;
  if (item.rarity === 'RARE') {
    if (/ Jewel$/.test(base)) return `rare jewel · ${base.replace(/ Jewel$/, '')}`;
    if (item.def) return `rare · ${item.def} (${base})`;
    const implicit = item.implicits.length ? ` (${item.implicits.join('; ')})` : '';
    return `rare · ${base}${implicit}`;
  }
  if (!item.name) return base;
  return item.def ? `${item.name} (${item.def}, ${base})` : `${item.name} (${base})`;
}

/**
 * Map link label -> item, taken from the build itself: item-set slots by name,
 * tree jewels by "Jewel <nodeId>". Returns a Map(label -> label text).
 */
function readPobItems(xml, setName) {
  const items = new Map();
  for (const m of xml.matchAll(/<Item id="(\d+)">([\s\S]*?)<\/Item>/g)) {
    items.set(m[1], parsePobItem(m[2]));
  }

  const labels = new Map();

  for (const m of xml.matchAll(/<ItemSet\b([^>]*)>([\s\S]*?)<\/ItemSet>/g)) {
    const title = (m[1].match(/title="([^"]*)"/) || [])[1] || '';
    if (title !== setName) continue;
    for (const s of m[2].matchAll(/<Slot itemId="(\d+)"[^>]*name="([^"]*)"/g)) {
      if (s[1] !== '0' && items.has(s[1])) labels.set(s[2], itemLabel(items.get(s[1])));
    }
  }

  // Jewels live in the tree spec, not in the item set: <Socket itemId="53" nodeId="6230"/>
  for (const m of xml.matchAll(/<Spec\b([^>]*)>([\s\S]*?)<\/Spec>/g)) {
    const title = (m[1].match(/title="([^"]*)"/) || [])[1] || '';
    if (title !== setName) continue;
    for (const s of m[2].matchAll(/<Socket itemId="(\d+)" nodeId="(\d+)"\s*\/>/g)) {
      if (s[1] !== '0' && items.has(s[1])) labels.set('Jewel ' + s[2], itemLabel(items.get(s[1])));
    }
  }

  return labels;
}

const links = readLinks(fs.readFileSync(linksFile, 'utf8'));
if (links.length === 0) {
  console.error('no links found in ' + linksFile);
  process.exit(1);
}

let total = meta.extra_chaos || 0;
const broken = [];
const pobLabels = pobFile ? readPobItems(fs.readFileSync(pobFile, 'utf8'), itemSet) : new Map();
const unlabeled = [];
const unpositioned = [];

const rows = links.map((link) => {
  const key = Object.keys(meta.prices || {}).find((k) => link.label.startsWith(k)) || '';
  const p = (meta.prices || {})[key] || {};
  const chaos = typeof p.chaos === 'number' ? p.chaos : 0;
  total += chaos;

  // The item label comes from the build when --pob is given; the meta value is
  // only a fallback for a link that has no matching item (and gets reported).
  const derived = pobLabels.get(link.label);
  if (pobFile && !derived) unlabeled.push(link.label);
  if (derived && p.item && p.item !== derived) {
    console.log(`label corrected: "${p.item}" -> "${derived}" (${link.label})`);
  }
  const itemText = derived || p.item || '';

  let ok = true;
  try {
    const q = decode(link.url);
    ok = q && q.status && q.status.option === 'securable';
  } catch (e) {
    ok = false;
  }
  if (!ok) broken.push(link.label);

  // "Item" carries the real name: the unique's name, or category + defence
  // type for a rare ("Shield · ES", "Gloves · EV/ES"). Slot names alone say
  // nothing to the buyer.
  const html = `<tr><td>${esc(p.slot || link.label)}</td>` +
    `<td>${esc(itemText)}</td>` +
    `<td>${esc(p.note || '')}</td>` +
    `<td class="p">${chaos > 0 ? fmt(chaos) : 'see link'}</td>` +
    `<td><a href="${esc(link.url)}" target="_blank">open search</a>${ok ? '' : ' <b>!</b>'}</td></tr>`;
  // `pos` is the row's place in the purchase order (Step 6): uniques, then
  // gems, then rares. The links file is written in PoB slot order, which is
  // not the buying order, so the table is sorted instead of trusting it.
  if (typeof p.pos !== 'number') unpositioned.push(link.label);
  return { pos: typeof p.pos === 'number' ? p.pos : 900, html };
});

// A cell that holds a trade URL becomes a link, and it is decoded like every
// other link on the page: a gem search nobody validated is just as broken as a
// corrupted payload.
const extras = (meta.extras || []).map((e) => {
  let cell = esc(e.link || '—');
  if (e.link && /^https?:/.test(e.link)) {
    let ok = true;
    try {
      const q = decode(e.link);
      ok = q && q.status && q.status.option === 'securable';
    } catch (err) {
      ok = false;
    }
    if (!ok) broken.push(e.item || e.label || e.link);
    cell = `<a href="${esc(e.link)}" target="_blank">open search</a>${ok ? '' : ' <b>!</b>'}`;
  }
  const html = `<tr><td>${esc(e.slot)}</td><td>${esc(e.item || '')}</td><td>${esc(e.what)}</td><td class="p">${esc(e.price)}</td><td>${cell}</td></tr>`;
  if (typeof e.pos !== 'number') unpositioned.push(e.item || e.label || '(extra)');
  return { pos: typeof e.pos === 'number' ? e.pos : 900, html };
});

// One table, one order: stable sort by `pos`, so rows keep their file order
// inside the same position. Untagged rows sort last instead of being scattered.
const ordered = [...rows, ...extras]
  .map((r, i) => ({ ...r, i }))
  .sort((a, b) => a.pos - b.pos || a.i - b.i)
  .map((r) => r.html)
  .join('\n');

const templateText = fs.readFileSync(template, 'utf8');
// Plain String.replace substitutes only the FIRST match, which silently leaves
// {{TITLE}} unrendered in <h1> (it also appears in <title>). Replace globally.
const fill = (text, key, value) => text.split(key).join(value);

let html = templateText;
html = fill(html, '{{TITLE}}', esc(meta.title || 'Budget loadout'));
html = fill(html, '{{SUBTITLE}}', esc(meta.subtitle || ''));
html = fill(html, '{{STATS}}', (meta.stats || []).map((s) => `<div class="stat"><span>${esc(s.label)}</span><b>${esc(s.value)}</b></div>`).join(''));
html = fill(html, '{{ROWS}}', ordered);
html = fill(html, '{{EXTRAS}}', '');
html = fill(html, '{{TOTAL}}', `<b>Total: ${(total / rate).toFixed(1)} div</b> · rate 1 div ≈ ${rate}c${meta.total_note ? ' · ' + esc(meta.total_note) : ''}`);
html = fill(html, '{{STEPS}}', (meta.steps || []).map((s) => `<li>${s}</li>`).join('\n'));
html = fill(html, '{{NEVER}}', (meta.never || []).map((s) => `<li>${s}</li>`).join('\n'));
html = fill(html, '{{UPGRADES}}', (meta.upgrades || []).map((u) =>
  `<tr><td>${esc(u.what)}</td><td class="p">${esc(u.price)}</td><td>${esc(u.gain)}</td></tr>`).join('\n'));
html = fill(html, '{{CHECKS}}', (meta.checks || []).map((s) => `<li>${s}</li>`).join('\n'));
html = fill(html, '{{GENERATED}}', new Date().toISOString().slice(0, 16).replace('T', ' '));

const leftovers = html.match(/\{\{[A-Z_]+\}\}/g);
if (leftovers) {
  console.error('unfilled placeholders: ' + [...new Set(leftovers)].join(', '));
  process.exit(1);
}

fs.writeFileSync(outFile, html, 'utf8');

console.log(`page: ${outFile}`);
console.log(`links: ${links.length}, broken: ${broken.length}`);
if (pobFile) console.log(`labels from PoB (${itemSet}): ${links.length - unlabeled.length}/${links.length}`);
if (unpositioned.length) console.log(`NO pos (appended at the end): ${unpositioned.join(', ')}`);
if (unlabeled.length) {
  console.log(`NO ITEM IN BUILD (label left to meta): ${unlabeled.join(', ')}`);
  process.exit(1);
}
if (broken.length) {
  console.log('BROKEN: ' + broken.join(', '));
  process.exit(1);
}
