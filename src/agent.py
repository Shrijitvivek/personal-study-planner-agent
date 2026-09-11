
"""
Personal Study Planner Agent
Final Integration

Combines:
    Part 1 - Input + Memory       -> input_memory.py
    Part 2 - Decision Engine      -> decision_engine.py
    Part 3 - Tools / Actions      -> tools.py

Flow:
    Student Input
          |
          v
    Part 1: Parse Input + Memory
          |
          v
    Part 2: Decision Engine
          |
          v
    Part 3: Selected Tool
          |
          v
    Final Result
"""


from input_memory import parse_user_input, get_student_state
from decision_engine import decide_action


def display_result(result):
    """
    Displays the result returned by the Decision Engine
    in a simple, readable format.
    """

    print("\n" + "=" * 60)

    tool = result.get("tool")

    if tool == "create_study_plan":

        print("                    STUDY PLAN")
        print("=" * 60)

        if result["status"] == "success":

            print(f"\nTopic           : {result['topic']}")
            print(f"Available Time  : {result['time_available']} minutes")

            print("\nPlan:")

            for step in result["plan"]:

                print(f"\n  {step['activity']}")
                print(f"  Duration : {step['duration']} minutes")
                print(f"  Task     : {step['task']}")

        else:

            print(f"\nERROR: {result['message']}")

    elif tool == "give_practice_questions":

        print("                 PRACTICE QUESTIONS")
        print("=" * 60)

        if result["status"] == "success":

            print(f"\nTopic: {result['topic']}")
            print("\nQuestions:")

            for number, question in enumerate(
                result["questions"],
                start=1
            ):
                print(f"\n  {number}. {question}")

        else:

            print(f"\nERROR: {result['message']}")

    elif tool == "give_revision_task":

        print("                    REVISION TASK")
        print("=" * 60)

        if result["status"] == "success":

            task = result["revision_task"]

            print(f"\nTopic    : {task['topic']}")
            print(f"Duration : {task['duration']} minutes")

            print("\nRecall:")
            print(f"  {task['recall']}")

            print("\nPractice:")
            print(f"  {task['practice']}")

            print("\nSelf-Test:")
            print(f"  {task['self_test']}")

        else:

            print(f"\nERROR: {result['message']}")

    else:

        print("                   AGENT RESPONSE")
        print("=" * 60)

        print(
            f"\n{result.get('message', 'No response generated.')}"
        )

    print("\n" + "=" * 60)


def run_agent(user_input):
    """
    Connects all three parts of the Personal Study Planner Agent.

    Part 1:
        Parses the student's natural-language input and
        retrieves the student's memory.

    Part 2:
        Uses the parsed input and memory to decide which
        action should be performed.

    Part 3:
        Executes the selected tool and returns the result.
    """

    # Part 1 - Input + Memory
    parsed_input = parse_user_input(user_input)

    # Get current student memory
    student_memory = get_student_state()

    # Part 2 - Decision Engine
    # Part 2 internally calls the appropriate Part 3 tool.
    result = decide_action(
        parsed_input,
        student_memory
    )

    return result


if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("          PERSONAL STUDY PLANNER AGENT")
    print("=" * 60)

    print("\nThe agent is ready.")
    print("Enter your study request.")
    print("Type 'exit' to stop.")

    while True:

        print("\n" + "-" * 60)

        user_input = input("Student: ")

        if user_input.lower().strip() == "exit":

            print("\nAgent: Good luck with your studies!")
            break

        if not user_input.strip():

            print("Agent: Please enter a study request.")
            continue

        result = run_agent(user_input)

        display_result(result)

