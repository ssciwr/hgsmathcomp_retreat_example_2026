[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Welcome to the Example project for the HGSComp Retreate Workshop 2026

This project exists to exemplify elements of working effectively with coding agents.
We are using the Pi Coding Agent here, a minimal open source system, and will built it out
with extensions as we need.
We are using a simple version of the Lotka-Volterra equations as an example problem an will built
a small app that solves them.

```math
\newline
dx/dt = \alpha x - \beta xy

\newline
dy/dt = \delta xy - \gamma y

```

There are 7 example exercises:

1. Basic usage of coding agents
2. More advanced usage of coding agents using plan mode
3. Agentic test driven development
4. Behavior driven development
5. Writing an `Agents.md` file to 'onboard' an agent onto your project
6. Write a custom skill for the Pi coding agent: `Repo-overview`
7. Add in an MCP server via the `pi-mcp-adapter`

Each example has a separate branch, such that they can be workd on independently.

