import json


def load_assessments():
    with open("catalog/assessments.json", "r", encoding="utf-8") as f:
        return json.load(f)


def search_assessments(query):

    assessments = load_assessments()

    keywords = query.lower().split()

    scored = []

    for assessment in assessments:

        searchable = " ".join([

            assessment.get("name", ""),

            assessment.get("description", ""),

            " ".join(assessment.get("keys", [])),

            " ".join(assessment.get("job_levels", [])),

            assessment.get("duration", ""),

            assessment.get("remote", ""),

            assessment.get("adaptive", "")

        ]).lower()

        score = 0

        for keyword in keywords:

            if keyword in searchable:
                score += 3

            if keyword in assessment.get("name", "").lower():
                score += 5

        if score > 0:
            scored.append((score, assessment))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [item[1] for item in scored]