from flask import request, jsonify
from Utils.cosine_similarity import calculate_cosine_similarity
import json

# Load questions from JSON file
with open("QuestionSet.json", "r") as f:
    questions_data = json.load(f)


def recommend_questions():
    # Get user expertise and level from the request
    user_data = request.get_json()  # Add parentheses to actually call the method
    user_expertise = user_data.get("expertise", [])
    user_level = user_data.get("level")

    # Validate input
    if not user_expertise:
        return jsonify({"error": "No expertise provided"}), 400
    if not user_level:
        return jsonify({"error": "No level provided"}), 400

    # Filter questions by level
    filtered_questions = [
        q for q in questions_data if q.get("level") == user_level]

    # Calculate cosine similarity scores for each question
    scored_questions = []
    for question in filtered_questions:
        question_keywords = question["keywords"]
        similarity_score = calculate_cosine_similarity(
            user_expertise, question_keywords)
        scored_questions.append((question["question"], similarity_score))

    # Sort questions by similarity score in descending order and get top 5
    top_questions = sorted(
        scored_questions, key=lambda x: x[1], reverse=True)[:5]
    top_questions_list = [q[0]
                          for q in top_questions]  # Extract only question text

    # Return the top 5 questions
    return jsonify({"recommended_questions": top_questions_list}), 200
