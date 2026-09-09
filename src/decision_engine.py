"""
Personal Study Planner Agent
Part 2 - Decision Engine

This file is the "brain" of the agent. It looks at:
    - parsed_input   -> structured facts from input_memory.py
    - student_memory -> the student's learning history

...and decides WHICH tool from tools.py should be called, and
for WHICH topic. It never builds study content itself -- that
job belongs to tools.py.


"""

from tools import create_study_plan, give_practice_questions, give_revision_task



# CURRICULUM ORDER & TOPIC IMPORTANCE


# The order topics are normally learned in. Used to figure out
# "what's next" when the student hasn't named a topic.
CURRICULUM_ORDER = ["Variables", "Conditions", "Loops", "Functions"]

# A simple 1-5 importance rating per topic. Used only for the
# priority score (Optional Extension).
TOPIC_IMPORTANCE = {
    "Variables": 3,
    "Conditions": 3,
    "Loops": 4,
    "Functions": 5
}



# PRIORITY SCORE  (Optional Extension)
#   priority = Weakness + Topic Importance + Time Fit

def calculate_priority_score(topic, student_memory, time_available):
    """
    Scores how urgently a topic should be studied right now.

    - Weakness  : +5 if the topic is a known weak topic, else 0
    - Importance: the topic's fixed importance rating (1-5)
    - Time Fit  : rewards having enough time to actually study
                  the topic properly (more time = higher fit)
    """

    weakness_score = 5 if topic in student_memory.get("weak_topics", []) else 0
    importance_score = TOPIC_IMPORTANCE.get(topic, 1)

    if time_available >= 60:
        time_fit_score = 3
    elif time_available >= 30:
        time_fit_score = 2
    elif time_available > 0:
        time_fit_score = 1
    else:
        time_fit_score = 0

    return weakness_score + importance_score + time_fit_score


