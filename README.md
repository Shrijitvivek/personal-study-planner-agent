# Personal Study Planner Agent

## 1. Business Problem

Students may not always know what they should study next. Their study decision can depend on the available time, weak topics, topics they have already completed, and whether they need practice or revision.

The Personal Study Planner Agent helps students decide what to study based on their current situation and learning progress.

## 2. Why an Agent is Useful

An agent is useful because it can take the student's current input, understand the situation, make a decision, and choose an appropriate action.

Instead of giving the same response to every student, the agent can choose between creating a study plan, giving practice questions, or providing a revision task.

The agent also uses simple memory to keep track of the student's completed topics, weak topics, and last studied topic.

## 3. Agent Goal

The goal of the Personal Study Planner Agent is to help a student decide what to study and what action to take based on:

- Available study time
- Weak topics
- Completed topics
- Current study request
- Previous learning progress

## 4. Architecture

The agent follows this basic flow:

    Student Input
          |
          v
    Input Parser + Memory
          |
          v
    Decision Engine
          |
          v
    Select Appropriate Tool
          |
          v
    Tool Result
          |
          v
    Agent Response

The main components are:

- `agent.py` - Main entry point and connects all components.
- `input_memory.py` - Parses the student's input and maintains learning state.
- `decision_engine.py` - Makes decisions based on the parsed input and memory.
- `tools.py` - Contains the actions performed by the agent.

## 5. Agent Workflow

The agent works through the following steps:

1. The student enters a study request.
2. The input parser extracts useful information such as topic, available time, intent, weak topics, and completed topics.
3. The agent updates the student's memory when learning progress is mentioned.
4. The decision engine checks the student's situation.
5. The decision engine selects an appropriate action.
6. The selected tool performs the action.
7. The agent displays the result to the student.
8. If the input is unclear, the agent asks the student for clarification.
9. The agent stops when the student enters `exit`.

## 6. Tools / Actions

The agent uses three main tools:

### `create_study_plan()`

Creates a study plan based on the selected topic and available study time.

The plan can contain:

- Concept review
- Practice
- Revision

### `give_practice_questions()`

Provides practice questions for the selected topic.

The number of questions can depend on whether the topic is a weak topic.

### `give_revision_task()`

Provides a revision activity containing:

- Recall
- Practice
- Self-test

These tools are selected by the Decision Engine based on the student's situation.

## 7. Memory / State

The agent maintains a simple in-memory student state.

It stores:

- `completed_topics` - Topics the student has already studied.
- `weak_topics` - Topics where the student needs more practice.
- `last_studied` - The most recently studied topic.
- `pending intent` - Used when the agent asks for missing information, such as asking for a topic before giving a revision task.

For example:

Student:
`Give me a revision task`

Agent:
`Which topic would you like revision for?`

Student:
`Functions`

The agent remembers that the student requested a revision task and provides a revision task for Functions.

The memory is simple and is available only while the program is running.

## 8. How to Run the Project

Clone the repository and enter the project directory.

Run the agent from the `src` directory:

    cd src
    python3 agent.py

The agent will ask for a study request.

Example:

    Student: I have 1 hour and want to study Python functions

To stop the agent:

    Student: exit

### Running the test scenarios

From the project root, run:

    python3 -m tests.test_scenarios

## 9. Sample Input / Output

Example input:

    Student: I have 1 hour and want to study Python functions

Example output:

    Topic           : Functions
    Available Time  : 60 minutes

    Concept Review  : 21 minutes
    Practice        : 24 minutes
    Revision        : 15 minutes

More demonstration scenarios are available in
`examples/sample_output.txt`.

## 10. Limitations

The current version has some limitations:

- The input parser uses simple keyword-based matching.
- Only a limited number of Python topics are currently supported.
- The memory is stored only while the program is running.
- The agent does not use external APIs or an LLM to understand complex language.
- The study recommendations are based on predefined rules.

## 11. Future Improvements

Possible future improvements include:

- Add more Python topics and subjects.
- Use an LLM for better natural-language understanding.
- Add persistent memory so learning progress is saved between sessions.
- Provide more personalized study recommendations.
- Add more types of practice questions and revision activities.
- Improve the agent's ability to understand different ways of expressing the same request.