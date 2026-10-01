#!/usr/bin/env bash
set -euo pipefail

git diff --check
if grep -RInE 'TODO:|Fill this in|Capture the project purpose|Describe what belongs here' \
  -- README.md RESEARCH_NOTES.md SOURCES.md ASSUMPTIONS.md docs knowledge \
  notebooks data src figures PROJECT_KNOWLEDGE.md; then
  echo "Found bootstrap placeholder text." >&2
  exit 1
fi
python3 -m py_compile scripts/benchmark.py
python3 scripts/benchmark.py --dry-run >/dev/null
CHECK_ARTIFACT_DIR="${TMPDIR:-/tmp}/ai-speech-lab-benchmark-check-$$"
python3 scripts/benchmark.py \
  --engine-cmd 'touch {output_path}' \
  --engine-ref check-dummy-engine \
  --artifact-dir "$CHECK_ARTIFACT_DIR/artifacts" \
  --results "$CHECK_ARTIFACT_DIR/results.jsonl" \
  --timeout-seconds 10 >/dev/null
test "$(wc -l < "$CHECK_ARTIFACT_DIR/results.jsonl")" -eq 6
