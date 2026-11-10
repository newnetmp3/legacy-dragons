// Draws one token per dragon type: tools/token-list.json -> <out>/<key>.png (512x512).
// Icons: game-icons.net (CC BY 3.0), see tools/icons and the README.
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';

const { chromium } = createRequire(import.meta.url)('playwright');
const [, , listFile, iconDir, outDir] = process.argv;
const list = JSON.parse(fs.readFileSync(listFile, 'utf8'));
fs.mkdirSync(outDir, { recursive: true });

const shade = (hex, f) => {  // f < 0 darker, > 0 lighter
  const n = parseInt(hex.slice(1), 16);
  const ch = [n >> 16, (n >> 8) & 255, n & 255].map((c) => Math.round(f < 0 ? c * (1 + f) : c + (255 - c) * f));
  return '#' + ch.map((c) => c.toString(16).padStart(2, '0')).join('');
};
const lum = (hex) => {
  const n = parseInt(hex.slice(1), 16);
  return (0.299 * (n >> 16) + 0.587 * ((n >> 8) & 255) + 0.114 * (n & 255)) / 255;
};
const iconPaths = (name) => {
  const svg = fs.readFileSync(path.join(iconDir, name + '.svg'), 'utf8');
  // Every path but the first (the icon's black background square).
  return [...svg.matchAll(/<path[^>]*\sd="([^"]+)"/g)].slice(1).map((m) => m[1]);
};

function tokenSvg(d) {
  const c = d.color;
  const light = lum(c) > 0.62;
  const fg = light ? shade(c, -0.78) : shade(c, 0.88);
  const rim = shade(c, light ? -0.45 : -0.55);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <radialGradient id="bg" cx="50%" cy="40%" r="65%">
      <stop offset="0" stop-color="${shade(c, 0.25)}"/><stop offset="0.65" stop-color="${c}"/><stop offset="1" stop-color="${shade(c, -0.5)}"/>
    </radialGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${shade(rim, 0.55)}"/><stop offset="0.5" stop-color="${rim}"/><stop offset="1" stop-color="${shade(rim, 0.35)}"/>
    </linearGradient>
    <pattern id="scales" width="36" height="22" patternUnits="userSpaceOnUse">
      <path d="M0 22 A18 18 0 0 1 36 22 M-18 11 A18 18 0 0 1 18 11 M18 11 A18 18 0 0 1 54 11" fill="none"
            stroke="${light ? '#000' : '#fff'}" stroke-opacity="0.09" stroke-width="2"/>
    </pattern>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#000" flood-opacity="0.55"/>
    </filter>
    <clipPath id="disc"><circle cx="256" cy="256" r="232"/></clipPath>
  </defs>
  <circle cx="256" cy="256" r="232" fill="url(#bg)"/>
  <rect width="512" height="512" fill="url(#scales)" clip-path="url(#disc)"/>
  <g filter="url(#shadow)" transform="translate(256 262) scale(0.72) translate(-256 -256)">
    ${iconPaths(d.icon).map((p) => `<path d="${p}" fill="${fg}"/>`).join('')}
  </g>
  <circle cx="256" cy="256" r="240" fill="none" stroke="url(#ring)" stroke-width="22"/>
  <circle cx="256" cy="256" r="228" fill="none" stroke="${shade(rim, 0.7)}" stroke-opacity="0.6" stroke-width="2"/>
  <circle cx="256" cy="256" r="251" fill="none" stroke="#000" stroke-opacity="0.5" stroke-width="2"/>
</svg>`;
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 512, height: 512 }, deviceScaleFactor: 1 });
for (const d of list) {
  await page.setContent(`<html><body style="margin:0;background:transparent">${tokenSvg(d)}</body></html>`);
  await page.locator('svg').screenshot({ path: path.join(outDir, d.key + '.png'), omitBackground: true });
}
await browser.close();
console.log(`${list.length} tokens`);
