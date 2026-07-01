from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from agent.retriever import search_assessments
from agent.compare import compare_assessments

app = FastAPI(title="SHL Assessment Recommender")


# -----------------------------
# Models
# -----------------------------
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------
# Health Endpoint
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    conversation = " ".join(
        message.content for message in request.messages
    ).lower()

    # ---------------------------------
    # Handle refinement requests
    # ---------------------------------
    if "personality" in conversation:

        personality_results = (
            search_assessments("OPQ") +
            search_assessments("personality") +
            search_assessments("behaviour") +
            search_assessments("behavior")
        )

        # Remove duplicates
        unique = []
        seen = set()

        for assessment in personality_results:
            entity_id = assessment.get("entity_id")

            if entity_id not in seen:
                seen.add(entity_id)
                unique.append(assessment)

        return {
            "reply": "I've updated the recommendations to include personality assessments.",
            "recommendations": unique[:10],
            "end_of_conversation": False
        }

    # ---------------------------------
    # Handle comparison requests
    # ---------------------------------
    if "compare" in conversation and "and" in conversation:

        try:
            text = conversation.replace("compare", "").strip()

            parts = text.split("and")

            if len(parts) >= 2:
                name1 = parts[0].strip()
                name2 = parts[1].strip()

                result = compare_assessments(name1, name2)

                if result:
                    return result

        except Exception:
            pass

    # ---------------------------------
    # Clarification
    # ---------------------------------
    vague_queries = [
        "assessment",
        "test",
        "i need an assessment",
        "i need a test",
        "recommend an assessment"
    ]

    if conversation.strip() in vague_queries:
        return {
            "reply": "Sure! What role are you hiring for? For example, Java Developer, Sales Manager, Graduate, or Customer Support.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # ---------------------------------
    # Recommendations
    # ---------------------------------
    recommendations = search_assessments(conversation)

    if recommendations:
        return {
            "reply": "Here are the SHL assessments that best match your request.",
            "recommendations": recommendations[:10],
            "end_of_conversation": False
        }

    # ---------------------------------
    # No Match
    # ---------------------------------
    return {
        "reply": "I couldn't find a matching SHL assessment. Could you tell me more about the role, required skills, or seniority level?",
        "recommendations": [],
        "end_of_conversation": False
    }