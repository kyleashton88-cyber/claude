#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const dir = __dirname;
const html = fs.readFileSync(path.join(dir, "index.html"), "utf8");
const engine = fs.readFileSync(path.join(dir, "engine.js"), "utf8");
const token = '<script src="engine.js"></script>';
if (!html.includes(token)) {
  console.error("index.html no longer has the engine script tag to inline.");
  process.exit(1);
}
const product = html.replace(
  token,
  "<script>\n" + engine + "\n</script>"
);
const out = path.join(dir, "On-Chain-Operator-Calculator.html");
fs.writeFileSync(out, product);
if (product.includes('src="engine.js"') || !product.includes("OcoCalc") || !product.includes("7dffe0")) {
  console.error("Product file failed its own checks.");
  process.exit(1);
}
const kb = Math.round(fs.statSync(out).size / 1024);
console.log("Wrote " + path.basename(out) + " (" + kb + " KB). Open it in a browser. It needs no other files.");
