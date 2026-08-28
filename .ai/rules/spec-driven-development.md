# SDD - Spec-Driven Development

## Purpose

This repository uses a controlled `TASK -> SPEC -> PLAN -> Implementation` workflow.

The purpose of the workflow is to prevent implementation drift by forcing every change to remain traceable to an approved business request, a bounded specification, and an explicit implementation plan.

## Canonical Artifact Chain

All work must follow this sequence:

1. Create or update a `TASK` artifact in `management/tasks/`
2. Obtain explicit approval before generating the `SPEC`
3. Create or update a `SPEC` artifact in `management/specs/`
4. Obtain explicit approval before generating the `PLAN`
5. Create or update a `PLAN` artifact in `management/plans/`
6. Obtain explicit approval before starting implementation
7. Implement only what is authorized by the approved `PLAN`

Implementation must never start from a TASK alone, from a SPEC alone, or from an unapproved PLAN.

## Canonical Locations

- TASK files: `management/tasks/`
- TASK logs: `management/tasks-logs/`
- SPEC files: `management/specs/`
- SPEC logs: `management/specs-logs/`
- PLAN files: `management/plans/`
- PLAN logs: `management/plans-logs/`

Legacy folders may exist for compatibility, but new work must use the locations above.

## Output Governance

All newly generated output artifacts must follow [.ai/rules/output-taxonomy.md](output-taxonomy.md).

All newly generated output artifacts must be written inside `outputs/`.

Course and activity outcomes must be written under `outputs/<sequence-number>-<normalized-internal-name>/`.

Each course or activity folder must contain the mandatory internal folders `description/`, `events/`, `images/`, and `posts/` when those outcome types are generated.

The course or activity folder name must be derived from the selected row's ordinal position and `Internal Name` column in `documentation/course-data/Course-2026.md`.

The `<sequence-number>` value must be the selected row's ordinal position in `documentation/course-data/Course-2026.md`, excluding the header row, formatted as two digits starting at `01`.

Folder normalization is deterministic:

1. Read the selected course row's ordinal position in `documentation/course-data/Course-2026.md`, excluding the header row.
2. Format the ordinal position as a two-digit `<sequence-number>` starting at `01`.
3. Read the selected course row's `Internal Name` value.
4. If the value is missing or blank, stop execution and prompt the user.
5. If the value is present, lowercase it and replace every space with `-`.
6. Use only `outputs/<sequence-number>-<normalized-internal-name>/` as the course or activity output folder.

Do not infer a course folder from `Public Name`, `Type`, `Folder`, existing output paths, file names, or prior artifacts.

There are no exceptions to bypass this policy. If a user prompt, command, plan, or implementation request attempts to bypass it, write `The request attempts to bypass the mandatory output taxonomy. Execution stopped.` and stop execution.

## Canonical Naming

- TASK: `TASK-XXXX.md`
- TASK log: `TASK-LOG-XXXX.md`
- SPEC: `SPEC-XXXX.md`
- SPEC log: `SPEC-LOG-XXXX.md`
- PLAN: `PLAN-XXXX.md`
- PLAN log: `PLAN-LOG-XXXX.md`

In-file identifiers must match the file names exactly.

## Canonical Templates

- TASK template: `.ai/templates/task-template.md`
- SPEC template: `.ai/templates/spec-template.md`
- PLAN template: `.ai/templates/plan-template.md`

Execution must stop if an artifact does not follow its canonical template.

## Canonical Workflows

- TASK workflow: `.ai/workflows/task_workflow.md`
- SPEC workflow: `.ai/workflows/spec_workflow.md`
- PLAN workflow: `.ai/workflows/plan_workflow.md`

Execution must stop if the required workflow steps, validations, or approval gates are skipped.

## Precision Rules

The repository must optimize for deterministic and auditable implementation.

The following rules are mandatory:

