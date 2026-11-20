// Entry program for the make.fun news-image-20261120 bounty.
//
// The front page itself is composed ahead of time by compose.py and stored
// next to this file as entry.png. The grader runs this program offline and
// expects the picture at /output/entry.png, so the whole job here is one
// file copy. For a local dry run, MAKEFUN_OUTPUT_DIR can stand in for
// /output:
//
//   MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));

// Notes: entry.png is committed to the repository, so this program needs no
// network, no build step and no arguments. Rebuild the picture itself with
// `python3 compose.py` (deterministic: same inputs, same bytes).
