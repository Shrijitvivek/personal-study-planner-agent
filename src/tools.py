"""
Personal Study Planner Agent
Part 3 - Tools / Actions

This file contains the actions that can be triggered by the
Decision Engine (Part 2).

Tools:
    1. create_study_plan()
    2. give_practice_questions()
    3. give_revision_task()

The Decision Engine is responsible for deciding which tool
should be called.
"""


# ============================================================
# STUDY MATERIAL
# ============================================================

QUESTION_BANK = {

    "Loops": [
        "What is the difference between a for loop and a while loop?",
        "Write a Python program to print numbers from 1 to 10.",
        "Write a Python program to print all even numbers from 1 to 20.",
        "Write a Python program to calculate the sum of numbers from 1 to 100.",
        "Write a Python program to print the multiplication table of a number."
    ],

    "Functions": [
        "What is a function in Python?",
        "What is the difference between a parameter and an argument?",
        "Write a function to calculate the square of a number.",
        "Write a function that returns the largest of two numbers.",
        "What is the purpose of the return statement?"
    ],

    "Variables": [
        "What is a variable in Python?",
        "What is the difference between int, float and string?",
        "Write a Python program to swap two variables.",
        "How can you change the value stored in a variable?",
        "Create variables to store a student's name, age and CGPA."
    ],

    "Conditions": [
        "What is the purpose of an if statement?",
        "What is the difference between if, elif and else?",
        "Write a program to check whether a number is positive, negative or zero.",
        "Write a program to find the largest of three numbers.",
        "Write a program to check whether a student has passed or failed."
    ]
}


# ============================================================
# TOOL 1 - CREATE STUDY PLAN
# ============================================================

def create_study_plan(parsed_input, student_memory):
    """
    Creates a study plan based on available study time
    and the student's weak topics.
    """

    topics = parsed_input.get("topics", [])
    time_available = parsed_input.get("time_available", 0)
    weak_topics = parsed_input.get("weak_topics", [])

    # Check whether a topic was identified
    if not topics:
        return {
            "tool": "create_study_plan",
            "status": "failed",
            "message": "No study topic was identified."
        }

    # Check whether study time was provided
    if time_available <= 0:
        return {
            "tool": "create_study_plan",
            "status": "failed",
            "message": "Available study time was not provided."
        }

    topic = topics[0]

    # Give more practice time to weak topics
    if (
        topic in weak_topics
        or topic in student_memory.get("weak_topics", [])
    ):
        concept_time = int(time_available * 0.25)
        practice_time = int(time_available * 0.55)
        revision_time = time_available - concept_time - practice_time

    else:
        concept_time = int(time_available * 0.35)
        practice_time = int(time_available * 0.40)
        revision_time = time_available - concept_time - practice_time

    plan = [
        {
            "activity": "Concept Review",
            "duration": concept_time,
            "task": f"Review the important concepts of {topic}."
        },
        {
            "activity": "Practice",
            "duration": practice_time,
            "task": f"Solve practice questions on {topic}."
        },
        {
            "activity": "Revision",
            "duration": revision_time,
            "task": f"Quickly revise the concepts learned in {topic}."
        }
    ]

    return {
        "tool": "create_study_plan",
        "status": "success",
        "topic": topic,
        "time_available": time_available,
        "plan": plan
    }


# ============================================================
# TOOL 2 - GIVE PRACTICE QUESTIONS
# ============================================================

def give_practice_questions(parsed_input, student_memory):
    """
    Provides practice questions for the selected topic.

    Weak topics receive more questions.
    """

    topics = parsed_input.get("topics", [])
    weak_topics = parsed_input.get("weak_topics", [])

    # Check whether a topic was identified
    if not topics:
        return {
            "tool": "give_practice_questions",
            "status": "failed",
            "message": "No topic was identified for practice."
        }

    topic = topics[0]

    # Check whether questions exist for the topic
    if topic not in QUESTION_BANK:
        return {
            "tool": "give_practice_questions",
            "status": "failed",
            "message": f"No practice questions are available for {topic}."
        }

    questions = QUESTION_BANK[topic]

    # Give more questions if the topic is weak
    if (
        topic in weak_topics
        or topic in student_memory.get("weak_topics", [])
    ):
        selected_questions = questions

    else:
        selected_questions = questions[:3]

    return {
        "tool": "give_practice_questions",
        "status": "success",
        "topic": topic,
        "questions": selected_questions
    }


# ============================================================
# TOOL 3 - GIVE REVISION TASK
# ============================================================

def give_revision_task(parsed_input, student_memory):
    """
    Creates a short revision task for a topic.

    If no topic is provided, the last studied topic from
    student memory is used.
    """

    topics = parsed_input.get("topics", [])

    # Use the last studied topic if no topic was identified
    if not topics:

        last_studied = student_memory.get("last_studied")

        if last_studied:
            topic = last_studied

        else:
            return {
                "tool": "give_revision_task",
                "status": "failed",
                "message": "No topic is available for revision."
            }

    else:
        topic = topics[0]

    revision_task = {
        "topic": topic,

        "recall": (
            f"Explain the main concepts of {topic} "
            "without looking at your notes."
        ),

        "practice": (
            f"Solve any 2 questions related to {topic}."
        ),

        "self_test": (
            f"Write down 3 important points you remember "
            f"about {topic}."
        ),

        "duration": 15
    }

    return {
        "tool": "give_revision_task",
        "status": "success",
        "revision_task": revision_task
    }


# ============================================================
# BASIC TOOL TESTING
# ============================================================

if __name__ == "__main__":

    # Sample structured input received from Part 1
    parsed_input = {
        "topics": ["Loops"],
        "time_available": 30,
        "weak_topics": [],
        "intent": "practice",
        "completed_topics": []
    }

    # Sample student memory received from Part 1
    student_memory = {
        "completed_topics": ["Loops"],
        "weak_topics": ["Functions"],
        "last_studied": "Functions"
    }


    # ========================================================
    # TOOL 1 OUTPUT
    # ========================================================

    result = create_study_plan(
        parsed_input,
        student_memory
    )

    print("\n" + "=" * 60)
    print("                  STUDY PLAN")
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


    # ========================================================
    # TOOL 2 OUTPUT
    # ========================================================

    result = give_practice_questions(
        parsed_input,
        student_memory
    )

    print("\n" + "=" * 60)
    print("               PRACTICE QUESTIONS")
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


    # ========================================================
    # TOOL 3 OUTPUT
    # ========================================================

    result = give_revision_task(
        parsed_input,
        student_memory
    )

    print("\n" + "=" * 60)
    print("                 REVISION TASK")
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

    print("\n" + "=" * 60)
