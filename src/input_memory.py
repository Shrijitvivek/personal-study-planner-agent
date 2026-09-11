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


#Returns the current state of the student memory.
def get_student_state(): 
    return student_memory

#Extracts the topic the student wants to study from the user input
def extract_topic(user_input):
    user_input = user_input.lower()
    topics = []
    if "loops" in user_input:
        topics.append("Loops")
    if "functions" in user_input:
        topics.append("Functions")
    if "variables" in user_input:
        topics.append("Variables")
    if "conditions" in user_input:
        topics.append("Conditions")
    return topics

#Extracts the amount of time the student has available to study from the user input.
def extract_time_available(user_input):
    import re
    text = re.sub(r"[^\w\s]", " ", user_input.lower())  # replace punctuation with space

    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    # "half an hour" or "half hour"
    if re.search(r"half.{0,4}hour", text):
        return 30

    # "X hours" or "X hour" (numeric or word)
    match = re.search(r"(\d+|" + "|".join(word_to_num) + r")\s*hours?", text)
    if match:
        val = match.group(1)
        return (word_to_num[val] if val in word_to_num else int(val)) * 60

    # "X minutes" or "X mins" (numeric or word)
    match = re.search(r"(\d+|" + "|".join(word_to_num) + r")\s*(?:minutes?|mins?)", text)
    if match:
        val = match.group(1)
        return word_to_num[val] if val in word_to_num else int(val)

    # bare number (e.g. "plan.20" or "plan 20")
    match = re.search(r"\b(\d+)\b", text)
    if match:
        return int(match.group(1))

    return 0  # Default to 0 if no time is specified

# Extract what the student wants the agent to do.
def extract_intent(user_input):
    user_input = user_input.lower()
    if "what should i study" in user_input or "plan" in user_input:
        return "plan"
    elif "what should i do next" in user_input or "next" in user_input:
        return "next"
    elif "practice" in user_input:
        return "practice"
    elif "dont understand" in user_input or "explain" in user_input:
        return "plan"
    elif "revision" in user_input or "revise" in user_input:
        return "revision"
    else:
        return None  # Default to None if no intent is specified

#Extracts the progress of the student from the user input.
def extract_progress(user_input):
    text = user_input.lower()
    progress = {
        "completed_topics": [],
        "weak_topics": []
    }

    topic_map = {
        "loops": "Loops",
        "functions": "Functions",
        "variables": "Variables",
        "conditions": "Conditions"
    }

    # Check whether the student identifies a topic as weak.
    if "weak" in text:
        for key, topic in topic_map.items():
            if key in text:
                progress["weak_topics"].append(topic)

    # Check whether the student has already studied a topic.
    if "already studied" in text:
        for key, topic in topic_map.items():
            if key in text:
                progress["completed_topics"].append(topic)

    return progress

# Parse the student's input and update their memory.
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
        parsed_input["topics"].extend(topics)
        student_memory["last_studied"] = topics[0]  # update last studied topic

    # Extract the amount of study time available and store it in minutes.
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

    # Store completed and weak topics in the student's memory.
    for topic in progress["completed_topics"]:
        update_progress(topic, "completed") # Update the student's progress for completed topics

    for topic in progress["weak_topics"]:
        update_progress(topic, "weak") # Update the student's progress for weak topics

    # Return all the information extracted from the student's message.
    return parsed_input
