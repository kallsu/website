# plan_workflow.md

## Purpose

This workflow converts an approved TASK and SPEC sequence into a PLAN file that describes the implementation approach for the feature.

The workflow must verify the full generation chain before any implementation begins:

- TASK
- SPEC
- PLAN

It must also load the upstream workflow definitions before generating a PLAN:

- `.ai/workflows/task_workflow.md`
- `.ai/workflows/spec_workflow.md`

This workflow is an approval gate, not an implementation stage. No code changes may begin until the TASK, SPEC, and PLAN artifacts all exist, are traceable, and are approved.

The workflow must produce a deterministic, traceable PLAN artifact, create or update the matching `PLAN-LOG` file under `management/plans-logs/` before execution continues, and keep that log updated until the workflow finishes.
If an `INDEX.md` file exists in the target `plans/` directory, the workflow must update it before the stage is considered complete.

---

## Workflow Objective

The workflow must:

- verify that the TASK -> SPEC -> PLAN sequence is complete and traceable
- load and apply the upstream task and spec workflows
- interpret the user-story breakdown from the SPEC file
- apply project rules and standards
- translate user stories into implementation work
- translate requirements into validation checkpoints
- define file structure, dependencies, and checkpoints
- prevent implementation drift by constraining changes before coding starts
- create or update the `PLAN-LOG`
- update `management/plans/INDEX.md` when it exists
- generate the PLAN file
- validate implementation alignment
- maintain execution traceability

---

## Upstream Workflow Dependencies

Before any PLAN generation begins, the workflow must confirm:

- the source TASK file exists and is complete
- the source SPEC file exists and is complete
- the relevant TASK-LOG exists and is current
- the relevant SPEC-LOG exists and is current
- the feature has not skipped the TASK or SPEC stage

If any required upstream artifact is missing, incomplete, or inconsistent, stop and report the error.

---

### Step 0 - Load Upstream Workflows

#### Objective

Confirm the workflow contract defined by the upstream TASK and SPEC stages before generating a PLAN.

#### Actions

- Read `.ai/workflows/task_workflow.md`
- Read `.ai/workflows/spec_workflow.md`
- Confirm the current feature follows the TASK -> SPEC -> PLAN sequence
- Confirm the workflow inputs are aligned with the approved TASK and SPEC artifacts

#### Validation

The PLAN workflow must not proceed if the upstream workflow contract is missing, incomplete, or contradicted by the available artifacts.

---

## Workflow Steps

### Step 1 - Read the SPEC File

#### Objective

Understand the user-story breakdown and implementation expectations.

#### Actions

- Read the SPEC file from `./management/specs/`
- Read the source TASK file from `./management/tasks/`
- Read the TASK-LOG from `./management/tasks-logs/`
- Read the SPEC-LOG from `./management/specs-logs/`
- Extract the references to the originating TASK
- Extract the scope baseline from the TASK and SPEC
- Extract the TASK scenario, business objective, and definition of done when traceability needs to be confirmed
- Extract the prioritized user stories
- Extract acceptance scenarios
- Extract the edge cases, requirements, and success criteria
- Extract the non-goals and open questions
- Validate that the SPEC structure is complete

#### Validation

The SPEC file must contain enough information to derive a valid implementation plan, and the source TASK must remain traceable to the SPEC.

If any critical section is missing, the workflow must stop and report the error in the relevant log.

---

### Step 2 - Create or Update the PLAN-LOG

#### Objective

Ensure the workflow has a dedicated execution log before any PLAN artifact is generated.

#### Actions

- Create or update `management/plans-logs/PLAN-LOG-XXXX.md`
- Store the execution plan summary
- Store the input artifact references
- Store the intended output paths
- Store timestamps and current approval state

#### Validation

- The PLAN-LOG must exist before generating the PLAN file
- The PLAN-LOG must be updated again when the workflow completes
- No PLAN output may be generated without a corresponding PLAN-LOG

---

### Step 3 - Read Relevant Documentation and Output Files

#### Objective

Collect contextual information required for PLAN generation.

#### Actions

