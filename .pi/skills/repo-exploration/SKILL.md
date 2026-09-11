---
name: repo-exploration
description: >
  Generate a single-file Markdown overview of an unfamiliar codebase.
  Use whenever the user asks to scout, explore, document, summarize,
  onboard onto, or get an overview of a codebase or repository.
  Writes scout/overview.md inside the target repository.
---

# Repo Overview

Understand the target repository for a new contributor. Inspect its structure, source code, tests, fixtures, documentation, CI, configuration, and tooling, then produce a concise but complete Markdown guide.

The guide must cover:

- the important elements of the technology stack;
- the dominant coding and testing paradigms (for example, object-oriented GUI code, functional numerical code, or unit and integration tests);
- a class diagram and short descriptions of important classes, structs, and free functions;
- a module diagram and descriptions of important modules;
- recommended starting points for reading the code;
- application, library, CLI, and CI entry points and their relevant code paths;
- tests and fixtures, including the production code to which they relate;
- verified commands for building, running, and testing the project; and
- constraints, risks, and open questions.

Include concrete file paths and relationships throughout. Use Mermaid `classDiagram` and `flowchart` fenced blocks when diagrams are appropriate. Include free functions in the class diagram when they are functionally important.

## When to use

- The user asks for an explanation of a repository's structure.
- The user asks for an introduction to a project they have not worked on before.
- The user asks for a succinct representation of a codebase.

## Input

The target repository path is provided as input. When invoked via `/skill:repo-overview <path>`, the path arrives as a user message immediately after the skill body. If no path is supplied, ask which repository to scout before proceeding.

## Workflow

1. Inspect the target repository directly. If a scout/explorer subagent is available and appropriate, use it for a bounded codebase survey.
2. Read `references/example.md` as a structural and density reference only. Reuse its section order and level of detail, but replace every domain-specific statement with facts established from the target repository.
3. Account for the complete repository structure. Summarize generated, vendored, binary, cache, or otherwise repetitive trees rather than listing every contained file.
4. Write the findings as a single Markdown file at `<repo>/scout/overview.md`.
5. Do not write any other files and do not dump the findings into the conversation.
6. Verify build, run, test, and callable-asset commands against repository configuration. Use syntax appropriate to the user's shell and platform.
7. Re-open `scout/overview.md` and check that all required sections below are present, paths and relationships are accurate, Markdown is well formed, and Mermaid diagrams have valid syntax. Correct any problems.
8. Reply with only a short sentence giving the final output path, for example: `Overview written to <repo>/scout/overview.md`.

## Required sections

Use these sections in this order, omitting a diagram only when the repository genuinely has no useful entities or relationships to diagram:

1. Title and one-paragraph repository summary
2. Repository map
3. Tech stack and paradigms
4. Class/function diagram
5. Class, struct, and important-function descriptions
6. Module diagram
7. Module descriptions
8. Reading order and entry points
9. Tests and fixtures
10. How to build, run, and test
11. Documentation pointers
12. Constraints, risks, and open questions

## Markdown requirements

- Use standard Markdown headings, lists, tables, links, and fenced code blocks.
- Use repository-relative paths in backticks; link them when doing so is useful and the relative link can be made correct from `scout/overview.md`.
- Use Mermaid fenced blocks for diagrams; do not embed raw HTML, SVG, CSS, scripts, or external assets.
- Keep the document self-contained and readable in both plain text and Markdown renderers.
- Prefer evidence-backed statements. Clearly label uncertainty as an open question rather than guessing.

## Verification

After writing `scout/overview.md`, re-read it and confirm:

- every required section is present and contains repository-specific information;
- the repository map accounts for all top-level paths and important source/test subtrees;
- important classes, structs, and free functions are represented and described;
- module and execution relationships agree with the code;
- Mermaid blocks use valid `classDiagram` or `flowchart` syntax;
- commands, paths, and links are correct for the target repository and environment; and
- there are no raw browser-document artifacts or legacy browser-output filenames.
