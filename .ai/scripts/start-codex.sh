#!/bin/bash

set -u
set -o pipefail

get_project_root() {
    local current
    current="$(pwd -P)"

    while [[ "$current" != "/" ]]; do
        if [[ -d "$current/.ai" ]]; then
            printf '%s\n' "$current"
            return 0
        fi

        current="$(dirname "$current")"
    done

    if [[ -d "/.ai" ]]; then
        printf '%s\n' "/"
        return 0
    fi

    printf '%s\n' "Directory .ai not found in current path or parent directories." >&2
    return 1
}

get_directory_hash() {
    local path="$1"

    (
        cd "$path" || exit 1

        find . \
            -type f \
            ! -path './cache/*' \
            ! -path './.codex-state/*' \
            -print |
            LC_ALL=C sort |
            while IFS= read -r file; do
                local relative_path="${file#./}"
                local file_hash
                file_hash="$(sha256sum "$file" | awk '{print $1}')"
                printf '%s|%s\n' "$relative_path" "$file_hash"
            done |
            sha256sum |
            awk '{print $1}'
    )
}

sync_codex_folders() {
    local project_root="$1"
    local ai_root="$2"
    local agents_root="$project_root/.agents"
    local codex_root="$project_root/.codex"
    local source_agents="$ai_root/agents"
    local source_skills="$ai_root/skills"
    local source_rules="$ai_root/rules"
    local source_hooks="$ai_root/hooks.json"
    local source_config="$ai_root/config.toml"
    local source_agents_md="$ai_root/AGENTS.md"

    rm -rf "$agents_root" "$codex_root" || return 1

    mkdir -p "$agents_root/skills" || return 1
    mkdir -p "$codex_root/rules" || return 1

    if [[ -d "$source_skills" ]]; then
        cp -a "$source_skills"/. "$agents_root/skills/" || return 1
    fi

    if [[ -d "$source_rules" ]]; then
        cp -a "$source_rules"/. "$codex_root/rules/" || return 1
    fi

    if [[ -f "$source_hooks" ]]; then
        cp -f "$source_hooks" "$codex_root/hooks.json" || return 1
    fi

    if [[ -f "$source_config" ]]; then
        cp -f "$source_config" "$codex_root/config.toml" || return 1
    fi

    if [[ -f "$source_agents_md" ]]; then
        cp -f "$source_agents_md" "$project_root/AGENTS.md" || return 1
    fi

    if [[ -d "$source_agents" ]]; then
        mkdir -p "$codex_root/agents" || return 1
        cp -a "$source_agents"/. "$codex_root/agents/" || return 1
    fi
}

test_codex_folders_ready() {
    local project_root="$1"

    [[ -d "$project_root/.agents/skills" && -d "$project_root/.codex/rules" ]]
}

disabled_folder_roots=()
disabled_folder_targets=()

disable_generated_folder_for_run() {
    local project_root="$1"
    local folder_name="$2"
    local folder_root="$project_root/$folder_name"
    local suffix=0
    local disabled_root

    if [[ ! -d "$folder_root" ]]; then
        return 0
    fi

    while true; do
        suffix=$((suffix + 1))
        disabled_root="$project_root/$folder_name.startup-error.$$.$suffix"

        if [[ ! -e "$disabled_root" ]]; then
            break
        fi
    done

    mv "$folder_root" "$disabled_root"
    disabled_folder_roots+=("$folder_root")
    disabled_folder_targets+=("$disabled_root")
}

disable_generated_folders_for_run() {
    local project_root="$1"

    disable_generated_folder_for_run "$project_root" ".agents"
    disable_generated_folder_for_run "$project_root" ".codex"
}

restore_generated_folders_after_run() {
    local i

    for ((i = 0; i < ${#disabled_folder_targets[@]}; i++)); do
        local folder_root="${disabled_folder_roots[$i]}"
        local disabled_root="${disabled_folder_targets[$i]}"

        if [[ ! -d "$disabled_root" ]]; then
            continue
        fi

        if [[ -e "$folder_root" ]]; then
            printf "Codex startup warning: skipped restoring '%s' because '%s' now exists.\n" "$disabled_root" "$folder_root" >&2
            continue
        fi

        mv "$disabled_root" "$folder_root"
    done
}

bootstrap_codex_folders() {
    local project_root="$1"
    local ai_root="$project_root/.ai"
    local state_root="$ai_root/.codex-state"
    local hash_file="$state_root/last-ai-hash.txt"
    local current_hash
    local previous_hash=""

    mkdir -p "$state_root" || return 1

    current_hash="$(get_directory_hash "$ai_root")" || return 1

    if [[ -f "$hash_file" ]]; then
        previous_hash="$(tr -d '[:space:]' < "$hash_file")" || return 1
    fi

    if [[ "$current_hash" != "$previous_hash" ]] || ! test_codex_folders_ready "$project_root"; then
        sync_codex_folders "$project_root" "$ai_root" || return 1
        printf '%s' "$current_hash" > "$hash_file" || return 1
    fi
}

startup_location="$(pwd -P)"
project_root="$startup_location"
codex_exit_code=0

if found_project_root="$(get_project_root)"; then
    project_root="$found_project_root"

    if ! bootstrap_codex_folders "$project_root"; then
        printf '%s\n' "Codex startup warning: failed to generate .agents and .codex from .ai." >&2
        printf '%s\n' "Codex startup warning: continuing normal startup with generated .agents and .codex disabled for this run." >&2

        if ! disable_generated_folders_for_run "$project_root"; then
            printf '%s\n' "Codex startup warning: could not disable generated folders." >&2
        fi
    fi
else
    printf '%s\n' "Codex startup warning: failed to generate .agents and .codex from .ai." >&2
    printf '%s\n' "Codex startup warning: continuing normal startup from the current directory." >&2
fi

cd "$project_root" || exit 1

codex "$@"
codex_exit_code=$?

cd "$startup_location" || true

if [[ ${#disabled_folder_targets[@]} -gt 0 ]]; then
    restore_generated_folders_after_run
fi

exit "$codex_exit_code"
