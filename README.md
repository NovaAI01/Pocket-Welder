# Pocket Welder

## Purpose

Pocket Welder converts a welding drawing into structured weld instructions.

It is not a general CAD system.
It is not a welding simulator.
It is not a full fabrication planning tool.

The first proof exists to answer one question:

**Can a drawing be turned into correct structured weld instructions reliably enough to justify continued development?**

---

## Phase 1 Goal

Build the smallest working proof.

### Input

One welding drawing provided as:

- image
- photo
- PDF page

### Output

Structured weld instructions in JSON.

Example output shape:

```json
{
  "drawing_id": "example_001",
  "welds": [
    {
      "joint_id": "J1",
      "process": null,
      "symbol": "square_groove",
      "side": "both_sides",
      "contour": "flush_one_side",
      "size_mm": null,
      "length_mm": null,
      "pitch_mm": null,
      "finish": "ground",
      "count": 8,
      "notes": []
    }
  ]
}
