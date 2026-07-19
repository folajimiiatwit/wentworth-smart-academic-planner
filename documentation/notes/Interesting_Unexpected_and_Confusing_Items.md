# Interesting, Unexpected, and Confusing Items

## PDF Text Extraction
Visually clean transcripts do not always produce clean extracted text. In one file, the visible line:

`COMP 3350 UG PROGRAMMING LANGUAGES B+ 4.000 13.32`

was extracted as:

`COMP 3350 UG PROGRAMMINGLANGUAGESB+ 4.000 13.32`

The parser therefore had to identify a grade by its position before credit and quality-point values rather than depending only on spaces.

## In-Progress Heading
The heading `COURSE(S) IN PROGRESS` was sometimes extracted without spaces. A flexible regular expression was required.

## False Grade Matches
A loose grade pattern could mistakenly match the final `S` in words such as `HOURS`. The final logic anchors grade detection to numeric credit values.

## Wrapped Rows
Long course titles and report headings often wrap across lines. The parser combines lines until the next course code is detected.

## Co-op Records
Co-op records can carry a passing `S` grade but should not count as completed academic requirements. The subject `COOP` is therefore excluded explicitly.

## AI Recommendations
Generating a useful curriculum map required prompts that clearly supplied completed courses, remaining requirements, prerequisite constraints, and expected semester load.
