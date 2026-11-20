// SPDX-License-Identifier: MIT
// Copies the pre-rendered front page for 19 November 2026 to the output directory.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const src = join(import.meta.dirname, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")}`);
