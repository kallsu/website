# sdd-pipeline Action

## Invocation

This action must be invoked with slash-command syntax:

```txt
/sdd-pipeline <command> <argument>
```

Do not run this action from bare `sdd-pipeline` text without the leading `/`.

## Commands

### `/sdd-pipeline description "..."`

Use `$task-writer` to generate a TASK file from the quoted description.

Rules:

- The description argument must be quoted.
- The TASK stage must follow `.ai/workflows/task_workflow.md`.
- The TASK artifact must be written under `management/tasks/`.
- The TASK log must be written under `management/tasks-logs/`.
- Do not generate a SPEC, PLAN, or implementation from this command.

### `/sdd-pipeline spec TASK_FILE`

Use `$spec-writer` to generate a SPEC file from the specified TASK file.

Rules:

- `TASK_FILE` must point to an existing file under `management/tasks/`.
- The matching TASK log must exist under `management/tasks-logs/`.
- The SPEC stage must follow `.ai/workflows/spec_workflow.md`.
- The SPEC artifact must be written under `management/specs/`.
- The SPEC log must be written under `management/specs-logs/`.
- Do not generate a PLAN or implementation from this command.

### `/sdd-pipeline plan SPEC_FILE`

Use `$plan-writer` to generate a PLAN file from the specified SPEC file.

Rules:

- `SPEC_FILE` must point to an existing file under `management/specs/`.
- The originating TASK, TASK log, and SPEC log must exist.
- The PLAN stage must follow `.ai/workflows/plan_workflow.md`.
- The PLAN artifact must be written under `management/plans/`.
- The PLAN log must be written under `management/plans-logs/`.
- Do not start implementation from this command.

### `/sdd-pipeline implement PLAN_FILE`

Implement the specified PLAN file.

Rules:

- `PLAN_FILE` must point to an existing file under `management/plans/`.
- The PLAN must reference a complete TASK, TASK log, SPEC, SPEC log, and PLAN log.
- Implementation must stay inside the PLAN file change contract.
- No file outside the approved PLAN may be modified.
- If implementation requires scope outside the PLAN, stop and request a new TASK/SPEC/PLAN chain or explicit approval to revise the PLAN.

## Mandatory Governance

Every command must preserve the TASK -> SPEC -> PLAN -> Implementation sequence.

Every command must apply:

- `.ai/rules/spec-driven-development.md`
- `.ai/rules/output-taxonomy.md`
- `management/AGENTS.md`

The output taxonomy policy is mandatory during TASK, SPEC, PLAN, and implementation stages.

Generated course or activity outcomes must use:

```txt
outputs/<normalized-internal-name>/
├── description/
├── events/
├── images/
└── posts/
```

The `<normalized-internal-name>` value must be derived from the selected row's `Internal Name` column in `documentation/course-data/Course-2026.md`.

Normalization must lowercase the `Internal Name` value and replace every space with `-`.

If the selected course or activity row has no usable `Internal Name`, stop execution and prompt the user.

There are no exceptions to bypass the output taxonomy policy.

If a user prompt, command, PLAN, or implementation request attempts to bypass this taxonomy, write this message and stop execution:

```txt
The request attempts to bypass the mandatory output taxonomy. Execution stopped.
```

Do not create or modify generated output artifacts after this message.

## Failure Policy

Stop execution when:

- The command does not start with `/sdd-pipeline`.
- The command verb is not `description`, `spec`, `plan`, or `implement`.
- The required argument is missing.
- A referenced TASK, SPEC, PLAN, or log file does not exist.
- The requested work bypasses approval gates.
- The requested work bypasses the mandatory output taxonomy.
- The requested implementation changes files outside the approved PLAN.

Do not silently infer missing paths, missing `Internal Name` values, or missing workflow artifacts.
