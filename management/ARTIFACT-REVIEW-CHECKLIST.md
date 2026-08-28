# Artifact Review Checklist

Use this checklist for human review of `TASK`, `SPEC`, and `PLAN` artifacts.

For deterministic checks, run:

```powershell
python management\validate_artifacts.py
```

Use this manual checklist when you need judgment on clarity, drift risk, or business alignment.

## TASK Review

- [ ] The file follows the current TASK template.
- [ ] `References` identify the user request and source-of-truth artifacts.
- [ ] `In Scope` and `Out of Scope` are explicit and do not conflict.
- [ ] `Scenario` uses coherent Given/When/Then logic.
- [ ] `Business Objective` is specific, measurable, relevant, and time-bounded.
- [ ] `Business Rules` state what must remain true.
- [ ] `Constraints` state hard limits that downstream artifacts must respect.
- [ ] `Assumptions` are explicit instead of hidden in prose.
- [ ] `Open Questions / Blockers` are explicit and carry a status.
- [ ] `Definition of Done` uses stable `DOD-XXX` identifiers and measurable outcomes.
- [ ] No user-story decomposition or implementation detail appears in the TASK.

## SPEC Review

- [ ] The file follows the current SPEC template.
- [ ] `Scope Baseline` carries forward TASK scope, rules, and constraints without weakening them.
- [ ] Every user story has a stable `US-XXX` identifier.
- [ ] Every acceptance scenario has a stable `AS-XXX` identifier.
- [ ] Edge cases are explicit and relevant to the feature.
- [ ] Functional requirements stay at specification level and do not drift into implementation detail.
- [ ] Non-functional requirements are present when quality constraints matter.
- [ ] `Non-Goals` make the excluded behavior explicit.
- [ ] `Traceability Matrix` covers all upstream scope, non-scope, rules, constraints, assumptions, blockers, and `DOD-XXX` identifiers.
- [ ] Success criteria are measurable and tied to requirements or stories.
- [ ] Open questions do not leave correctness-critical ambiguity unresolved.

## PLAN Review

- [ ] The file follows the current PLAN template.
- [ ] `Scope Baseline` matches the approved TASK and SPEC.
- [ ] `Critical Requirements` cover all approved `FR-XXX` and `NFR-XXX` identifiers.
- [ ] `Story to Implementation Mapping` shows how each approved story becomes concrete work.
- [ ] `File Change Contract` names the exact file or artifact areas expected to change.
- [ ] `Implementation Sequence` is deterministic and bounded by approved scope.
- [ ] `Validation Matrix` covers all approved requirements.
- [ ] `Anti-Drift Checks` are explicit and actionable.
- [ ] `Readiness Gate` is complete and does not hide unresolved blockers.
- [ ] The PLAN does not authorize work outside the approved SPEC.

## Chain Review

- [ ] TASK, SPEC, and PLAN all reference the correct upstream artifacts.
- [ ] The matching TASK, SPEC, and PLAN logs exist.
- [ ] No template placeholders remain in the artifacts.
- [ ] No downstream artifact introduces scope that is absent from the upstream artifact.
- [ ] The implementation can be reviewed or executed without needing hidden assumptions.
