from .retriever import load_assessments


def compare_assessments(name1, name2):

    assessments = load_assessments()

    a1 = None
    a2 = None

    for assessment in assessments:

        if name1.lower() in assessment["name"].lower():
            a1 = assessment

        if name2.lower() in assessment["name"].lower():
            a2 = assessment

    if not a1 or not a2:
        return None

    return {
        "reply": f"""Comparison:

Assessment 1:
Name: {a1['name']}
Type: {a1['test_type']}
Duration: {a1['duration']}
Description: {a1['description']}

Assessment 2:
Name: {a2['name']}
Type: {a2['test_type']}
Duration: {a2['duration']}
Description: {a2['description']}
""",
        "recommendations": [],
        "end_of_conversation": False
    }