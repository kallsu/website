# Project AI Operating Instructions

This repository uses the `.ai` directory as the canonical source for AI-related project behavior.

Before starting any task, Codex must inspect and apply the relevant instructions, rules, workflows, skills, actions, and agent definitions stored under `.ai`.

## Mandatory Startup Procedure

At the beginning of every session and before executing the first user request:

1. Read this file completely.
2. Inspect `.ai/rules/` and apply all rules relevant to the current task.
3. Inspect `.ai/workflows/` and select the workflow that best matches the current task.
4. Inspect `.ai/actions/` and identify any reusable action that should be used.
5. Inspect `.ai/skills/` and load the skill instructions relevant to the current task.
6. Inspect `.ai/agents/` and use the appropriate custom agent definition when the task requires specialized reasoning.
7. If multiple instructions conflict, apply the precedence rules defined below.
8. Do not begin implementation until the applicable rules and workflow have been identified.

## Instruction Precedence

When instructions conflict, use the following order of priority:

1. System and platform instructions.
2. User instructions from the current conversation.
3. Repository-level instructions in `AGENTS.md`.
4. Rules in `.ai/rules/`.
5. Workflow instructions in `.ai/workflows/`.
6. Skill-specific instructions in `.ai/skills/`.
7. Action-specific instructions in `.ai/actions/`.
8. General project conventions and inferred patterns.

Never ignore a higher-priority instruction because of a lower-priority file.

## Repository AI Layout

The current `.ai` layout is:

```text
.ai/
├── .codex-state/
├── AGENTS.md
├── actions/
├── agents/
├── rules/
├── scripts/
├── skills/
├── templates/
├── tools/
└── workflows/
```

### `.ai/rules/`

Contains project rules, coding standards, architectural constraints, security requirements, naming conventions, review criteria, and other mandatory instructions.

Codex must treat these files as persistent project policy.

### `.ai/workflows/`

Contains step-by-step workflows for recurring work. The active repository workflows are:

- `content_chain_workflow.md`
- `task_workflow.md`
- `spec_workflow.md`
- `plan_workflow.md`

Codex must select the most relevant workflow before planning the task.

### `.ai/actions/`

Contains reusable operational actions, command recipes, checklists, or procedures.

The current repository action is `/sdd-pipeline`, defined in `.ai/actions/sdd-pipeline.md`.

### `.ai/skills/`

Contains project-specific skills.

When a skill appears relevant, Codex must read its `SKILL.md` before using it.

Expected structure:

```text
.ai/skills/<skill-name>/SKILL.md
```

### `.ai/agents/`

Contains project custom-agent source definitions.

Each `*.toml` file under `.ai/agents/` defines one custom agent and must use the OpenAI custom-agent schema:

```toml
name = "agent-name"
description = "Human-facing guidance for when to use this agent."
developer_instructions = """
Core behavior instructions for the agent.
"""
```

The `name` field is the source of truth for the custom agent identity. Keep filenames aligned with the agent name unless there is a documented reason not to.

### `.ai/templates/`

Contains canonical templates used by repository workflows, including TASK, SPEC, and PLAN templates.

### `.ai/scripts/`

Contains repository automation scripts used to bootstrap, validate, or synchronize AI artifacts.

## Generated Runtime Mirrors

This repository materializes selected `.ai` content into Codex-compatible runtime locations:

```text
.agents/
.codex/
AGENTS.md
```

Current generated layout:

```text
.agents/
└── skills/

.codex/
├── agents/
└── rules/
```

The canonical source remains `.ai`.

Do not assume `.agents/`, `.codex/`, or root `AGENTS.md` are manually maintained unless project documentation explicitly says so.

When changing canonical files under `.ai`, keep generated runtime mirrors synchronized when the change is needed for the current Codex session to see the updated behavior. In particular, `.ai/agents/*.toml` should match the corresponding `.codex/agents/*.toml` runtime copy.

## Management Workflow Layout

The controlled SDLC artifacts live under `management/`:

```text
management/
├── AGENTS.md
├── ARTIFACT-REVIEW-CHECKLIST.md
├── plans/
├── plans-logs/
├── specs/
├── specs-logs/
├── tasks/
├── tasks-logs/
└── validate_artifacts.py
```

Repository workflow rules use this sequence:

```text
TASK -> SPEC -> PLAN -> Implementation
```

Use `.ai/rules/spec-driven-development.md`, `.ai/actions/sdd-pipeline.md`, and `management/AGENTS.md` when a request is part of the controlled SDLC artifact workflow.

## Default Operating Workflow

For every task:

1. Understand the user request.
2. Identify the relevant `.ai` rules, workflows, skills, actions, and agents.
3. Produce a concise plan unless the task is trivial.
4. Make the smallest safe change that satisfies the request.
5. Preserve existing project conventions.
6. Prefer editing existing files over creating unnecessary new files.
7. Run relevant checks or explain why they were not run.
8. Summarize what changed and mention any risks, assumptions, or follow-up work.

## Safety and Quality Rules

Codex must:

- avoid destructive operations unless explicitly requested;
- avoid deleting user work without confirmation;
- avoid broad rewrites when a targeted edit is sufficient;
- preserve formatting and style where possible;
- keep changes scoped to the current task;
- call out uncertainty instead of guessing;
- prefer explicit project instructions over generic best practices;
- avoid introducing new dependencies unless justified;
- avoid exposing secrets, credentials, tokens, or private configuration.

## Missing Files

If a referenced `.ai` directory or file does not exist, Codex should continue gracefully and use the available instructions.

Do not fail a task only because an optional `.ai` subdirectory is missing.

## Final Response Expectations

When completing a task, Codex should report:

- what changed;
- which checks were run;
- any assumptions made;
- any important limitations or next steps.

Keep responses concise and practical.
