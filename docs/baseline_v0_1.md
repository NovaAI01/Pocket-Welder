# Pocket Welder Baseline v0.1

## Status

Manual case extraction baseline established.

## Passing Cases

- case_001: compound symbol structure
- case_002: fillet + stitch
- case_003: square groove + both sides + flush one side
- case_004: fillet + all-around

## Current Supported Fields

- symbol
- side
- contour
- reference_text
- stitch note
- all-around note

## Not Yet Supported

- explicit weld size
- explicit length
- explicit pitch
- finish letter decoding
- tail note interpretation
- automatic image parsing

## Validation

`python3 ~/Dev/pocket_welder/scripts/run_all_cases.py`

Expected result:

- total_cases = 4
- passed = 4
- failed = 0
