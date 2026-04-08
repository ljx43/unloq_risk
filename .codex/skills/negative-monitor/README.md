# negative-monitor

Repo-local Codex skill under `.codex/skills/negative-monitor`.

## Cloud task / CI

Use the repo as a self-contained Codex home:

```bash
export CODEX_HOME="$PWD/.codex"
```

## Demo runner

This repo includes a demo script that outputs the required Excel/JSON structure:

```bash
python .codex/skills/negative-monitor/scripts/run_monitor.py --input input.json --out-dir output
```

Dependencies:
- `pandas`
- `openpyxl`

Note: the demo runner currently seeds evidence for a small sample set only; it is meant as a template for wiring real retrieval later.
