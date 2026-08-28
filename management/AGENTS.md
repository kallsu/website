# AGENTS.md

## Purpose

This folder contains the management artifacts that drive the controlled TASK -> SPEC -> PLAN workflow for the repository.

The agent operating inside this folder is responsible for:

- Reading project documentation
- Reading generated output artifacts when they are needed for traceability
- Interpreting TASK files as feature descriptions
- Generating SPEC files as user-story breakdowns
- Generating PLAN files as implementation plans
- Tracking execution logs
- Maintaining session records
- Following the defined workflows (`task_workflow`, then `spec_workflow`, then `plan_workflow`)
- Applying repo-level rules, skills, tools, and workflows
- Preventing requirement drift through explicit traceability and approval gates

---

# Folder Structure

```txt
repo-root/
├── .agents/
│   └── skills/
├── .ai/
│   ├── actions/
│   ├── agents/
│   ├── rules/
│   ├── scripts/
│   ├── skills/
│   ├── templates/
│   └── workflows/
├── .codex/
│   ├── agents/
│   └── rules/
├── apps/
│   └── backend-dotnet/
│       ├── src/
│       ├── It.Ggo.MaRLP.slnx
│       └── README.md
├── AGENTS.md
└── management/
│   ├── AGENTS.md
│   ├── ARTIFACT-REVIEW-CHECKLIST.md
│   ├── validate_artifacts.py
│   ├── plans/
│   ├── plans-logs/
│   ├── specs/
│   ├── specs-logs/
│   ├── tasks/
│   └── tasks-logs/
```

---

# Responsibilities

The agent must:

1. Create or update the relevant TASK-LOG before starting any workflow stage
2. Execute the [task_workflow](../.ai/workflows/task_workflow.md) first to generate TASK files as feature descriptions
3. Store TASK execution details inside [tasks-logs/](./tasks-logs), whose canonical repository path is `management/tasks-logs/`
4. After `task_workflow` completes, request explicit user approval before starting [spec_workflow](../.ai/workflows/spec_workflow.md)
5. Create or update the relevant SPEC-LOG before starting the spec stage
6. Execute the [spec_workflow](../.ai/workflows/spec_workflow.md) second to generate SPEC files as user-story breakdowns
7. Store SPEC execution details inside [specs-logs/](./specs-logs)
8. After `spec_workflow` completes, request explicit user approval before starting [plan_workflow](../.ai/workflows/plan_workflow.md)
9. Create or update the relevant PLAN-LOG before starting the plan stage
10. Execute the [plan_workflow](../.ai/workflows/plan_workflow.md) third to generate PLAN files as implementation plans
11. Store PLAN execution details inside [plans-logs/](./plans-logs)
12. Maintain traceability between TASK, SPEC, PLAN, the log files, referenced documentation, and relevant output artifacts
13. Stop execution when ambiguity would force hidden assumptions
14. Preserve explicit identifiers and scope boundaries across all three stages

---

# Folder Definitions

## documentation/

Contains unstructured and structured project information and source inputs.

Examples:

- business notes
- architecture notes
- technical decisions
- meeting notes
- requirements
- domain knowledge
- architecture patterns
- coding standards
- security policies
- course data
- content notes
- project indexes

Key files and folders:

- `assets/`
- `course-data/`
- `INDEX.md`
- `registration-form-changes.md`

The agent must use these files as contextual memory during workflow execution.

Legacy compatibility folders `plan-logs/` and `spec-logs/` may still exist, but new logs must be written to `plans-logs/` and `specs-logs/`.

---

## outputs/

Contains all generated course outcomes and related derived artifacts.

These files are output artifacts, not source inputs.

All output generation must follow [output-taxonomy.md](../.ai/rules/output-taxonomy.md).

Generated artifacts must always remain inside `outputs/`.

Each course or activity outcome must have a dedicated folder at `outputs/<sequence-number>-<normalized-internal-name>/`.

Each course or activity folder must use this internal structure:

```txt
outputs/<sequence-number>-<normalized-internal-name>/
├── description/
├── events/
├── images/
└── posts/
```

Folder purposes:

- `description/`: course or activity descriptions.
- `events/`: event-management outcomes.
- `images/`: images for the event and course or activity.
- `posts/`: social media posts.

