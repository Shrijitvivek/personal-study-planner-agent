from src.input_memory import parse_user_input, get_student_state


# Check whether the parser understands weak and completed topics.
print("Test 1")
result = parse_user_input(
    "I am weak in functions but I already studied loops"
)
print(result)

 
# Check whether the parser understands study time.
print("Test 2")
result = parse_user_input(
    "I have 1 hour to study"
)
print(result)


# Check whether the parser remembers the student's progress.
print("Test 3")
result = parse_user_input(
    "I am weak in functions but I already studied loops"
)
print(get_student_state())
