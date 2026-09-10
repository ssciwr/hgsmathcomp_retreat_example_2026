# Agentic Coding Workshop Plan: Predator–Prey Lab

Use **Lotka–Volterra**, but make it a deliberately small “predator–prey lab,” not a full app. It fits the PhD audience, provides real correctness traps, and lets every exercise build on the same repository.

Keep Tic-Tac-Toe as an optional fallback for attendees who have broken environments or no scientific Python stack.

## Course outcome

A small Python package that:

- simulates Lotka–Volterra dynamics with `scipy.integrate.solve_ivp`
- validates parameters and initial states
- exports results to CSV
- plots populations over time
- has tests, BDD scenarios, an ADR, a custom skill, a reviewer subagent, and an MCP tool

## Design principles for unreliable/free models

1. **Every exercise must have a prepared checkpoint branch.** If an agent fails, students checkout `exercise-03-start` and continue.
2. **One narrowly scoped prompt per task.** Avoid “build the app.” Ask for one function, test module, or document.
3. **Give acceptance criteria in the prompt.** Free models perform far better with explicit inputs, outputs, and constraints.
4. **Use small files.** Aim for fewer than 150 lines per module and fewer than 100 lines per test file.
5. **Do not make agent output the primary deliverable.** The learning objective is the workflow: inspect → constrain → run → review → revise.
6. **Always run local deterministic commands.**

   ```bash
   pytest -q
   ruff check .
   ```

   The agent proposes; the test suite decides.

---

# Suggested repository

```text
predator_prey_lab/
├── README.md
├── pyproject.toml
├── src/predator_prey/
│   ├── __init__.py
│   ├── model.py          # equations and parameter dataclass
│   ├── simulation.py     # solve_ivp wrapper
│   ├── io.py             # CSV export
│   └── plot.py           # optional plot helper
├── tests/
│   ├── test_model.py
│   ├── test_simulation.py
│   └── features/
│       ├── simulation.feature
│       └── test_simulation_steps.py
├── docs/
│   └── adr/
├── .pi/
│   ├── skills/
│   └── agents/
└── workshop/
    ├── prompts/
    └── checkpoints.md
```

Use a simple model:

\[
dx/dt = \alpha x - \beta xy
\]
\[
dy/dt = \delta xy - \gamma y
\]

Where `x` is prey and `y` is predator population.

---

# Eight exercises

## 1. Basic coding-agent usage: fill in a prepared API

**Goal:** Show that a small, constrained prompt can safely generate useful code.

**Starting state:** `model.py` contains a dataclass and `lotka_volterra_rhs(...)` with `NotImplementedError`.

### Student instructions

1. Open `src/predator_prey/model.py`.
2. Read the docstring and type hints.
3. Prompt the agent:

   > Implement only `lotka_volterra_rhs` in `src/predator_prey/model.py`.
   > Do not change the public function signature or other files.
   > Return derivatives `(d_prey, d_predator)` using the equations in the docstring.
   > Add concise comments explaining each term.

4. Inspect the diff.
5. Run:

   ```bash
   pytest -q tests/test_model.py
   ```

6. Fix manually or prompt again only for the failing behavior.

**Teaching point:** Types, docstrings, TODOs, and comments are lightweight steering mechanisms.

---

## 2. Planning → critique → ADR

**Goal:** Show that planning is useful only when it becomes an inspectable engineering decision.

**Scenario:** Decide how simulation configuration and validation should work.

### Student instructions

1. Ask the agent for a plan only:

   > Inspect this repository. Propose a minimal plan for adding a `simulate` API based on `scipy.integrate.solve_ivp`.
   > Requirements: typed parameters, input validation, deterministic tests, and no plotting inside the simulation layer.
   > Do not edit files.

2. Critique its plan:

   > Critique the plan for unnecessary abstraction, hidden numerical assumptions, missing validation, and testability.
   > Give a revised plan with at most five steps.

3. Ask for an ADR:

   > Create `docs/adr/001-simulation-api.md` from the revised plan.
   > Include Context, Decision, Alternatives Considered, Consequences, and Acceptance Criteria.
   > Keep it under 500 words.

4. Review the ADR together. In particular, discuss:
   - solver choice and tolerances
   - whether negative initial populations are invalid
   - whether parameter values must be positive
   - separation of numerical simulation from plotting/export

