---
description: "Implementation plan template for the PLAN stage"
---

# Plan : PLAN-XXXX

**Input**: Approved SPEC file from `/management/specs/SPEC-XXXX.md`
**Traceability**: originating TASK, TASK-LOG, SPEC, SPEC-LOG, and PLAN-LOG
**Purpose**: Describe the implementation approach only. Do not include code changes, and do not begin implementation until TASK, SPEC, and PLAN are all complete and approved.

## Summary

[Summarize the implementation approach, the primary stories being addressed, and the intended delivery sequence.]

## Source Artifacts

- TASK file: `/management/tasks/TASK-XXXX.md`
- TASK-LOG: `/management/tasks-logs/TASK-LOG-XXXX.md`
- SPEC file: `/management/specs/SPEC-XXXX.md`
- SPEC-LOG: `/management/specs-logs/SPEC-LOG-XXXX.md`
- PLAN-LOG: `/management/plans-logs/PLAN-LOG-XXXX.md`

## Scope Baseline

### In Scope

- `T-001`: [Copied from TASK]
- `T-002`: [Copied from TASK]

### Out of Scope

- `T-OUT-001`: [Copied from TASK]
- `T-OUT-002`: [Copied from TASK]

### Critical Requirements

- `FR-001`: [Copied from SPEC]
- `FR-002`: [Copied from SPEC]
- `NFR-001`: [Copied from SPEC or `N/A`]

## Technical Context

**Language/Version**: [e.g., .NET 10, TypeScript 5.7, Python 3.11 or NEEDS CLARIFICATION]

**Primary Dependencies**: [frameworks, libraries, services, or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL, files, Redis, or N/A]

**Testing**: [e.g., xUnit, Playwright, pytest, or NEEDS CLARIFICATION]

**Target Platform**: [e.g., Linux server, browser, mobile, or NEEDS CLARIFICATION]

**Project Type**: [e.g., library, CLI, web service, mobile app, or NEEDS CLARIFICATION]

**Performance Goals**: [domain-specific goals or NEEDS CLARIFICATION]

**Constraints**: [domain-specific constraints or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific scale or NEEDS CLARIFICATION]

## Story to Implementation Mapping

| Story / Requirement | Planned Work | Target Files / Areas | Validation |
|---------------------|--------------|----------------------|------------|
| `US-001`, `FR-001` | [Concrete implementation step] | `[path/or/area]` | [Test, review, or check] |
| `US-002`, `FR-002` | [Concrete implementation step] | `[path/or/area]` | [Test, review, or check] |

## File Change Contract

- `[path/to/file-or-folder]`: [Why it is expected to change]
- `[path/to/file-or-folder]`: [Why it is expected to change]

## Implementation Sequence

1. [Sequence step]. Traceability: [`US-XXX`, `FR-XXX`]
2. [Sequence step]. Traceability: [`US-XXX`, `FR-XXX`]
3. [Sequence step]. Traceability: [`US-XXX`, `FR-XXX`]

## Data / Interface Contracts *(include when relevant)*

- [Contract or schema impacted and the expected change]
- [API, DTO, document structure, or integration boundary impacted]

## Validation Matrix

| Requirement / Story | Validation Method | Evidence Expected |
|---------------------|-------------------|------------------|
| `FR-001` | [Unit test, integration test, manual review, diff check] | [What proves success] |
| `FR-002` | [Unit test, integration test, manual review, diff check] | [What proves success] |
| `NFR-001` | [Performance, accessibility, security, or content review] | [What proves success] |

## Risks / Open Questions

- **Q-001**: [Open question]. Status: [Open|Resolved]. Action: [Next step]
- **R-001**: [Implementation risk and mitigation]

## Anti-Drift Checks

- Every planned change maps to an approved `US-XXX`, `FR-XXX`, or `NFR-XXX`.
- No file outside the file change contract may be modified without updating the PLAN.
- No out-of-scope item may appear in implementation steps.
- Any unresolved blocker pauses implementation until explicitly resolved.

## Complexity Tracking

> Fill only if local rules or repository constraints require justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [item] | [reason] | [alternative] |

## Readiness Gate

- [ ] TASK exists and is complete
- [ ] SPEC exists and is complete
- [ ] TASK-LOG exists and is current
- [ ] SPEC-LOG exists and is current
- [ ] PLAN-LOG exists before plan generation continues
- [ ] Every `DOD-XXX` is covered by one or more `FR-XXX`, `NFR-XXX`, or `US-XXX`
- [ ] No blocking `Q-XXX` remains open for implementation
- [ ] The file change contract is explicit enough to constrain implementation

## Readiness Check

- Implementation must not begin until the readiness gate is fully satisfied.
