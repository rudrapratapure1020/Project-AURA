# Project AURA

**AURA** is a local AI-powered desktop automation assistant for Windows. It is designed to understand natural-language instructions, turn them into actionable steps, and execute those steps through a modular set of desktop tools.

The project brings together an agent workflow, local language-model planning, command routing, desktop automation, and execution safeguards.

> **Status:** Active development — working prototype  
> **Platform:** Windows desktop  
> **Primary language:** Python  
> **Local LLM runtime:** Ollama  
> **Model tested:** `llama3.2:3b`

## Features

- Accepts natural-language task requests through the AURA agent.
- Converts requests into structured action plans.
- Routes planned commands to registered tools for execution.
- Launches supported applications, including Chrome, Notepad, Calculator, and Paint.
- Performs Google searches through the browser automation tool; Microsoft Edge was tested for this flow.
- Automates keyboard and mouse input.
- Reads from and writes to the system clipboard.
- Captures desktop screenshots.
- Tracks execution context, including the current application and foreground window.
- Includes safeguards against repeated duplicate actions and runaway multi-step execution.
- Supports local LLM planning through Ollama, reducing dependence on a paid cloud API.

## Architecture

AURA follows a modular agent-and-tools design. The agent receives a request, obtains a plan, normalizes and routes the planned commands, executes them through desktop tools, and uses context/observation modules to track the desktop state.

```text
                User instruction
                       |
                       v
                 core/agent.py
                       |
                       v
              Brain / Planner (LLM)
                       |
                       v
           Command normalization
                       |
                       v
                Command router
                       |
                       v
               Command registry
                       |
                       v
                   Executor
                       |
                       v
                 Desktop tools
                       |
                       v
             Context / Observation
                       |
                       v
              Result to the agent
```

### Core modules

| Module | Responsibility |
|---|---|
| `core/agent.py` | Main agent workflow; coordinates request handling, planning, and execution. |
| `core/brain.py` | AI/LLM-facing reasoning component used by the agent. |
| `core/planner.py` | Produces an action plan from a user request. |
| `core/executor.py` | Executes planned commands through the available tools. |
| `core/router.py` | Routes normalized commands to the appropriate registered action. |
| `core/command_normalizer.py` | Normalizes command wording before routing. |
| `core/command_registry.py` | Maintains the available command/tool registrations. |
| `core/context.py` | Stores execution context, including current application and window information. |
| `core/observer.py` | Observes desktop state, including the foreground application/window. |

### Desktop tools

| Module | Responsibility |
|---|---|
| `tools/app_discovery.py` | Supports discovery of installed or available applications. |
| `tools/app_launcher.py` | Opens supported desktop applications. |
| `tools/browser.py` | Browser actions, including Google search. |
| `tools/keyboard_tool.py` | Keyboard input and typing actions. |
| `tools/mouse_tool.py` | Mouse movement and click actions. |
| `tools/clipboard_tool.py` | Clipboard read/write operations. |
| `tools/screenshot_tool.py` | Captures screenshots of the desktop. |
| `tools/window_tool.py` | Window-related inspection and control support. |

## Technology stack

- **Python** — agent logic and desktop automation.
- **Ollama** — local model runtime.
- **Llama 3.2 3B (`llama3.2:3b`)** — local model used in planning tests.
- **PyAutoGUI** — keyboard, mouse, and desktop automation.
- **Pillow / PyScreeze** — screenshot and image support used by the automation stack.
- **Pyperclip** — clipboard operations.
- **Git and GitHub** — source control and project hosting.

The project also experimented with the OpenAI API. Cloud API planning encountered an account quota/credit limitation, so Ollama was installed and used as a local planning alternative.

## Project structure

The following is the project structure established during development. Update it if the repository changes.

```text
Project-AURA/
├── core/
│   ├── agent.py
│   ├── brain.py
│   ├── command_normalizer.py
│   ├── command_registry.py
│   ├── context.py
│   ├── executor.py
│   ├── observer.py
│   ├── planner.py
│   └── router.py
│
├── tools/
│   ├── app_discovery.py
│   ├── app_launcher.py
│   ├── browser.py
│   ├── clipboard_tool.py
│   ├── keyboard_tool.py
│   ├── mouse_tool.py
│   ├── screenshot_tool.py
│   └── window_tool.py
│
├── .env                 # Local configuration/secrets; do not commit
├── .gitignore
├── main.py
└── README.md
```