**Teaching point:** The output is not “the plan”; the output is a decision artifact humans can challenge.

---

## 3. Agentic TDD: tests first, implementation second

**Goal:** Demonstrate isolated agent roles and a test-controlled implementation loop.

**Starting state:** ADR exists; `simulation.py` is empty.

### Student instructions

1. In a first agent session, request tests only:

   > Based on ADR 001, add tests for `simulate` in `tests/test_simulation.py`.
   > Do not implement production code.
   > Cover: output shape, initial state preservation, finite results, invalid negative initial populations, and invalid non-positive model parameters.

2. Inspect test quality:
   - Are tests checking implementation details?
   - Are numerical assertions tolerant rather than exact?
   - Does the initial-state test account for solver output conventions?

3. In a **new agent session**, request implementation only:

   > Implement the smallest `simulate` function that makes the existing tests pass.
   > Do not alter tests, public signatures, or the ADR.
   > Use `scipy.integrate.solve_ivp`.

4. Run tests:

   ```bash
   pytest -q
   ```

5. If red, ask the implementation agent:

   > Here is the exact failing test output. Diagnose and fix production code only.

6. Once green, ask a final session:

   > Refactor only for readability. Preserve behavior and do not change tests. Run pytest afterward.

**Teaching point:** Separate test author, implementer, and refactorer contexts to reduce “the agent changes the test to make itself correct.”

---

## 4. Agentic BDD: user story → executable scenario → TDD

**Goal:** Start from behavior visible to a scientific user rather than internal functions.

### User story to provide

> As a researcher, I want to run a predator–prey simulation over a requested time range so that I can compare prey and predator trajectories at known observation times.

### Student instructions

1. Write the story yourself before calling an agent.
2. Ask the agent:

   > Convert this story into pytest-bdd scenarios in `tests/features/simulation.feature`.
   > Use concrete examples. Include successful simulation and invalid input behavior.
   > Do not write implementation code.

3. Review and simplify the feature file. Keep only 2–3 scenarios.
4. Ask the agent to write step definitions:

   > Implement pytest-bdd step definitions for the approved feature file.
   > Reuse the existing public API. Do not change production code.

5. Run:

   ```bash
   pytest -q
   ```

6. Use the same TDD loop as Exercise 3 to implement any missing behavior.

### Recommended scenarios

- A simulation returns one population pair per requested observation time.
- The first result equals the supplied initial populations.
- Invalid initial populations receive a clear validation error.

**Teaching point:** BDD is not “tests in English.” It is an agreement about observable user behavior.

---

## 5. Custom skill: repository-overview skill

**Goal:** Teach skills as reusable workflow manuals, not magical capability upgrades.

### Student instructions

1. Explain the desired behavior:

   > Given an unfamiliar repository, produce a concise architecture overview: entry points, modules, tests, dependency boundaries, and likely risk areas.

2. Ask the agent:

   > Create a custom skill named `repo-overview` for Pi.
   > It must instruct an agent to inspect a repository efficiently and write `scout/overview.md`.
   > Include: when to use it, step-by-step workflow, output template, and rules against inventing architecture.

3. Review the generated skill manually.
4. Improve it by adding explicit constraints:
   - inspect `pyproject.toml` or the package manifest first
   - distinguish observed facts from inferred relationships
   - list commands used
   - mark uncertainty
   - cap overview length at roughly 600 words

5. Run the skill against the workshop repository.
6. Compare the overview against the repository structure.

**Teaching point:** A skill encodes a repeatable process and quality bar; it does not replace judgment.

---

## 6. Custom subagent: code-reviewer role

**Goal:** Show role separation and bounded review prompts.

### Student instructions

1. Ask the agent to create a Pi subagent definition:

   > Create a `code-reviewer` subagent definition for this Python scientific-computing repository.
   > It must not modify files.
   > It reviews correctness, numerical robustness, API compatibility, tests, error handling, and unnecessary complexity.
   > Output findings ordered by severity with file and line references.

2. Review the role definition. Ensure it says:
   - inspect first, do not assume
   - no implementation changes
   - distinguish bugs from suggestions
   - do not demand speculative abstractions
   - request test evidence for numerical claims