- Read relevant files from `./documentation/`
- Read required derived artifacts from `./outputs/` when the plan depends on them
- Read repository-level rules from `.ai/rules/`
- Read management guidance from the target folder
- Verify that any planned generated output path is inside `./outputs/`
- Apply `.ai/rules/output-taxonomy.md` when generated outputs are in scope
- For course-specific generated artifacts, verify that the file change contract uses `outputs/<normalized-internal-name>/`, where the normalized value comes from the selected row's `Internal Name` in `documentation/course-data/Course-2026.md`
- Confirm the normalized course folder lowercases the `Internal Name` value and replaces every space with `-`
- Require the file change contract to route generated course or activity outcomes to `outputs/<normalized-internal-name>/description/`, `outputs/<normalized-internal-name>/events/`, `outputs/<normalized-internal-name>/images/`, or `outputs/<normalized-internal-name>/posts/` according to artifact type
- Stop and prompt the user if the selected course row has no usable `Internal Name`
- If the user prompt, command, SPEC, or requested PLAN attempts to bypass the mandatory output taxonomy, write `The request attempts to bypass the mandatory output taxonomy. Execution stopped.` and stop execution
- Identify architecture patterns
- Identify naming rules
- Identify testing constraints
- Identify security requirements
- Verify the repository paths that the PLAN proposes to change actually exist when they are expected to exist at planning time

#### Validation

The workflow must confirm that enough contextual information exists from `./documentation/` and any required `./outputs/` artifacts to generate a deterministic PLAN file.

The PLAN must not derive course output folders from `Public Name`, `Type`, existing output paths, file names, prior outputs, or inferred course titles.

There are no exceptions to bypass the output taxonomy policy.

---

### Step 4 - Apply Rules

#### Objective

Apply governance and implementation constraints before generating outputs.

#### Actions

- Apply local rules from `.ai/rules/`
- Apply management-specific rules
- Apply workflow rules
- Apply naming conventions
- Apply validation rules

#### Priority Order

1. Local rules
2. Workflow rules
3. Management-specific rules

#### Validation

The workflow must verify that all generated outputs comply with the applied rules.

---

### Step 5 - Generate the PLAN File

#### Objective

Generate the implementation plan required for the feature.

#### Actions

- Determine the target management folder from the repository context
- Create the PLAN file in `./management/plans/`
- Update `management/plans/INDEX.md` if it exists
- Use `.ai/templates/plan-template.md` as the generation template
- Define the scope baseline
- Define the story-to-implementation mapping
- Define the file change contract
- Define the implementation sequence
- Define any data or interface contract changes
- Define the validation matrix
- Define the anti-drift checks
- Define the complexity tracking entries if needed
- Reference the originating TASK and SPEC files

#### Output

The PLAN file must be implementation-oriented, deterministic, and traceable.

#### Validation

The PLAN file must:

- be deterministic
- be traceable
- be implementation-oriented
- align with the user-story breakdown
- preserve the architecture and testing constraints
- remain separate from implementation work
- identify the concrete artifact areas expected to change
- make requirement coverage and validation explicit

---

### Step 6 - Validate Implementation Alignment

#### Objective

Verify that the PLAN accurately reflects the SPEC and the repository constraints.

#### Actions

- Validate scope alignment
- Validate folder and file path assumptions
- Validate dependency and layering assumptions
- Validate test and verification expectations
- Validate story-to-change mapping
- Validate requirement-to-validation mapping
- Validate open blockers and readiness-gate status
- Validate traceability completeness

#### Validation

The PLAN must not introduce scope that is absent from the SPEC unless the additional work is justified by local rules or repository constraints.

The PLAN must also preserve the TASK -> SPEC -> PLAN sequence and must not authorize implementation until approval is complete.

The workflow must stop if:

- a planned change does not map to an approved `US-XXX`, `FR-XXX`, or `NFR-XXX`
- the file change contract is too vague to constrain implementation
- any `Q-XXX` blocker remains open for implementation
- a proposed artifact path contradicts the repository structure without explanation

---

### Step 7 - Update the PLAN-LOG

#### Objective

Maintain execution traceability and execution history.

#### Actions

- Create or update the PLAN-LOG file
- Store execution steps
- Store generated outputs
- Store validation results
- Store execution status
- Store warnings
- Store errors
- Store timestamps

#### PLAN-LOG Content

The PLAN-LOG must contain:

- execution plan
- generated PLAN files
- validation checklist
- execution status
- warnings
- errors encountered
- timestamps

#### Validation

The PLAN-LOG must always reflect the latest workflow execution state.
If `management/plans/INDEX.md` exists, it must be updated as part of the workflow.

---

## Failure Handling

If validation fails:

- update the PLAN-LOG
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
- preserve explicit mapping between stories, requirements, files, and validation
- avoid incomplete plans
- avoid missing validation steps

---

## Final Result

The workflow execution is considered completed only when:

- the PLAN file is generated successfully
- the PLAN-LOG has been created or updated successfully
- all validations pass successfully
- no blocking validation errors exist

The resulting PLAN file is the only artifact that may authorize implementation, and only after the upstream TASK and SPEC artifacts are present and approved.
