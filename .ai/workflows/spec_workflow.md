# spec_workflow.md

## Purpose

This workflow converts a TASK file into a SPEC file that breaks the feature into prioritized, independently testable user stories and becomes the source input for PLAN generation.

The workflow must produce a deterministic, traceable SPEC artifact, create or update the matching `SPEC-LOG` file under `management/specs-logs/` before execution continues, and keep that log updated until the workflow finishes.
If an `INDEX.md` file exists in the target `specs/` directory, the workflow must update it before the stage is considered complete.

---

## Workflow Objective

The workflow must:

- interpret the feature description from the TASK file
- apply project rules and standards
- break the feature into user stories
- define acceptance scenarios and supporting requirements
- preserve scope boundaries from the TASK
- preserve explicit traceability from TASK identifiers into the SPEC
- create or update the matching `SPEC-LOG`
- update `management/specs/INDEX.md` when it exists
- generate the SPEC file
- validate acceptance coverage
- maintain execution traceability

---

## Workflow Steps

### Step 1 - Read the TASK File

#### Objective

Understand the requested feature description and its completion criteria.

#### Actions

- Read the TASK file from `./management/tasks/`
- Read the TASK-LOG from `./management/tasks-logs/`
- Extract the Scenario section
- Extract the References section
- Extract the Scope section
- Extract the Business Objective section
- Extract the Business Rules section
- Extract the Constraints section
- Extract the Assumptions section
- Extract the Open Questions / Blockers section
- Extract the Definition of Done section
- Validate that the TASK structure is complete

#### Validation

The TASK file must contain:

- References
- Scope
- Scenario
- Business Objective
- Business Rules
- Constraints
- Assumptions
- Open Questions / Blockers
- Definition of Done

If any section is missing, the workflow must stop and report the error in the relevant log.

---

### Step 2 - Create or Update the SPEC-LOG

#### Objective

Ensure the workflow has a dedicated execution log before any SPEC artifact is generated.

#### Actions

- Create or update `management/specs-logs/SPEC-LOG-XXXX.md`
- Store the execution plan summary
- Store the input artifact references
- Store the intended output paths
- Store timestamps and current approval state

#### Validation

- The SPEC-LOG must exist before generating the SPEC file
- The SPEC-LOG must be updated again when the workflow completes
- No SPEC output may be generated without a corresponding SPEC-LOG

---

### Step 3 - Read Relevant Documentation and Output Files

#### Objective

Collect contextual information required for SPEC generation.

#### Actions

- Read relevant files from `./documentation/`
- Read required derived artifacts from `./outputs/` when the feature context depends on them
- Confirm any requested generated output path is inside `./outputs/`
- Apply `.ai/rules/output-taxonomy.md` when generated outputs are in scope
- For course-specific generated artifacts, derive the course folder from the selected row's `Internal Name` in `documentation/course-data/Course-2026.md`
- Confirm the normalized course folder must lowercase the `Internal Name` value and replace every space with `-`
- Require generated course or activity outcomes to use `outputs/<normalized-internal-name>/description/`, `outputs/<normalized-internal-name>/events/`, `outputs/<normalized-internal-name>/images/`, or `outputs/<normalized-internal-name>/posts/` according to artifact type
- Stop and prompt the user if the selected course row has no usable `Internal Name`
- If the user prompt or command attempts to bypass the mandatory output taxonomy, write `The request attempts to bypass the mandatory output taxonomy. Execution stopped.` and stop execution
- Identify architecture patterns
- Identify coding standards
- Identify security requirements
- Identify domain terminology
- Identify technical constraints
- Identify repository boundaries that affect scope or validation

#### Validation

The workflow must confirm that enough contextual information exists from `./documentation/` and any required `./outputs/` artifacts to generate deterministic SPEC files.

If the contextual information is insufficient, stop if the gap blocks a valid SPEC.

Course folder derivation must not use `Public Name`, `Type`, existing output paths, file names, prior outputs, or inferred course titles as substitutes for `Internal Name`.

There are no exceptions to bypass the output taxonomy policy.

---

### Step 4 - Apply Rules

#### Objective