def rank_candidate_topics(candidate_topics, student_memory, time_available):
    """
    Sorts a list of topics from highest to lowest priority score.
    Returns a list of (topic, score) tuples.
    """
    scored = [
        (topic, calculate_priority_score(topic, student_memory, time_available))
        for topic in candidate_topics
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored



# "WHAT SHOULD I STUDY NEXT?" LOGIC


def decide_next_topic(student_memory, time_available=30):
    """
    Picks a topic when the student hasn't named one, using memory.

    Priority order:
        1. Any weak topic that isn't completed yet (highest score first)
        2. The next topic in curriculum order that isn't completed
        3. None, if everything is completed
    """

    completed = student_memory.get("completed_topics", [])
    weak = student_memory.get("weak_topics", [])

    pending_weak = [t for t in weak if t not in completed]
    if pending_weak:
        ranked = rank_candidate_topics(pending_weak, student_memory, time_available)
        return ranked[0][0]

    for topic in CURRICULUM_ORDER:
        if topic not in completed:
            return topic

    return None  # everything completed


# MAIN DECISION LOGIC


def decide_action(parsed_input, student_memory):
    """
    The single entry point the rest of the agent should call.

    Returns whatever dictionary the chosen tool returns, e.g.:
        {"tool": "give_practice_questions", "status": "success", ...}
    """

    intent = parsed_input.get("intent")
    topics = parsed_input.get("topics", [])
    time_available = parsed_input.get("time_available", 0)
    weak_topics_mentioned = parsed_input.get("weak_topics", [])
    completed_topics_mentioned = parsed_input.get("completed_topics", [])

    
    # STEP 0a - Reject inputs with no actionable signal at all.
    
    if (
        not topics
        and intent is None
        and time_available <= 0
        and not weak_topics_mentioned
        and not completed_topics_mentioned
    ):
        return {
            "tool": None,
            "status": "clarification_needed",
            "message": (
                "I couldn't tell what you'd like help with. Could you "
                "let me know a subject/topic, how much time you have, "
                "or whether you'd like a study plan, practice questions, "
                "or a revision task?"
            )
        }

 
    # STEP 0b - Reject "action words with no real topic".
   
    TOPIC_REQUIRED_INTENTS = {"practice", "revision", "explain", "plan"}

    if not topics and intent in TOPIC_REQUIRED_INTENTS:
        return {
            "tool": None,
            "status": "clarification_needed",
            "message": (
                f"Sure, I can help with that — which topic would you like "
                f"{intent} for? For example: Variables, Conditions, Loops, "
                f"or Functions."
            )
        }

    
    # STEP 1 - Resolve the topic.
   
    if not topics:
        next_topic = decide_next_topic(student_memory, time_available)

        if next_topic is None:
            return {
                "tool": None,
                "status": "success",
                "message": "All tracked topics are completed. Nice work!"
            }

        # Don't mutate the caller's dict - work on a copy.
        parsed_input = dict(parsed_input)
        parsed_input["topics"] = [next_topic]

    topic = parsed_input["topics"][0]

    is_completed = topic in student_memory.get("completed_topics", [])
    is_weak = (
        topic in student_memory.get("weak_topics", [])
        or topic in parsed_input.get("weak_topics", [])
    )

   
    # STEP 2 - Explicit intent wins first.
    # If the student directly asked for something, honor it.
   

    if intent == "practice":
        return give_practice_questions(parsed_input, student_memory)

    if intent == "revision":
        return give_revision_task(parsed_input, student_memory)

    if intent == "explain":
        # There's no dedicated "explain" tool, so a full study
        # plan (which opens with Concept Review) covers the
        # "I don't understand X" case.
        return create_study_plan(parsed_input, student_memory)

    if intent == "plan":
        return create_study_plan(parsed_input, student_memory)

    if intent == "next":
        return _route_completed_or_weak(topic, is_completed, is_weak,
                                         time_available, parsed_input, student_memory)

    # STEP 3 - No explicit intent given.
    # Infer the best action from the topic's status + time.
   

    # Already completed -> revise instead of re-learning from scratch.
    if is_completed:
        return give_revision_task(parsed_input, student_memory)

    # Known weak topic -> needs a full plan (concept + heavy practice),
    
    if is_weak:
        if time_available <= 0:
            return give_revision_task(parsed_input, student_memory)
        return create_study_plan(parsed_input, student_memory)

    # Very little time -> don't hand out a full plan, just practice.
    if 0 < time_available <= 20:
        return give_practice_questions(parsed_input, student_memory)

    # New topic with a reasonable amount of time -> full study plan.
    if time_available > 0:
        return create_study_plan(parsed_input, student_memory)

    # Nothing else to go on -> safe, low-effort default.
    return give_practice_questions(parsed_input, student_memory)


def _route_completed_or_weak(topic, is_completed, is_weak, time_available,
                              parsed_input, student_memory):
    """
    Sub-rule used when intent == "next" (i.e. memory picked the topic).

    - Completed, non-weak topic -> revision task (light, no time needed).
    - Weak or new topic, WITH time available -> full study plan.
    - Weak or new topic, WITH NO time available -> create_study_plan
      would fail (it requires time_available > 0), so fall back to
      practice questions for weak topics, or a revision task otherwise.
    """
    if is_completed and not is_weak:
        return give_revision_task(parsed_input, student_memory)

    if time_available <= 0:
        if is_weak:
            return give_practice_questions(parsed_input, student_memory)
        return give_revision_task(parsed_input, student_memory)

    return create_study_plan(parsed_input, student_memory)

# BASIC DECISION ENGINE TESTING


if __name__ == "__main__":

    from input_memory import student_memory, update_progress

    # Simulate prior progress, matching the assignment's example memory:
    #   Completed: Variables, Conditions, Loops | Weak: Functions
    update_progress("Variables", "completed")
    update_progress("Conditions", "completed")
    update_progress("Loops", "completed")
    update_progress("Functions", "weak")

    test_cases = [
        {
            "description": "\"I don't understand loops\" -> should explain/plan Loops",
            "parsed_input": {
                "topics": ["Loops"], "time_available": 45,
                "weak_topics": [], "intent": "explain", "completed_topics": []
            }
        },
        {
            "description": "\"I understand loops, give me practice\" -> practice questions",
            "parsed_input": {
                "topics": ["Loops"], "time_available": 30,
                "weak_topics": [], "intent": "practice", "completed_topics": []
            }
        },
        {
            "description": "\"I have 2 hours and I'm weak in Functions\" -> full study plan",
            "parsed_input": {
                "topics": ["Functions"], "time_available": 120,
                "weak_topics": ["Functions"], "intent": None, "completed_topics": []
            }
        },
        {
            "description": "\"I already studied loops, what should I do next?\" -> uses memory",
            "parsed_input": {
                "topics": [], "time_available": 30,
                "weak_topics": [], "intent": "next", "completed_topics": ["Loops"]
            }
        },
        {
            "description": "\"I only have 15 minutes\" (no topic) -> light action via memory",
            "parsed_input": {
                "topics": [], "time_available": 15,
                "weak_topics": [], "intent": None, "completed_topics": []
            }
        },
        {
            "description": "\"What should I study next?\" with everything done",
            "parsed_input": {
                "topics": [], "time_available": 30,
                "weak_topics": [], "intent": "next", "completed_topics": []
            }
        },
        {
            "description": "\"What is a computer?\" -> unrelated input, should ask for clarification",
            "parsed_input": {
                "topics": [], "time_available": 0,
                "weak_topics": [], "intent": None, "completed_topics": []
            }
        },
        {
            "description": "\"What should I do next?\" with NO time given -> must not crash",
            "parsed_input": {
                "topics": [], "time_available": 0,
                "weak_topics": [], "intent": "next", "completed_topics": []
            }
        },
    ]

    for case in test_cases:
        print("\n" + "=" * 70)
        print(case["description"])
        print("=" * 70)
        result = decide_action(case["parsed_input"], student_memory)
        print(result)