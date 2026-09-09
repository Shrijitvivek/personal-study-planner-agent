# Personal Study Planner Agent

A small Python project that helps a student decide what to study next based on their topic needs, time available, and prior progress.

## Features

- Detects study topic from user input
- Extracts available study time
- Understands basic intent such as practice, revision, plan, and next topic
- Tracks completed and weak topics
- Recommends a study plan, practice questions, or revision task

## Project files

- `agent.py` – main CLI loop
- `input_memory.py` – parsing and memory tracking
- `decision_engine.py` – logic that chooses the next action
- `tools.py` – generated study tasks and questions

## Run it

From the project folder, run:

```bash
python agent.py
```

Then type requests like:

- "I have 30 minutes and need practice on functions"
- "Plan my revision for variables"
- "What should I study next?"

## Requirements

This project uses the Python standard library only, so no external dependencies are required.

## Notes

The agent is intentionally simple and designed for learning and assignment work.
