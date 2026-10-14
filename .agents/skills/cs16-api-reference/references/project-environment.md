# Project toolchain memory

Use this workflow when a plugin task needs local include lookup or compilation and the environment has not been recorded, has changed, or cannot be reused. Store the selected compiler and include paths once as project context, then reuse them after checking the relevant paths.

## Read existing context first

Read applicable project instructions, the active build configuration and any established toolchain notes. The default local record is `<target-project>/.agents/cs16-environment.md`. If the project already records this information in another maintained Markdown file or directly in `AGENTS.md`, use that location rather than creating a competing record.

Current user instructions and the active build configuration take precedence over an old saved profile. If their selections conflict and the conversation does not resolve the choice, clarify the specific compiler or include set needed by the task. A saved path is a useful hint, not proof that the file still exists or that the toolchain still works.

## Discover the actual selection

Prefer paths supplied by the user and paths used by the project's build command. Inspect relevant build scripts, task configuration, Makefiles or CI definitions before looking for another installation. Resolve relative paths and environment variables using the build's working directory and execution context.

When configuration is incomplete, inspect the project and the selected SDK/compiler's adjacent directories. A compiler located through `PATH` is a candidate until it is associated with the intended build. Do not treat the skill's bundled `references/includes` directory as the user's SDK, or choose between multiple compiler installations merely by their directory names.

Confirm that a local compiler path points to the intended executable and that the selected include directory contains the headers needed by the feature. Read local version macros when useful. Only claim a working compiler after an appropriate compile succeeds; a path-existence check alone establishes that the file is present. Reuse the project's normal build command when it defines important flags or runtime wrappers.

If several include directories participate in the build, record their order and preserve the compiler's actual resolution rules. A header found later in the search path must not silently replace one selected earlier. Container, WSL or remote paths need their execution context recorded; they are not interchangeable with host filesystem paths.

Ask for missing paths only when the task needs them and project evidence cannot establish the selection. Include lookup can proceed with a known include directory even if the compiler is unavailable. Keep unresolved fields explicitly unknown rather than substituting the bundled snapshot or a guessed installation.

## Save the project context

During authorized plugin implementation or environment setup, create or update the local record with the selections actually established. For a read-only task, use existing context without creating configuration files unless saving it was requested.

Use [the environment template](../assets/cs16-environment.template.md) as a starting shape, adapting it to the project. Save the compiler executable, include directory or ordered directories, build working directory, and established build command. Add the host/execution context, selection evidence and verification status so another task can distinguish a user-provided preference from a discovered build setting.

- Save known values; mark unavailable compiler/version/build verification as unknown or not performed. Do not leave template placeholders in a claimed configured profile.
- Prefer project-relative paths for tools shipped with the project; use validated absolute paths for an external installation. Resolve relative profile paths from the documented project root, unless a field explicitly specifies another base.
- Record a user-provided path as user-provided. Record a path inferred from a build script as discovered from that script; do not relabel it as a direct user instruction.
- Keep machine-specific values in the target project's local context, outside the portable `SKILL.md`, source manifest and reference snapshot. Follow the project's existing local-file ignore convention when absolute host paths should remain unshared.
- Update only the relevant environment fields; preserve other project instructions and unrelated notes. Do not overwrite a working profile with an unrelated compiler found on another host.

This skills repository is not itself a configured plugin project. Add the instruction and template here; create the actual environment record in the consuming project only when its toolchain is established.

## Make the record discoverable

All domain skills read the shared contracts, which explicitly direct the assistant to read the established environment record when selecting compile inputs. An arbitrary Markdown filename does not automatically become an instruction file.

For persistent project guidance, add a small pointer to the applicable project `AGENTS.md` when establishing this environment within the requested scope. Preserve existing content and more-specific instructions. If the project uses another agent's instructions file, use its established convention instead.

Example `AGENTS.md` addition after the environment record exists:

```markdown
## CS 1.6 toolchain

Before local Pawn API lookup or compilation, read `.agents/cs16-environment.md`.
Reuse its compiler and include selections for this project, verify the paths
needed by the task, and update stale settings from current user instructions
and the active build configuration. Resolve relative profile paths from the
project root. Keep compiler include search order intact.
```

Codex's [project-instruction documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) describes how `AGENTS.md` guidance is discovered. The pointer requests an explicit read of the local environment record without requiring custom filename configuration.

## Reuse on later tasks

Read the established record, check the paths needed for the current operation, and reuse valid settings without repeatedly asking the user. If the host, build command or SDK changes, update the affected fields after resolving the new selection. Retain verification results as dated observations; do not present an old successful compile as validation of a new plugin change.

Pass the saved values explicitly to `api_catalog.py --include-dir` and, when compiling the bundled examples, `validate_examples.py --compiler ... --include-dir ...`. These helpers do not parse the Markdown profile automatically. Use the project's full build command for builds that require additional include paths, flags or wrappers. The record describes the user's environment; it does not alter the SDK or establish installed server capabilities.
