# Next Capability

## Target

Support explicit weld size extraction.

## Why

A weld system that cannot represent stated weld size is incomplete.

## Requirement

Case 005 must include a visible numeric weld size and force the extractor to output:

- `size_mm`

## Rule

Do not implement OCR or automatic number reading yet.

First:
1. create a manual benchmark case with explicit size
2. update extraction logic to preserve `size_mm`
3. make the case pass
4. rerun full suite