The course folder name must be derived from the selected row's ordinal position and `Internal Name` column in `documentation/course-data/Course-2026.md`.

Folder normalization is deterministic:

1. Read the selected course row's ordinal position in `documentation/course-data/Course-2026.md`, excluding the header row.
2. Format the ordinal position as a two-digit `<sequence-number>` starting at `01`.
3. Read the selected course row's `Internal Name` value.
4. If the value is missing or blank, stop execution and prompt the user.
5. If the value is present, lowercase it and replace every space with `-`.
6. Use only `outputs/<sequence-number>-<normalized-internal-name>/` as the course or activity output folder.

Examples:

- first row with `Azure Fundamentals` -> `outputs/01-azure-fundamentals/`
- second row with `Azure AI Fundamentals` -> `outputs/02-azure-ai-fundamentals/`

Do not infer a course folder from `Public Name`, `Type`, existing output paths, file names, prior outputs, or course titles.

There are no exceptions to bypass this policy. If a user prompt, command, plan, or implementation request attempts to bypass it, write `The request attempts to bypass the mandatory output taxonomy. Execution stopped.` and stop execution.

## tasks/

Contains TASK files.

TASK files define the feature description.

TASK structure:

```markdown
# Task : TASK-0001

## References
Source request and source artifacts

## Scope
### In Scope
### Out of Scope

## Scenario
Gherkin description of the feature-level scenario

## Business Objective
Description of the business objective(s) using SMART syntax

## Business Rules
Rules that must remain true

## Constraints
Hard boundaries that implementation and specification must respect

## Assumptions
Conditions believed true at task time

## Open Questions / Blockers
Questions that require explicit tracking

## Definition of Done
Rigorous and objective completion criteria with stable identifiers
```

TASK files must focus on the business problem, expected behavior, and done criteria.

TASK file structure is defined by [TASK-template.md](../.ai/templates/task-template.md).

---

## tasks-logs/

Contains execution logs generated by the agent.

Every TASK execution must generate or update a dedicated TASK-LOG file.
The TASK-LOG must exist before the stage starts and be updated again when the stage finishes.
No TASK stage may complete without a corresponding TASK-LOG file.

TASK-LOG files must contain:

- execution plan summary
- generated outputs
- validation checklist
- execution status
- encountered errors
- warnings
- timestamps

---

# Workflow Rules

The workflow is governed by:

```txt
../.ai/workflows/task_workflow.md
../.ai/workflows/spec_workflow.md
../.ai/workflows/plan_workflow.md
```

The workflows define:

- prompt validation
- documentation review
- artifact generation
- approval gates
- validation steps
- traceability rules

The slash action for running the controlled sequence is defined in [sdd-pipeline.md](../.ai/actions/sdd-pipeline.md) and must be invoked as `/sdd-pipeline`.

Use [validate_artifacts.py](./validate_artifacts.py) for deterministic compliance checks and [ARTIFACT-REVIEW-CHECKLIST.md](./ARTIFACT-REVIEW-CHECKLIST.md) for human review when appropriate.

The agent must keep the three stage artifacts consistent:

- `TASK` = feature description
- `SPEC` = user-story breakdown
- `PLAN` = implementation plan
- `outputs` = generated course descriptions and derived artifacts

---

# SPEC File Rules

Generated SPEC files must follow this structure:

```markdown
# Feature Story Breakdown: [FEATURE NAME]

## References
- [TASK file](Link-to-the-TASK-file)

## Scope Baseline
Copied in-scope, out-of-scope, rules, and constraints from the TASK

## User Stories
### User Story 1 - [Title] (Priority: P1, ID: US-001)
...

## Requirements
`FR-XXX` and `NFR-XXX` items

## Traceability Matrix
Mapping from TASK identifiers to SPEC identifiers
```

The SPEC must be prioritized, independently testable, and traceable back to the originating TASK.

SPEC file structure is defined by [SPEC-template.md](../.ai/templates/spec-template.md).

---

# PLAN File Rules

Generated PLAN files must follow the implementation-plan structure required by the feature and repository context.

The PLAN must:

- reference the originating TASK and SPEC
- describe the implementation approach
- define the concrete file or artifact structure impacted by the change
- map user stories and requirements to implementation work
- map requirements to validation
- include validation and checkpoint expectations
- remain implementation-oriented and deterministic