3. Make a deliberately flawed change, such as:
   - permit negative initial populations
   - swap predator/prey derivative terms
   - call the solver without requested output times
   - silently discard solver failures

4. Run the reviewer subagent.
5. Have students classify findings:
   - true bug
   - questionable recommendation
   - false positive
   - missing issue

**Teaching point:** Subagents are prompt-packaged perspectives, not authoritative reviewers.

---

## 7. MCP: connect a supplied FastMCP server

**Goal:** Teach tool discovery, explicit tool boundaries, and verification of external-tool results.

Keep the supplied server intentionally modest. Ideal tools:

- `validate_parameters(alpha, beta, delta, gamma)`
- `equilibrium_points(alpha, beta, delta, gamma)`
- `sample_initial_conditions(seed, count)`

Avoid an MCP server that writes arbitrary code or hides the whole exercise’s logic.

### Student instructions

1. Start the supplied FastMCP server.
2. Add the `pi-mcp-adapter` extension/configuration.
3. Restart Pi if required.
4. List the available MCP tools.
5. Ask the agent:

   > Use the MCP tool discovery output to explain which available tool is appropriate for validating model parameters. Do not modify code.

6. Ask it to call the parameter validator for one valid and one invalid configuration.
7. Verify the results against ordinary Python validation logic.
8. Optionally ask the agent:

   > Add a small CLI command that calls the MCP equilibrium-point tool and prints the returned values. Keep the existing simulation independent of MCP.

**Teaching point:** MCP augments an agent with explicit tools. It should not become an invisible dependency in core domain logic.

---

## 8. Capstone: plan → critique → ADR → BDD/TDD → review

**Goal:** Tie all patterns together in one small, realistic feature.

**Feature:** CSV export with metadata.

Example desired output:

```csv
time,prey,predator
0.0,40.0,9.0
0.5,...
```

Optional metadata sidecar: solver settings and model parameters in JSON.

### Student instructions

1. Prompt for a plan:

   > Plan a minimal CSV-export feature for simulation results. Do not edit files.

2. Critique the plan:

   > Identify ambiguities, compatibility risks, and missing test cases. Revise to five steps or fewer.

3. Write an ADR covering:
   - output schema
   - overwrite behavior
   - NaN/failed-simulation policy
   - whether metadata is embedded or separate

4. Write a BDD scenario:

   > A researcher can export a completed simulation and reload the CSV with the expected columns and row count.

5. Generate unit tests before implementation.
6. Use a fresh agent session for implementation.
7. Run tests and lint.
8. Run the `code-reviewer` subagent.
9. Decide which findings to accept, reject, or defer in the ADR.

**Teaching point:** The end-to-end workflow is deliberate narrowing: idea → decision → behavior → tests → implementation → independent review.

---

# Suggested course flow

| Block | Exercise | Time |
|---|---:|---:|
| Warm-up | 1. API completion | 20 min |
| Design | 2. Plan, critique, ADR | 30 min |
| Correctness | 3. TDD | 40 min |
| User behavior | 4. BDD | 35 min |
| Reuse | 5. Skill | 25 min |
| Delegation | 6. Reviewer subagent | 25 min |
| Tools | 7. MCP | 30 min |
| Integration | 8. Capstone | 45–60 min |

This is roughly a **one-day workshop**. Exercises 1–4 also work as a shorter half-day session.

---

# Preparation checklist

Prepare these in advance:

- a tested starter repository
- one branch or tag per exercise:

  ```text
  exercise-01-start
  exercise-01-solution
  ...
  exercise-08-start
  exercise-08-solution
  ```

- pinned dependencies in `pyproject.toml`
- one-page environment setup instructions
- copy/paste prompts in `workshop/prompts/`
- a known-good FastMCP server and configuration
- a manual solution patch for every exercise
- deliberately flawed commits for the reviewer exercise
- a small worksheet asking students to record:
  - prompt used
  - agent failure or mistake
  - local verification command
  - human decision made

## Key framing for participants

> Agentic coding is not delegating responsibility. It is designing short feedback loops in which agents generate hypotheses and artifacts, while humans define constraints and deterministic tools verify outcomes.

The Lotka–Volterra domain makes that visible: generated code may look plausible while being mathematically wrong, numerically fragile, or behaviorally incompatible.