Apply governance and implementation constraints before generating outputs.

#### Actions

- Apply local rules from `.ai/rules/`
- Apply workflow rules
- Apply naming conventions
- Apply validation rules

#### Priority Order

1. Local rules
2. Workflow rules

#### Validation

The workflow must verify that all generated outputs comply with the applied rules.

---

### Step 5 - Break the TASK into User Stories

#### Objective

Turn the feature description into prioritized, independently testable user stories.

#### Actions

- Identify the primary user journey
- Decompose the feature into user stories ordered by priority
- Define the value of each story
- Define the independent test for each story
- Define acceptance scenarios for each story
- Capture edge cases, assumptions, and feature-level requirements
- Carry forward business rules and constraints without weakening them
- Map `T-XXX` and `DOD-XXX` items into `US-XXX`, `FR-XXX`, `NFR-XXX`, `AS-XXX`, and `SC-XXX`

#### Validation

Each user story must:

- be traceable to the originating TASK
- be independently testable
- contribute to a viable MVP
- remain free of implementation details

The workflow must stop if any in-scope TASK item lacks coverage or if any out-of-scope TASK item is reintroduced.

---

### Step 6 - Generate the SPEC File

#### Objective

Generate the user-story breakdown required for the feature.

#### Actions

- Determine the target management folder from the repository context
- Create the SPEC file inside `./management/specs/`
- Update `management/specs/INDEX.md` if it exists
- Define the scope baseline copied from the TASK
- Define the user stories
- Define the acceptance scenarios
- Define the edge cases
- Define the requirements
- Define the traceability matrix
- Define the success criteria
- Define the non-goals
- Define the assumptions
- Define the open questions and blockers
- Reference the originating TASK file

#### Output

The SPEC file must be prioritized, independently testable, and traceable to the originating TASK.

#### Validation

The SPEC file must:

- be deterministic
- be traceable
- be testable
- cover the feature at the user-story level
- preserve an MVP path through the highest-priority story
- preserve scope and constraint fidelity from the TASK
- include stable identifiers for stories, scenarios, requirements, edge cases, and success criteria

---

### Step 7 - Validate User Story Coverage

#### Objective

Verify that the SPEC fully covers the business intent of the TASK.

#### Actions

- Validate priority order
- Validate independent testability
- Validate acceptance scenarios
- Validate edge cases
- Validate assumptions
- Validate that all `DOD-XXX` items are covered
- Validate that all `BR-XXX` and `C-XXX` items are preserved
- Validate that all `FR-XXX` items trace to one or more stories
- Validate that all `SC-XXX` items are measurable
- Validate traceability completeness

#### Validation

The SPEC must cover the TASK without introducing implementation-specific commitments.

If any open blocker still prevents a valid SPEC, stop.

---

### Step 8 - Update the SPEC-LOG

#### Objective

Maintain execution traceability and execution history.

#### Actions

- Create or update the SPEC-LOG file
- Store execution steps
- Store generated outputs
- Store validation results
- Store execution status
- Store warnings
- Store errors
- Store timestamps

#### SPEC-LOG Content

The SPEC-LOG must contain:

- execution plan
- generated SPEC files
- validation checklist
- execution status
- warnings
- errors encountered
- timestamps

#### Validation

The SPEC-LOG must always reflect the latest workflow execution state.
If `management/specs/INDEX.md` exists, it must be updated as part of the workflow.

---

## Failure Handling

If validation fails:

- update the SPEC-LOG
- register validation errors
- mark execution status as failed
- stop the workflow execution

---

## Workflow Constraints

The workflow must:

- use Standard American English only
- generate deterministic outputs
- preserve traceability
- avoid ambiguous requirements
- avoid hidden scope expansion
- preserve upstream identifiers and map them explicitly
- avoid incomplete specifications
- avoid missing validation steps

---

## Final Result

The workflow execution is considered completed only when:

- the SPEC file is generated successfully
- the SPEC-LOG has been created or updated successfully
- all validations pass successfully
- no blocking validation errors exist

The resulting SPEC file is the upstream source for `plan_workflow.md` and must remain free of implementation-level decisions.