PLAN file structure is defined by [PLAN-template.md](../.ai/templates/plan-template.md).

---

# Traceability Rules

The agent must maintain traceability between:

- TASK files
- SPEC files
- PLAN files
- TASK-LOG files
- SPEC-LOG files
- PLAN-LOG files
- referenced documentation
- relevant output artifacts

Every generated SPEC must reference the originating TASK file.
Every generated PLAN must reference the originating TASK and SPEC files.
Every workflow stage must also reference a corresponding log file.
Every downstream artifact must preserve upstream identifiers where they control scope, rules, constraints, blockers, or measurable outcomes.

---

# Agent Execution Rules

## Mandatory Workflow

The agent must always:

1. Read relevant documentation files
2. Apply repo-level rules
3. Create or update the relevant TASK-LOG before starting the task stage
4. Execute the [task_workflow](../.ai/workflows/task_workflow.md) to generate TASK files
5. Update the relevant TASK-LOG after the task stage completes
6. Ask the user to approve starting the [spec_workflow](../.ai/workflows/spec_workflow.md)
7. Create or update the relevant SPEC-LOG before starting the spec stage
8. Execute the [spec_workflow](../.ai/workflows/spec_workflow.md) to generate SPEC files
9. Update the relevant SPEC-LOG after the spec stage completes
10. Ask the user to approve starting the [plan_workflow](../.ai/workflows/plan_workflow.md)
11. Create or update the relevant PLAN-LOG before starting the plan stage
12. Execute the [plan_workflow](../.ai/workflows/plan_workflow.md) to generate PLAN files
13. Update the relevant PLAN-LOG after the plan stage completes
14. Validate feature-description, user-story, and implementation-plan alignment
15. Block implementation if any unresolved question still affects correctness or scope

---

# Validation Rules

Before considering the execution completed, the agent must validate:

- the input request contains enough context to create a bounded TASK without hidden assumptions
- sufficient information exists in `./documentation/` and any required `./outputs/` artifacts to generate a TASK
- the TASK contains explicit `In Scope` and `Out of Scope` sections
- the TASK Scenario uses valid Gherkin syntax
- Business Objectives satisfy SMART criteria
- the TASK Scenario, Business Objective, Rules, Constraints, and Definition of Done are aligned
- the SPEC contains prioritized, independently testable user stories
- the SPEC contains full coverage for TASK identifiers
- the PLAN is aligned with the SPEC and the repository structure
- the PLAN contains an explicit file change contract and validation matrix
- traceability completeness across TASK, SPEC, PLAN, and their log files

---

# Priority Rules

Priority order:

1. Repo-level `.ai/rules`
2. Repo-level `.ai/workflows`
3. Repo-level `.ai/skills`

---

# Naming Conventions

## TASK Files

```txt
TASK-XXXX.md
```

Example:

```txt
TASK-0001.md
```

---

## SPEC Files

```txt
SPEC-XXXX.md
```

Example:

```txt
SPEC-0001.md
```

---

## PLAN Files

```txt
PLAN-XXXX.md
```

Example:

```txt
PLAN-0001.md
```

---

## TASK-LOG Files

```txt
TASK-LOG-XXXX.md
```

Example:

```txt
TASK-LOG-0001.md
```

---

# Agent Constraints

The agent must:

- never modify existing TASK files; if scope changes, create a new TASK file and record the relationship in the TASK-LOG
- never leave the log files out of sync with the workflow outputs
- never delete logs
- never generate incomplete SPEC files
- never generate incomplete PLAN files
- never bypass validation steps
- never skip traceability references
- never introduce scope in a SPEC that is excluded by the TASK
- never introduce scope in a PLAN that is absent from the approved SPEC
- never hide ambiguity by silently inventing rules, assumptions, or implementation details

The agent must always generate deterministic and auditable outputs.

---

# Output Quality Rules

Generated artifacts must be:

- clear
- deterministic
- implementation-oriented
- testable
- traceable
- architecture-aligned
- security-aware
- scope-bounded
- ambiguity-resistant

Acceptance criteria must be measurable and objectively verifiable.

---

# Final Objective

Transform business-oriented TASK files into user-story SPECs and implementation PLANs through a controlled and traceable SDLC workflow.

# Output style

Always follow the rules in the `i-have-adhd` skill: action-first, numbered steps, no preamble, no closers, state restated each turn.
