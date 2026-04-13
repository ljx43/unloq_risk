---
name: markitdown-converter
description: Use this skill to convert local files (pdf/docx/pptx/xlsx/html/images, etc.) into Markdown using Microsoft's MarkItDown.
---

# MarkItDown Converter

## Overview

This skill converts a local input file into a Markdown file using Microsoft's MarkItDown.

## When To Use

Use this skill when the user asks to:
- convert files to Markdown,
- extract readable text from office or PDF files,
- normalize mixed document formats into `.md`.

## Input

Accept these parameters from the user request:
- `input_path` (required): absolute or repo-relative file path.
- `output_path` (optional): target markdown path. Default: `<input_basename>.md` next to input file.
- `overwrite` (optional): `true` or `false` (default `false`).

## Execution

Run:

```bash
bash .codex/skills/markitdown-converter/scripts/convert_with_markitdown.sh \
  --input "<input_path>" \
  [--output "<output_path>"] \
  [--overwrite]
```

## Behavior Rules

1. Always verify the input file exists before conversion.
2. If output exists and `overwrite` is not enabled, stop with a clear message.
3. Prefer `uvx --from markitdown markitdown` first.
4. Fallback to `markitdown` if `uvx` is unavailable.
5. Return the final output markdown path and a short preview (first 20 lines).

## Notes

- MarkItDown may need extra optional dependencies for some formats.
- If both `uvx` and `markitdown` are unavailable, instruct installation:
  - `uv tool install markitdown`
  - or `pipx install markitdown`
