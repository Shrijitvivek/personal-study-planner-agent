"""This file handles understanding the user input 
and storing it in memory for future reference."""


#A dictionary to store the student's progress and memory.
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

"""update_progress("Loops", "completed")
update_progress("Functions", "weak")"""

print(student_memory)


#Returns the current state of the student memory.
def get_student_state(): 
    return student_memory

print(get_student_state())

#Extracts the topic the student wants to study from the user input
def extract_topic(user_input):
    user_input = user_input.lower()
    topics = [] # List to store the topics
    if "loops" in user_input: 
        topics.append("Loops") 
    if "functions" in user_input:
        topics.append("Functions") 
    return topics

#Extracts the amount of time the student has available to study from the user input.
def extract_time_available(user_input):
    user_input = user_input.lower()
    if "30 minutes" in user_input:
        return 30
    elif "1 hour" in user_input:
        return 60
    elif "2 hours" in user_input:
        return 120
    else:
        return 0  # Default to 0 if no time is specified

def extract_intent(user_input):
    user_input = user_input.lower()
    if "what should i study" in user_input:
        return "plan"
    elif "what should i do next" in user_input:
        return "next"
    elif "practice" in user_input:
        return "practice"
    elif "dont understand" in user_input:
        return "explain"
    elif "revision" in user_input:
        return "revision"
    else:
        return None  # Default to None if no intent is specified

#Extracts the progress of the student from the user input.
def extract_progress(user_input):
    user_input = user_input.lower()
    progress ={
       "completed_topics": [],
       "weak_topics": [],
   }
    # Check whether the student identifies a topic as weak.
    if "weak" in user_input:
        if "functions" in user_input:
            progress["weak_topics"].append("Functions")

    # Check whether the student has already studied a topic.
    if "already studied" in user_input:
        if "already studied loops" in user_input:
            progress["completed_topics"].append("Loops")

        if "already studied functions" in user_input:
            progress["completed_topics"].append("Functions")

    return progress

#Parses the user input and updates the parsed_input dictionary.
def parse_user_input(user_input):
    

    # Create a fresh dictionary for every new user message.
    # This prevents information from an earlier message from carrying over.
    parsed_input = {
        "topics": [],
        "time_available": 0,
        "weak_topics": [],
        "intent": None,
        "completed_topics": []
    }

    # Extract the topic the student wants to study.
    topics = extract_topic(user_input) 
    if topics:
        parsed_input["topics"].extend(topics) # Extend the topics list 

    # Extract the amount of study time availablea and store it in minutes.
    time_available = extract_time_available(user_input)
    if time_available:
        parsed_input["time_available"] = time_available

    # Identify what the student wants the agent to do.
    intent = extract_intent(user_input)
    if intent:
        parsed_input["intent"] = intent

    # Extract the progress of the student from the user input.
    progress = extract_progress(user_input)
    if progress:
        parsed_input["completed_topics"] = progress["completed_topics"]
        parsed_input["weak_topics"] = progress["weak_topics"]

    # Return all the information extracted from the student's message.
    return parsed_input

print(parse_user_input("I am weak in functions but I already studied loops"))