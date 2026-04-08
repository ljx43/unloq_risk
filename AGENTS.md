# AGENTS

## Repo intent

- Keep Codex skills under `.codex/skills/` so cloud tasks can set `CODEX_HOME=$PWD/.codex`.
- Do not commit secrets (API keys, tokens, credentials). Use env vars / secret stores.

## Conventions

- Prefer small, composable scripts in each skill's `scripts/`.
- Keep the taxonomy in `references/` and avoid breaking field names across runs.
