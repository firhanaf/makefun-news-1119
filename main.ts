// SPDX-License-Identifier: MIT
// Copies the pre-rendered front page for 19 November 2026 to the output directory,
// after checking it is a PNG within the bounty's limits (<= 1 MiB, <= 1024x1024).
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const bytes = readFileSync(join(import.meta.dirname, "entry.png"));

if (!bytes.subarray(0, 8).equals(PNG_SIG)) throw new Error("entry.png is not a PNG");
if (bytes.length > 1048576) throw new Error(`entry.png is ${bytes.length} bytes, over 1 MiB`);
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) throw new Error(`entry.png is ${width}x${height}, over 1024x1024`);
if (bytes.subarray(bytes.length - 8, bytes.length - 4).toString("latin1") !== "IEND") {
  throw new Error("entry.png does not end with an IEND chunk");
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), bytes);
console.log(`wrote ${join(outDir, "entry.png")} (${width}x${height}, ${bytes.length} bytes)`);
