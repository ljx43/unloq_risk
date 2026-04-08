# unloq_risk

This repo stores Codex skills and runnable helpers for risk monitoring.

## Why `.codex/skills/`?

Putting skills under `.codex/skills` makes it easy to use in cloud tasks/CI:

```bash
export CODEX_HOME="$PWD/.codex"
# now Codex will find skills in $CODEX_HOME/skills
```

## Included skills

- `.codex/skills/negative-monitor` — negative event monitoring (evidence workbook + JSON + alert text).