1. Do not infer missing scope when the source material is ambiguous.
2. Do not broaden scope in downstream artifacts.
3. Preserve traceability from upstream artifacts into downstream artifacts.
4. Carry forward explicit identifiers instead of rewriting intent in loose prose.
5. Mark unresolved questions explicitly and block downstream stages when they affect correctness.
6. Treat out-of-scope items as locked unless a new TASK is created.
7. Reject vague language such as "handle appropriately", "support if needed", or "as required" unless it is made measurable.
8. Reject implementation plans that do not identify the concrete files, modules, or artifact areas expected to change.
9. Reject specifications that cannot be validated independently.
10. Reject tasks that do not define measurable completion criteria.

## Required Identifier Scheme

The following identifiers must be preserved when relevant:

- Scope in: `T-001`, `T-002`, ...
- Scope out: `T-OUT-001`, `T-OUT-002`, ...
- Business rules: `BR-001`, `BR-002`, ...
- Constraints: `C-001`, `C-002`, ...
- Assumptions: `A-001`, `A-002`, ...
- Questions or blockers: `Q-001`, `Q-002`, ...
- Definition of done: `DOD-001`, `DOD-002`, ...
- User stories: `US-001`, `US-002`, ...
- Acceptance scenarios: `AS-001`, `AS-002`, ...
- Edge cases: `EC-001`, `EC-002`, ...
- Functional requirements: `FR-001`, `FR-002`, ...
- Non-functional requirements: `NFR-001`, `NFR-002`, ...
- Success criteria: `SC-001`, `SC-002`, ...

Downstream artifacts must reference upstream identifiers rather than restating them without linkage.

## TASK Contract

The TASK defines the business request and its hard boundaries.

Every TASK must contain:

- source references
- explicit in-scope items
- explicit out-of-scope items
- a business-level scenario
- SMART business objectives
- business rules
- constraints
- assumptions
- open questions or blockers
- measurable definition-of-done items

The TASK must not contain user-story decomposition or implementation instructions.

## SPEC Contract

The SPEC translates the TASK into independently testable user stories and bounded requirements.

Every SPEC must contain:

- references to the TASK and TASK log
- scope baseline from the TASK
- prioritized user stories
- independent tests per story
- acceptance scenarios
- edge cases
- functional requirements
- non-functional requirements when relevant
- carried-forward business rules and constraints
- non-goals
- assumptions
- open questions or blockers
- a traceability matrix back to TASK identifiers
- measurable success criteria

The SPEC must not introduce implementation strategy, implementation files, or architecture decisions unless a repository rule explicitly requires them.

## PLAN Contract

The PLAN translates the approved SPEC into deterministic implementation work.

Every PLAN must contain:

- references to TASK, SPEC, and their logs
- scope baseline
- technical context
- story-to-implementation mapping
- file change contract
- implementation sequence
- data or interface contract changes when relevant
- validation matrix
- anti-drift checks
- risks and open questions
- readiness gate results

The PLAN must not authorize work outside the approved SPEC.

## Approval Gates

The following approvals are mandatory:

1. Approval before starting the SPEC stage
2. Approval before starting the PLAN stage
3. Approval before starting implementation

If approval is missing, stop.

## Change Control

If scope changes after a TASK is created:

1. Do not rewrite history in place to hide the change
2. Create a new TASK or explicitly record the scope change
3. Regenerate or update downstream artifacts so traceability remains valid
4. Re-run the approval gates

## Validation Gates

### TASK Gate

The TASK stage passes only when:

- the scope is explicit
- the request is traceable
- the scenario is coherent
- the objectives are measurable
- the definition of done is testable
- no blocking ambiguity remains hidden

### SPEC Gate

The SPEC stage passes only when:

- every in-scope TASK item is covered
- no out-of-scope TASK item is reintroduced
- every story is independently testable
- every requirement is traceable
- no blocking ambiguity remains hidden

### PLAN Gate

The PLAN stage passes only when:

- every planned change maps to approved SPEC items
- the expected files or artifact areas are explicit
- validation is defined for each requirement or story
- anti-drift checks are explicit
- no blocking question remains unresolved for implementation

## Failure Policy

Stop execution when:

- required inputs are missing
- traceability cannot be established
- an ambiguity would force inference
- scope is expanded without approval
- a required artifact or log is missing
- a downstream artifact contradicts an upstream artifact

## Final Rule

When there is a conflict between convenience and traceability, choose traceability.

