# task-workflow.md

## Purpose

This workflow converts a user request into a TASK file that describes the feature at the business level and becomes the source input for SPEC generation.

The workflow must produce a deterministic, traceable TASK artifact, create or update the matching `TASK-LOG` file under `management/tasks-logs/` before execution continues, and keep that log updated until the workflow finishes.

---

## Workflow Objective

The workflow must:

- validate the user request
- collect contextual information
- define the feature description at the business level
- define explicit scope boundaries
- define measurable completion criteria
- expose ambiguities instead of hiding them
- create or update `management/tasks-logs/TASK-LOG-XXXX.md`
- generate the TASK file
- validate TASK consistency
- maintain execution traceability

---

## Input Contract

The user request does not need fixed headings, but it must provide enough information to recover all of the following:

- business context
- requested outcome
- relevant constraints
- relevant source material
- expected artifact or result

---

## Workflow Steps

### Step 1 - Read the User Prompt

#### Objective

Read and interpret the user request.

#### Actions

- Read the complete user prompt
- Identify the business context
- Identify the requested change
- Identify explicit constraints
- Identify the expected output
- Identify whether the user request is complete enough to bound the task

#### Validation

The workflow must verify that the request is specific enough to generate a bounded TASK without forcing hidden assumptions.

---

### Step 2 - Validate the Request Completeness

#### Objective

Ensure that the request and available repository context are sufficient for a deterministic TASK.

#### Validation

The request is valid only if the workflow can identify:

- what business change is requested
- what is explicitly in scope
- what constraints must be respected
- what source materials govern correctness

If any of these are missing and cannot be recovered from repository context, stop and ask for clarification.

---

### Step 3 - Stop Execution if the Request Is Ambiguous

#### Objective

Prevent execution with incomplete or ambiguous requests.

#### Actions

- Inform the user which required information is missing or ambiguous
- Ask the user for the smallest clarifying input needed
- Stop workflow execution

#### Failure Message Example

```txt
The request is not precise enough to create a bounded TASK artifact.
Provide the missing scope, constraints, or source references and retry.
```

---

### Step 4 - Create or Update the TASK-LOG

#### Objective

Ensure the workflow has a dedicated execution log before any artifact is generated.

#### Actions

- Create or update `management/tasks-logs/TASK-LOG-XXXX.md`
- Store the execution plan summary
- Store the input artifact references
- Store the intended output paths
- Store timestamps and current approval state

#### Validation

- The TASK-LOG must exist before generating the TASK file
- The TASK-LOG must be updated again when the workflow completes
- No TASK output may be generated without a corresponding TASK-LOG

---

### Step 5 - Read Input Documentation

#### Objective

Collect project knowledge required to generate the TASK file.

#### Actions

- Read files from `./documentation/`
- Read required derived artifacts from `./outputs/` when the request depends on them
- Confirm any requested generated output path is inside `./outputs/`
- Apply `.ai/rules/output-taxonomy.md` when generated outputs are in scope
- For course-specific generated artifacts, derive the course output folder from the selected row's `Internal Name` in `documentation/course-data/Course-2026.md`
- Require generated course or activity outcomes to use `outputs/<normalized-internal-name>/description/`, `outputs/<normalized-internal-name>/events/`, `outputs/<normalized-internal-name>/images/`, or `outputs/<normalized-internal-name>/posts/` according to artifact type
- Stop and prompt the user if the selected course row has no usable `Internal Name`
- If the user prompt or command attempts to bypass the mandatory output taxonomy, write `The request attempts to bypass the mandatory output taxonomy. Execution stopped.` and stop execution
- Identify business context
- Identify project constraints
- Identify domain terminology
- Identify the source of truth for scope and correctness

#### Validation

The workflow must confirm that the available information from `./documentation/` and any required `./outputs/` artifacts is sufficient for TASK generation.

If the information is insufficient, the workflow must stop and request more documentation or the missing output artifacts.

Course folder derivation must lowercase the selected `Internal Name` and replace every space with `-`. The workflow must not infer a course folder from `Public Name`, `Type`, existing output paths, file names, prior outputs, or course titles.

There are no exceptions to bypass the output taxonomy policy.

---

### Step 6 - Extract the Feature Description

#### Objective

