# Output Taxonomy Policy

## Purpose

This policy defines the mandatory folder taxonomy for every generated course or activity outcome.

## Canonical Output Root

All generated course or activity outcomes must be written inside `outputs/`.

Course and activity outcomes must be written under `outputs/<sequence-number>-<normalized-internal-name>/`.

The `<sequence-number>` value must be the selected row's ordinal position in `documentation/course-data/Course-2026.md`, excluding the header row, formatted as two digits starting at `01`.

The `<normalized-internal-name>` value must be derived from the selected row's `Internal Name` column in `documentation/course-data/Course-2026.md`.

Do not infer a course folder from `Public Name`, `Type`, existing output paths, file names, prior artifacts, or course titles.

## Folder Normalization

Folder normalization is deterministic:

1. Read the selected course row's ordinal position in `documentation/course-data/Course-2026.md`, excluding the header row.
2. Format the ordinal position as a two-digit `<sequence-number>` starting at `01`.
3. Read the selected course row's `Internal Name` value.
4. If the value is missing or blank, stop execution and prompt the user.
5. If the value is present, lowercase it and replace every space with `-`.
6. Use only `outputs/<sequence-number>-<normalized-internal-name>/` as the course or activity output folder.

## Required Subfolders

When those outcome types are generated, each course or activity folder must contain the relevant internal folders:

- `description/`
- `events/`
- `images/`
- `posts/`

## Mandatory Workflow Enforcement

This policy applies during every stage of the repository workflow:

1. TASK
2. SPEC
3. PLAN
4. Implementation

Every TASK, SPEC, PLAN, and implementation must preserve this taxonomy when generated outputs are in scope.

There are no exceptions to bypass this policy.

If a user prompt, command, plan, or implementation request attempts to bypass this taxonomy, write this message and stop execution:

```txt
The request attempts to bypass the mandatory output taxonomy. Execution stopped.
```

Do not create or modify generated output artifacts after this message.
