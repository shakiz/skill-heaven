#!/usr/bin/env bash
# Build a marketplace ZIP for one skill: tools/package_skill.sh <skill-name> <version>
# Excludes tests (evals/), caches and OS files. Output: dist/<skill>-v<version>.zip
set -euo pipefail
skill="${1:?skill name}"; version="${2:?version, e.g. 1.0.0}"
root="$(cd "$(dirname "$0")/.." && pwd)"
src="$root/skills/$skill"
[ -f "$src/SKILL.md" ] || { echo "No SKILL.md in $src" >&2; exit 1; }
mkdir -p "$root/dist"
out="$root/dist/$skill-v$version.zip"
rm -f "$out"
(cd "$root/skills" && zip -qr "$out" "$skill" \
  -x "$skill/evals/*" "*/__pycache__/*" "*.pyc" "*/.DS_Store" "*-workspace/*")
files=$(unzip -Z1 "$out" | grep -v '/$' | wc -l | tr -d ' ')
size=$(du -h "$out" | cut -f1)
echo "Built $out ($files files, $size)"
grep -rnE "https?://|requests\.|urllib|socket\." "$src" --include=*.py && echo "WARNING: network-looking code above" || echo "No network calls in scripts."