## Setup and installation

These instructions reflect the development environment used for the prototype. Exact dependencies and configuration may change as the project evolves.

### Prerequisites

- Windows 10 or Windows 11
- Python 3.11 (Python 3.11.9 was used during development)
- Git
- Ollama
- A supported Ollama model

### 1. Clone the repository

```bash
git clone https://github.com/rudrapratapure1020/Project-AURA.git
cd Project-AURA
```

### 2. Create and activate a virtual environment

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

If `py -3.11` is not recognized, install Python 3.11 and confirm that the Python launcher can find it.

### 3. Install the current known dependencies

```bash
python -m pip install --upgrade pip
pip install openai pyautogui pillow pyscreeze pyperclip
```

These are the packages used or installed during the development work recorded so far. Other imports in the current source may require additional packages. If a `requirements.txt` is added to the repository, use that as the authoritative dependency list:

```bash
pip install -r requirements.txt
```

### 4. Install and configure Ollama

Install Ollama, then download the model used during development:

```bash
ollama pull llama3.2:3b
```

Ensure the Ollama service is running before launching AURA. The local OpenAI-compatible endpoint used in development was:

```text
http://localhost:11434/v1/
```

The model identifier used was:

```text
llama3.2:3b
```

### 5. Configure environment variables

AURA uses a root `.env` file for local configuration. Keep API keys and other secrets in your local environment and **never commit `.env` or publish secret keys**.

Use the exact variable names expected by the current source code; this README intentionally does not guess them.

### 6. Run AURA

With the virtual environment active and Ollama running, start the application from the repository root:

```bash
python main.py
```

## Safety and execution controls

Desktop automation can make real changes to a computer. During development, the following safeguards were added and tested:

- **Repeated-action blocking:** detects and blocks repeated identical actions in the execution flow.
- **Execution-step limit:** a six-step safety limit was introduced to stop runaway action loops.
- **Desktop context tracking:** records the current application/window and observes the foreground window to provide context for actions.

These controls reduce specific failure modes, but they do not make the prototype risk-free. Review actions carefully, particularly keyboard input, mouse clicks, and actions in applications containing important data. Do not rely on the current prototype for unattended sensitive operations.

## Implemented and tested during development

The following capabilities have been exercised in the development environment:

- Starting AURA and exiting its command loop.
- Local planning tests using Ollama and `llama3.2:3b`.
- Opening Chrome, Notepad, Calculator, and Paint.
- Performing a Google search through the browser tool; Edge was tested for this flow.
- Keyboard and mouse automation.
- Clipboard read/write operations.
- Screenshot capture after installing the required screenshot dependencies.
- Tracking the active/foreground application and window.
- Blocking repeated actions and stopping execution at the configured safety limit.
- Fixing integration issues involving command routing/imports, browser search arguments, screenshot dependencies, and repeated-action loops.

This is a development record, not a formal benchmark. A verified accuracy score, F1 score, task-success rate, latency benchmark, or total supported-command count has not yet been established. No such performance metrics are claimed here.

## Current limitations

- AURA is currently a Windows desktop prototype; full mobile/phone automation has not been established.
- Automation reliability depends on desktop state, application availability, permissions, and UI changes.
- Natural-language planning and multi-step execution can still produce incorrect actions or misunderstand ambiguous requests.
- The local model is relatively small and may need clearer instructions for complex tasks.
- The project has not yet been validated as a production-ready or fully autonomous assistant.
- Formal automated evaluation and repeatable benchmark results are still pending.

## Roadmap

Potential next development milestones:

- Expand and document the supported command set.
- Improve planner-output validation and execution error recovery.
- Add explicit confirmation gates before sensitive or destructive actions.
- Create repeatable unit and end-to-end tests for tools and agent workflows.
- Measure task success rate, failure categories, and execution time on a defined test set.
- Add structured logs and clearer execution reports.
- Add a pinned `requirements.txt` for reproducible setup.
- Improve cross-application reliability and desktop-state awareness.
- Explore mobile integration as a separate future milestone.

## Repository

- **GitHub:** [Project AURA](https://github.com/rudrapratapure1020/Project-AURA)
- **Development branch:** `agentic-tools`

## Author

**Rudra Pratapure**

---

*Project AURA is an evolving personal AI automation project. Features and setup instructions should be kept in sync with the current source code.*
