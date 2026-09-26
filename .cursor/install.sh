#!/usr/bin/env bash
# Idempotent bootstrap for the Grid Bot Builder + DeFi Program skills archive.
# Prepares the Node export pipeline, the Python tooling, and wires system Chrome
# to the path the Playwright-based export scripts expect.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# 1. Node dependencies for the course export pipeline
#    (playwright-core, mermaid, marked, docx) — used by programs/defi-program/export.
( cd programs/defi-program/export && npm ci )

# 2. Python tooling. The calculators and doc builders are stdlib-only; these
#    packages cover the export PDF/image crop path (pymupdf) and MCP skill dev.
python3 -m pip install --user --break-system-packages --no-warn-script-location pymupdf
python3 -m pip install --user --break-system-packages --no-warn-script-location \
  -r .claude/skills/mcp-builder/scripts/requirements.txt

# 3. The Playwright export scripts default to
#    /opt/pw-browsers/chromium-1194/chrome-linux/chrome (overridable via
#    CHROMIUM_PATH). Point that path at the system Chrome so the render/PDF/video
#    scripts work with zero extra configuration.
sudo mkdir -p /opt/pw-browsers/chromium-1194/chrome-linux
sudo ln -sf /usr/bin/google-chrome-stable /opt/pw-browsers/chromium-1194/chrome-linux/chrome

echo "Environment bootstrap complete."
