# markitdown-converter

Convert common document files to Markdown with Microsoft's MarkItDown.

## Files

- `SKILL.md` — skill contract and runtime behavior.
- `scripts/convert_with_markitdown.sh` — conversion entrypoint.

## Manual run

```bash
bash .codex/skills/markitdown-converter/scripts/convert_with_markitdown.sh \
  --input "/absolute/path/to/input.pdf" \
  --output "/absolute/path/to/output.md" \
  --overwrite
```

## Prerequisite

Have at least one runtime available:

- `uvx` (recommended), or
- `markitdown` command in `PATH`.
