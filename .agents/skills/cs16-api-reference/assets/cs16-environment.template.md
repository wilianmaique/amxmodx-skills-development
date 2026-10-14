# CS 1.6 project environment

Use this record for this project's Pawn API lookup and compilation. Current user instructions and the active build configuration take precedence over stale entries. Resolve relative paths from the project root, and check relevant paths before reusing them.

Copy this template to the consuming project's `.agents/cs16-environment.md` only when recording an established toolchain. Replace placeholders with known values or an explicit unknown status. Keep the saved profile outside the portable skill folders.

## Selection context

- Project root: `.`
- Target game: `Counter-Strike 1.6`
- Host / execution context: `<host label and Windows, Linux, WSL or container context>`
- Selection evidence: `<user-provided paths or the specific build configuration used>`
- Last relevant path check: `<YYYY-MM-DD and what was checked>`

## Compiler

- Executable: `<validated absolute or project-relative compiler path, or unknown>`
- Version: `<observed compiler version, or unknown>`
- Build working directory: `<project-relative or absolute working directory>`
- Build command: `<established command with its required flags/wrapper, or not established>`
- Compile verification: `<dated successful check, or not performed>`

## Includes

- Primary API lookup directory: `<validated absolute or project-relative include directory>`
- Compiler include directories, in the build's resolution order:
  1. `<first include directory>`
  2. `<additional directory if used; otherwise remove this item>`
- Local AMXX include version: `<version macro evidence, or unknown>`
- Local ReAPI include version: `<version macro evidence, or not used / unknown>`

## Reuse notes

Record only project-specific details that change how these selections should be used, such as an SDK wrapper, required adjacent compiler library or deliberate compatibility target. Keep server-module availability separate from include-version evidence. Update affected fields when the selected toolchain changes.
