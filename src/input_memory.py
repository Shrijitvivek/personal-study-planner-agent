"""This file handles understanding the user input 
and storing it in memory for future reference."""


"""A dictionary to store the student's progress and memory."""
student_memory = {
    "completed_topics": [],
    "weak_topics": [],
    "last_studied": None
}

 # Update the progress of the student
def update_progress(topic,status): 
    if status == "completed":
        if topic not in student_memory["completed_topics"]: 
            student_memory["completed_topics"].append(topic)
    elif status == "weak":
        if topic not in student_memory["weak_topics"]:
            student_memory["weak_topics"].append(topic)
    student_memory["last_studied"] = topic # Update the last studied topic

update_progress("Loops", "completed")
update_progress("Functions", "weak")

print(student_memory)


"""Returns the current state of the student memory."""
def get_student_state(): 
    return student_memory

print(get_student_state())




"""Parses the user input and updates the parsed_input dictionary."""
def parse_user_input(user_input):

    parsed_input = {
        "topics": [],
        "time_available": 0,
        "weak_topics": [],
        "intent": None,
        "completed_topics": []
    }

    if "loops" in user_input.lower():
        parsed_input["topics"].append("Loops")

    if "30 minutes" in user_input.lower():
        parsed_input["time_available"] = 30

    if "practice" in user_input.lower():
        parsed_input["intent"] = "practice"

    if "dont understand" in user_input.lower():
        parsed_input["intent"] = "explain"

    if "revision" in user_input.lower():
        parsed_input["intent"] = "revision"

    return parsed_input
print(parse_user_input("I already studied loops. Give me a revision task."))