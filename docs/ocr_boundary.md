# OCR Boundary

## Current Position

OCR is treated as an assistive input only.

It may help recover visible text from cropped weld callouts, but it is not trusted as authoritative extraction.

## Evidence

Initial OCR probing showed mixed results:

- some images returned usable partial text
- some images returned no text
- some images returned corrupted pattern values
- surrounding diagram noise was often included

## Safe Rule

OCR output must never be treated as ground truth without validation against the image.

## Allowed Use

OCR may be used to:

- suggest visible_text candidates
- support manual observation
- provide a secondary signal for text-heavy callouts

## Disallowed Use

OCR must not yet be used to:

- directly populate benchmark case truth
- overwrite human observation
- infer weld meaning without image validation
- act as the sole source for size, pitch, count, or process fields

## Practical Meaning

Current benchmark pipeline remains:

image -> human observation -> extractor -> structured output

OCR may assist the human observation step, but does not replace it.
