// Compiles the JSON source into the Foundry compendium (LevelDB) and checks it reads back.
//   node tools/pack.mjs   (needs: npm install @foundryvtt/foundryvtt-cli)
import { compilePack, extractPack } from '@foundryvtt/foundryvtt-cli';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const src = path.join(root, 'src', 'legacy-dragons');
const dest = path.join(root, 'packs', 'legacy-dragons');
fs.rmSync(dest, { recursive: true, force: true });
await compilePack(src, dest, { log: false });
const check = fs.mkdtempSync(path.join(os.tmpdir(), 'ld-'));
await extractPack(dest, check, { log: false });
const n = fs.readdirSync(check).length;
const want = fs.readdirSync(src).length;
fs.rmSync(check, { recursive: true, force: true });
console.log(`packed ${want} documents; read back ${n}`);
if (n !== want) process.exit(1);
