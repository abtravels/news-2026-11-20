import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry program for the news-image-20261120 bounty.
// Copies the pre-rendered image ./entry.png into the output directory
// the harness reads (MAKEFUN_OUTPUT_DIR, or /output by default).

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
console.log(`entry.png -> ${join(outDir, "entry.png")}`);
