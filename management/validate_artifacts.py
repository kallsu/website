#!/usr/bin/env python3
"""Validate TASK, SPEC, and PLAN artifacts for management compliance."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MANAGEMENT_DIR = REPO_ROOT / "management"
LEGACY_TASK_LOG_FRAGMENT = "management/" + "task" + "-logs"
CANONICAL_TASK_LOG_FRAGMENT = "management/tasks-logs"
DELETED_OUTPUT_FOLDER_FRAGMENT = "market" + "ing"

ACTIVE_GUIDANCE_FILES = [
    MANAGEMENT_DIR / "AGENTS.md",
    REPO_ROOT / ".ai" / "actions" / "sdd-pipeline.md",
    REPO_ROOT / ".ai" / "rules" / "output-taxonomy.md",
    REPO_ROOT / ".ai" / "rules" / "spec-driven-development.md",
    REPO_ROOT / ".ai" / "skills" / "task-writer" / "SKILL.md",
    REPO_ROOT / ".ai" / "skills" / "spec-writer" / "SKILL.md",
    REPO_ROOT / ".ai" / "skills" / "plan-writer" / "SKILL.md",
    REPO_ROOT / ".ai" / "workflows" / "task_workflow.md",
    REPO_ROOT / ".ai" / "workflows" / "spec_workflow.md",
    REPO_ROOT / ".ai" / "workflows" / "plan_workflow.md",
    REPO_ROOT / ".ai" / "templates" / "spec-template.md",
    REPO_ROOT / ".ai" / "templates" / "plan-template.md",
]

TASK_REQUIRED_HEADINGS = [
    "## References",
    "## Scope",
    "### In Scope",
    "### Out of Scope",
    "## Scenario",
    "## Business Objective",
    "## Business Rules",
    "## Constraints",
    "## Assumptions",
    "## Open Questions / Blockers",
    "## Definition of Done",
]

SPEC_REQUIRED_HEADINGS = [
    "## References",
    "## Scope Baseline *(mandatory)*",
    "### In Scope From TASK",
    "### Out of Scope From TASK",
    "### Carried-Forward Constraints",
    "### Carried-Forward Business Rules",
    "## User Scenarios & Testing *(mandatory)*",
    "### Edge Cases",
    "## Requirements *(mandatory)*",
    "### Functional Requirements",
    "## Traceability Matrix *(mandatory)*",
    "## Success Criteria *(mandatory)*",
    "## Non-Goals",
    "## Assumptions",
    "## Open Questions / Blockers",
]

PLAN_REQUIRED_HEADINGS = [
    "## Summary",
    "## Source Artifacts",
    "## Scope Baseline",
    "### In Scope",
    "### Out of Scope",
    "### Critical Requirements",
    "## Technical Context",
    "## Story to Implementation Mapping",
    "## File Change Contract",
    "## Implementation Sequence",
    "## Validation Matrix",
    "## Risks / Open Questions",
    "## Anti-Drift Checks",
    "## Readiness Gate",
    "## Readiness Check",
]

PLACEHOLDER_FRAGMENTS = [
    "TASK-XXXX",
    "SPEC-XXXX",
    "PLAN-XXXX",
    "[FEATURE NAME]",
    "[DATE]",
    "[Brief Title]",
    "[Question or blocker]",
    "[Specific capability]",
    "[Concrete implementation step]",
    "[path/to/file-or-folder]",
    "NEEDS CLARIFICATION",
    "| [item] | [reason] | [alternative] |",
]


@dataclass
class ValidationResult:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def ok(self) -> bool:
        return not self.errors


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_repo_path(raw_path: str) -> Path:
    cleaned = raw_path.strip().strip("`")
    if cleaned.startswith("/"):
        cleaned = cleaned[1:]
    return REPO_ROOT / cleaned.replace("/", "\\")


def ensure_file_exists(result: ValidationResult, raw_path: str, label: str) -> Path | None:
    path = normalize_repo_path(raw_path)
    if not path.exists():
        if label == "Referenced TASK-LOG" and LEGACY_TASK_LOG_FRAGMENT in raw_path.replace("\\", "/"):
            migrated_path = normalize_repo_path(
                raw_path.replace("\\", "/").replace(LEGACY_TASK_LOG_FRAGMENT, CANONICAL_TASK_LOG_FRAGMENT)
            )
            if migrated_path.exists():
                result.warning(
                    f"{label} uses legacy path but exists at migrated location: {raw_path}"
                )
                return migrated_path
        result.error(f"{label} does not exist: {raw_path}")
        return None
    return path


def extract_ids(text: str, pattern: str) -> list[str]:
    return re.findall(pattern, text)


def unique_ids(result: ValidationResult, ids: list[str], label: str) -> None:
    seen: set[str] = set()
    duplicates = sorted({item for item in ids if item in seen or seen.add(item)})  # type: ignore[arg-type]
    if duplicates:
        result.error(f"Duplicate {label} identifiers found: {', '.join(duplicates)}")


def parse_index_rows(index_path: Path, prefix: str) -> list[Path]:
    text = read_text(index_path)
    pattern = re.compile(
        rf"^\|\s*{prefix}-(\d+)\s*\|\s*\[([^\]]+)\]\(([^)]+)\)",
        re.MULTILINE,
    )
    paths: list[Path] = []
    for _, _, target in pattern.findall(text):
        paths.append((index_path.parent / target).resolve())
    return paths


def parse_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(heading)}\n(.*?)(?=^##\s|^###\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def parse_reference_path(text: str, label: str) -> str | None:
    pattern = re.compile(rf"- {re.escape(label)}: `([^`]+)`")
    match = pattern.search(text)
    return match.group(1) if match else None


def check_required_headings(result: ValidationResult, text: str, headings: list[str]) -> None:
    for heading in headings:
        if heading not in text:
            result.error(f"Missing required heading: {heading}")


def check_placeholders(result: ValidationResult, text: str) -> None:
    for fragment in PLACEHOLDER_FRAGMENTS:
        if fragment in text:
            result.error(f"Template placeholder still present: {fragment}")


def validate_task(path: Path) -> tuple[ValidationResult, dict[str, set[str]]]:
    text = read_text(path)
    result = ValidationResult(path)

    if not text.startswith("# Task : TASK-"):
        result.error("TASK title is missing or malformed")

    for required_line in ("**Input**:", "**Purpose**:"):
        if required_line not in text:
            result.error(f"Missing required metadata line: {required_line}")

    check_required_headings(result, text, TASK_REQUIRED_HEADINGS)
    check_placeholders(result, text)

    ids = {
        "scope_in": set(extract_ids(text, r"\*\*(T-\d{3})\*\*")),
        "scope_out": set(extract_ids(text, r"\*\*(T-OUT-\d{3})\*\*")),
        "business_rules": set(extract_ids(text, r"\*\*(BR-\d{3})\*\*")),
        "constraints": set(extract_ids(text, r"\*\*(C-\d{3})\*\*")),
        "assumptions": set(extract_ids(text, r"\*\*(A-\d{3})\*\*")),
        "questions": set(extract_ids(text, r"\*\*(Q-\d{3})\*\*")),
        "definition_of_done": set(extract_ids(text, r"\*\*(DOD-\d{3})\*\*")),
    }

    for label, values in ids.items():
        if not values:
            result.error(f"TASK is missing required identifiers for {label}")

    for label, values in ids.items():
        unique_ids(result, list(values), label)

    scenario = parse_section(text, "## Scenario")
    if not all(token in scenario for token in ("Given", "When", "Then")):
        result.error("Scenario does not contain Given / When / Then")

    blockers = parse_section(text, "## Open Questions / Blockers")
    if "Status:" not in blockers:
        result.error("Open Questions / Blockers section must include Status markers")

    return result, ids


def validate_spec(path: Path) -> tuple[ValidationResult, dict[str, set[str]]]:
    text = read_text(path)
    result = ValidationResult(path)

    if not text.startswith("# Feature Story Breakdown:"):
        result.error("SPEC title is missing or malformed")

    for required_line in ("**Feature Branch**:", "**Created**:", "**Status**:", "**Input**:", "**Purpose**:"):
        if required_line not in text:
            result.error(f"Missing required metadata line: {required_line}")

    check_required_headings(result, text, SPEC_REQUIRED_HEADINGS)
    check_placeholders(result, text)

    task_ref = parse_reference_path(text, "TASK file")
    task_log_ref = parse_reference_path(text, "TASK-LOG")
    spec_log_ref = parse_reference_path(text, "SPEC-LOG")

    task_path = ensure_file_exists(result, task_ref, "Referenced TASK file") if task_ref else None
    if task_ref is None:
        result.error("SPEC is missing TASK file reference")
    if task_log_ref is None:
        result.error("SPEC is missing TASK-LOG reference")
    else:
        ensure_file_exists(result, task_log_ref, "Referenced TASK-LOG")
    if spec_log_ref is None:
        result.error("SPEC is missing SPEC-LOG reference")
    else:
        ensure_file_exists(result, spec_log_ref, "Referenced SPEC-LOG")

    ids = {
        "stories": set(extract_ids(text, r"ID: (US-\d{3})\)")),
        "acceptance_scenarios": set(extract_ids(text, r"\*\*(AS-\d{3})\*\*:")),
        "edge_cases": set(extract_ids(text, r"\*\*(EC-\d{3})\*\*")),
        "functional_requirements": set(extract_ids(text, r"\*\*(FR-\d{3})\*\*")),
        "non_functional_requirements": set(extract_ids(text, r"\*\*(NFR-\d{3})\*\*")),
        "success_criteria": set(extract_ids(text, r"\*\*(SC-\d{3})\*\*")),
        "assumptions": set(extract_ids(text, r"\*\*(A-\d{3})\*\*")),
        "questions": set(extract_ids(text, r"\*\*(Q-\d{3})\*\*")),
    }

    mandatory_id_groups = ("stories", "acceptance_scenarios", "edge_cases", "functional_requirements", "success_criteria")
    for label in mandatory_id_groups:
        if not ids[label]:
            result.error(f"SPEC is missing required identifiers for {label}")

    for label, values in ids.items():
        unique_ids(result, list(values), label)

    matrix_section = parse_section(text, "## Traceability Matrix *(mandatory)*")
    matrix_ids = set(re.findall(r"`([A-Z-]+-\d{3})`", matrix_section))
    if not matrix_ids:
        result.error("SPEC traceability matrix is missing identifier entries")

    if task_path and task_path.exists():
        task_result, task_ids = validate_task(task_path)
        for _, upstream_ids in task_ids.items():
            missing = sorted(upstream_ids - matrix_ids)
            if missing:
                result.error(
                    "SPEC traceability matrix does not cover TASK identifiers: "
                    + ", ".join(missing)
                )
        if not task_result.ok:
            result.warning("Referenced TASK file has compliance errors; fix upstream artifact")

    open_questions = parse_section(text, "## Open Questions / Blockers")
    if open_questions and "Stage impact:" not in open_questions:
        result.error("SPEC blockers must include Stage impact markers")

    return result, ids


def validate_plan(path: Path) -> ValidationResult:
    text = read_text(path)
    result = ValidationResult(path)

    if not text.startswith("# Plan : PLAN-"):
        result.error("PLAN title is missing or malformed")

    for required_line in ("**Input**:", "**Traceability**:", "**Purpose**:"):
        if required_line not in text:
            result.error(f"Missing required metadata line: {required_line}")

    check_required_headings(result, text, PLAN_REQUIRED_HEADINGS)
    check_placeholders(result, text)

    for label in ("TASK file", "TASK-LOG", "SPEC file", "SPEC-LOG", "PLAN-LOG"):
        ref = parse_reference_path(text, label)
        if ref is None:
            result.error(f"PLAN is missing {label} reference")
        else:
            ensure_file_exists(result, ref, f"Referenced {label}")

    spec_ref = parse_reference_path(text, "SPEC file")
    spec_path = ensure_file_exists(result, spec_ref, "Referenced SPEC file") if spec_ref else None

    critical_requirements = set(extract_ids(text, r"`((?:FR|NFR)-\d{3})`"))
    if not critical_requirements:
        result.error("PLAN critical requirements are missing FR/NFR identifiers")

    readiness_gate = parse_section(text, "## Readiness Gate")
    if readiness_gate.count("- [x]") + readiness_gate.count("- [ ]") < 8:
        result.error("PLAN readiness gate is incomplete")

    file_change_contract = parse_section(text, "## File Change Contract")
    if "`" not in file_change_contract:
        result.error("PLAN file change contract does not identify concrete paths")

    validation_matrix = parse_section(text, "## Validation Matrix")
    if "|" not in validation_matrix:
        result.error("PLAN validation matrix is missing or malformed")

    if spec_path and spec_path.exists():
        spec_result, spec_ids = validate_spec(spec_path)
        missing_story_coverage = sorted(spec_ids["stories"] - set(extract_ids(text, r"`(US-\d{3})`")))
        if missing_story_coverage:
            result.error("PLAN does not reference all SPEC user stories: " + ", ".join(missing_story_coverage))

        missing_requirement_coverage = sorted(
            (spec_ids["functional_requirements"] | spec_ids["non_functional_requirements"]) - critical_requirements
        )
        if missing_requirement_coverage:
            result.error(
                "PLAN critical requirements do not cover SPEC FR/NFR identifiers: "
                + ", ".join(missing_requirement_coverage)
            )

        matrix_requirement_ids = set(extract_ids(validation_matrix, r"`((?:FR|NFR)-\d{3})`"))
        missing_validation_coverage = sorted(
            (spec_ids["functional_requirements"] | spec_ids["non_functional_requirements"]) - matrix_requirement_ids
        )
        if missing_validation_coverage:
            result.error(
                "PLAN validation matrix does not cover SPEC FR/NFR identifiers: "
                + ", ".join(missing_validation_coverage)
            )

        if not spec_result.ok:
            result.warning("Referenced SPEC file has compliance errors; fix upstream artifact")

    return result


def validate_active_guidance() -> ValidationResult:
    result = ValidationResult(MANAGEMENT_DIR / "active-guidance")

    for path in ACTIVE_GUIDANCE_FILES:
        if not path.exists():
            result.error(f"Active guidance file does not exist: {path.relative_to(REPO_ROOT)}")
            continue

        text = read_text(path)
        rel_path = path.relative_to(REPO_ROOT)
        normalized = text.replace("\\", "/")

        if LEGACY_TASK_LOG_FRAGMENT in normalized:
            result.error(f"Active guidance uses legacy TASK log path: {rel_path}")

        if DELETED_OUTPUT_FOLDER_FRAGMENT in normalized:
            result.error(f"Active guidance references deleted output folder: {rel_path}")

    task_log_guidance = [
        REPO_ROOT / ".ai" / "rules" / "spec-driven-development.md",
        REPO_ROOT / ".ai" / "skills" / "task-writer" / "SKILL.md",
        REPO_ROOT / ".ai" / "workflows" / "task_workflow.md",
        REPO_ROOT / ".ai" / "workflows" / "spec_workflow.md",
        REPO_ROOT / ".ai" / "workflows" / "plan_workflow.md",
        REPO_ROOT / ".ai" / "templates" / "spec-template.md",
        REPO_ROOT / ".ai" / "templates" / "plan-template.md",
        MANAGEMENT_DIR / "AGENTS.md",
    ]
    for path in task_log_guidance:
        if path.exists() and CANONICAL_TASK_LOG_FRAGMENT not in read_text(path).replace("\\", "/"):
            result.error(
                f"Active guidance is missing canonical TASK log path: {path.relative_to(REPO_ROOT)}"
            )

    output_guidance = [
        REPO_ROOT / ".ai" / "rules" / "output-taxonomy.md",
        REPO_ROOT / ".ai" / "rules" / "spec-driven-development.md",
        REPO_ROOT / ".ai" / "workflows" / "task_workflow.md",
        REPO_ROOT / ".ai" / "workflows" / "spec_workflow.md",
        REPO_ROOT / ".ai" / "workflows" / "plan_workflow.md",
        MANAGEMENT_DIR / "AGENTS.md",
    ]
    required_output_phrases = (
        "outputs/",
        "Internal Name",
        "lowercase",
        "replace",
        "prompt the user",
        "description",
        "events",
        "images",
        "posts",
        "mandatory output taxonomy",
        "Execution stopped",
    )
    for path in output_guidance:
        if not path.exists():
            continue
        text = read_text(path)
        missing = [phrase for phrase in required_output_phrases if phrase not in text]
        if missing:
            result.error(
                f"Active output guidance is missing required phrase(s) in {path.relative_to(REPO_ROOT)}: "
                + ", ".join(missing)
            )

    return result


def collect_targets(args: argparse.Namespace) -> tuple[list[Path], list[Path], list[Path]]:
    if args.all_files:
        tasks = sorted((MANAGEMENT_DIR / "tasks").glob("TASK-*.md"))
        specs = sorted((MANAGEMENT_DIR / "specs").glob("SPEC-*.md"))
        plans = sorted((MANAGEMENT_DIR / "plans").glob("PLAN-*.md"))
        return tasks, specs, plans

    tasks: list[Path] = [Path(item).resolve() for item in args.task]
    specs: list[Path] = [Path(item).resolve() for item in args.spec]
    plans: list[Path] = [Path(item).resolve() for item in args.plan]

    if tasks or specs or plans:
        return tasks, specs, plans

    return (
        parse_index_rows(MANAGEMENT_DIR / "tasks" / "INDEX.md", "TASK"),
        parse_index_rows(MANAGEMENT_DIR / "specs" / "INDEX.md", "SPEC"),
        parse_index_rows(MANAGEMENT_DIR / "plans" / "INDEX.md", "PLAN"),
    )


def print_result(result: ValidationResult) -> None:
    status = "PASS" if result.ok else "FAIL"
    rel_path = result.path.relative_to(REPO_ROOT)
    print(f"[{status}] {rel_path}")
    for warning in result.warnings:
        print(f"  warning: {warning}")
    for error in result.errors:
        print(f"  error: {error}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate TASK, SPEC, and PLAN compliance.")
    parser.add_argument("--task", action="append", default=[], help="Path to a TASK file to validate")
    parser.add_argument("--spec", action="append", default=[], help="Path to a SPEC file to validate")
    parser.add_argument("--plan", action="append", default=[], help="Path to a PLAN file to validate")
    parser.add_argument(
        "--all-files",
        action="store_true",
        help="Validate all TASK, SPEC, and PLAN files on disk instead of only index-tracked artifacts",
    )
    args = parser.parse_args()

    tasks, specs, plans = collect_targets(args)
    results: list[ValidationResult] = []

    for task_path in tasks:
        result, _ = validate_task(task_path)
        results.append(result)

    for spec_path in specs:
        result, _ = validate_spec(spec_path)
        results.append(result)

    for plan_path in plans:
        results.append(validate_plan(plan_path))

    if args.all_files or not (args.task or args.spec or args.plan):
        results.append(validate_active_guidance())

    if not results:
        print("No artifacts selected for validation.")
        return 1

    for result in results:
        print_result(result)

    failures = [result for result in results if not result.ok]
    if failures:
        print(f"\nValidation failed: {len(failures)} artifact(s) have compliance errors.")
        return 1

    print(f"\nValidation passed: {len(results)} artifact(s) compliant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