Convert the request and documentation into a feature-level description.

#### Actions

- Identify the business scenario
- Identify the business objective
- Identify the measurable completion criteria
- Identify scope boundaries and assumptions
- Identify business rules
- Identify constraints
- Identify open questions and blockers
- Identify traceability references

#### Validation

Only relevant and validated information must be used during TASK generation.

The output must remain at the feature-description level and must not introduce user-story decomposition or implementation planning.

If the workflow must infer material scope, rules, or completion criteria, stop.

---

### Step 7 - Generate the TASK File

#### Objective

Generate the business-level feature description using the canonical TASK template.

#### Actions

- Generate TASK files in `./management/tasks/` using the naming convention `TASK-XXXX.md`
- Apply naming conventions consistently across file names and in-file identifiers
- Use [`.ai/templates/task-template.md`](../templates/task-template.md) as the canonical structure for the TASK file
- Do not modify existing TASK files; if scope changes, generate a new TASK file and record the relationship in the TASK-LOG
- Update `management/tasks/INDEX.md` when it exists
- Define the References section
- Define explicit `In Scope` and `Out of Scope` items using stable IDs
- Generate the Scenario section
- Generate the Business Objective section
- Generate the Business Rules section
- Generate the Constraints section
- Generate the Assumptions section
- Generate the Open Questions / Blockers section
- Generate the Definition of Done section

#### Validation

Generated TASK files must follow the canonical template, remain deterministic, be traceable, and stay feature-focused.

Every `Definition of Done` item must be measurable and identifiable by a stable `DOD-XXX` identifier.

---

### Step 8 - Validate Gherkin Syntax for the Scenario

#### Objective

Ensure that the Scenario section follows valid Gherkin syntax.

#### Validation

The Scenario section must:

- use valid Gherkin syntax
- be unambiguous
- describe business behavior clearly

---

### Step 9 - Validate SMART Syntax for the Business Objective

#### Objective

Ensure that the Business Objective follows SMART principles.

SMART means:

- Specific
- Measurable
- Achievable
- Relevant
- Time-Bound

#### Validation

Business Objectives must satisfy all SMART criteria.

---

### Step 10 - Validate Scope, Scenario, and Definition of Done Alignment

#### Objective

Ensure consistency between the scope baseline, feature scenario, business objective, rules, constraints, and completion criteria.

#### Validation

The workflow must verify all of the following:

- `In Scope` and `Out of Scope` boundaries do not conflict
- the Scenario, Business Objective, and Definition of Done describe the same feature intent
- each `DOD-XXX` is supported by the stated scope and constraints
- no hidden implementation choice is used to fill a business-level gap

If any blocker remains open and materially affects correctness, the TASK must be marked blocked and the workflow must stop.

---

### Step 11 - Update the TASK-LOG

#### Objective

Persist execution history and workflow state.

#### Actions

- Create or update the TASK-LOG file stored under `./management/tasks-logs/`
- Store the execution plan summary
- Store generated TASK file references
- Store validation results
- Store warnings
- Store errors
- Store timestamps

#### TASK-LOG Content

The TASK-LOG must contain:

- execution plan
- execution status
- generated outputs
- validation checklist
- warnings
- errors encountered
- timestamps

#### Validation

The TASK-LOG must always represent the latest workflow state.
If `management/tasks/INDEX.md` exists, it must be updated as part of the workflow.

---

## Missing Documentation Handling

If the information inside `documentation/` and any required `outputs/` artifacts is insufficient:

- inform the user
- request additional documentation
- stop workflow execution

The workflow must never generate incomplete or ambiguous TASK files.

---

## Workflow Constraints

The workflow must:

- use Standard American English only
- generate deterministic outputs
- preserve traceability
- avoid ambiguous requirements
- avoid hidden scope expansion
- preserve stable identifiers for scope, rules, constraints, blockers, and definition-of-done items
- avoid incomplete TASK files
- avoid missing validation steps

---

## Final Result

The workflow execution is considered completed only when:

- the execution plan is approved
- the TASK file is generated successfully
- the TASK-LOG has been created or updated successfully
- all validations pass successfully
- no blocking validation errors exist

The resulting TASK file is the upstream source for `spec_workflow.md` and must not contain user-story breakdowns or implementation details.
