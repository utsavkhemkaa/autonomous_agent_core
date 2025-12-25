# Autonomous Agent Core

A production-style autonomous AI agent framework built from scratch.

This project implements a deterministic agent execution engine with:
- Planner (LLM-based decision making)
- Executor (tool invocation with failure normalization)
- Control loop (retry vs replan logic)
- Explicit state tracking
- Pluggable tool system

The goal is to demonstrate **engineering-first agent design** without relying on high-level frameworks.

---

## Architecture
Planner → Plan → Loop → Executor → Tools → State


Key principles:
- Planner decides **what to do**
- Executor decides **how to do it**
- Loop enforces safety, retries, and termination
- State records what happened (no decision logic)

---

## Running the Agent

### Requirements
- Python 3.10+
- OpenAI API key

```bash
export OPENAI_API_KEY=your_key_here
python main.py

You will be prompted to enter a task.

Tools Included
	•	Web search
	•	File writer
	•	Calculator

Tools are isolated, deterministic, and return structured results.



Why this project?

Most AI agent demos focus on prompt chaining.
This project focuses on:
	•	execution correctness
	•	failure handling
	•	clean system boundaries
	•	production-style control flow


