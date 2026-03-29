+# Pocket Welder System Boundary v0.5

## Current Capability

Pocket Welder v0.5 supports single-callout extraction only.

It can currently represent and validate controlled manual benchmark cases for:

- weld symbol type
- side interpretation
- contour interpretation
- all-around modifier
- intermittent/stitch indication
- process-context support
- numeric weld size
- numeric weld length
- numeric weld pitch
- weld count
- a/z notation recognition in notes

## Explicit Boundary

Pocket Welder v0.5 does not yet perform automatic extraction directly from images.

It currently depends on manually defined benchmark cases and deterministic extraction logic built from structured human observation.

## Multi-Callout Limitation

Multi-callout drawings are detected but not yet extracted into multiple weld records.

Current behavior for multi-callout input:

- detect that multiple callouts exist
- return an explicit unsupported state
- avoid pretending that a single weld output represents the full drawing

## Schema Limitation

a/z semantics are recognised in notes, but are not yet represented as first-class schema fields.

This means the current schema does not yet explicitly model:

- size_type
- secondary_size_mm
- secondary_size_type

These semantics are preserved in benchmark case observations and output notes only.

## Safe Interpretation Rule

Pocket Welder must prefer explicit uncertainty over invented detail.

If the drawing does not clearly support a field value, the system must preserve ambiguity using:

- null
- notes
- unsupported detection states

## Baseline Status

Current validated baseline:

- 8 benchmark cases
- 8 passing
- 0 failing

Validation command:

```bash
python3 ~/Dev/pocket_welder/scripts/run_all_cases.py

```

## Meaning of v0.5

Pocket Welder v0.5 is a controlled extraction baseline, not a production image-reading system.

Its value is that behavior is:

- explicit
- testable
- repeatable
- versioned

