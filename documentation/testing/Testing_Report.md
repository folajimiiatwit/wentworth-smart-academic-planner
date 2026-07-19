# Testing Report

## Testing Strategy
Testing covered transcript parsing, course classification, degree-progress logic, course selection, schedule conflict detection, API integration, and end-to-end user workflows.

## Representative Transcript Tests

| Test | Expected Result | Status |
|---|---|---|
| Standard completed course with grade A/B/C | Course included | Passed |
| Withdrawn course with W | Course excluded | Passed |
| Failed course with F | Course excluded | Passed |
| Co-op course with S | Course excluded | Passed |
| Course listed after in-progress marker | Course excluded | Passed |
| Transfer course with TR | Course included | Passed |
| Wrapped course title | Course row reconstructed | Passed |
| Grade merged into title, e.g. `LANGUAGESB+` | Grade detected from trailing credit pattern | Passed after parser adjustment |
| Duplicate course occurrence | Course appears once | Passed |
| Unknown transcript layout | User verification required | Known limitation |

## Functional Tests

| Area | Test | Result |
|---|---|---|
| Authentication | Valid user can enter application | Passed |
| Transcript upload | PDF/DOCX upload accepted | Passed |
| Course review | Detected courses displayed | Passed |
| Degree progress | Remaining requirements calculated | Passed |
| Course selection | Completed courses not recommended again | Passed |
| Schedule | Overlapping sections flagged | Passed |
| Curriculum map | Recommended future terms generated | Passed |
| Error handling | Invalid or empty upload does not crash app | Passed/needs continued edge-case testing |

## Acceptance Result
The prototype satisfies the main project goals and is suitable for demonstration and local use. Additional transcript samples and deployment testing are recommended before production release.
