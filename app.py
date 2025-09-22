from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load datasets
students_df = pd.read_csv("students.csv")
companies_df = pd.read_csv("companies.csv")

# Preprocess company dataset
companies_df["combined_features"] = companies_df["skills"].astype(str) + " " + companies_df["location"].astype(str)

# Fit TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
company_tfidf_matrix = vectorizer.fit_transform(companies_df["combined_features"])

# Matching function
def match_internships(student_id, top_n=5):
    student = students_df[students_df["id"] == student_id]
    if student.empty:
        return []

    student_input = student.iloc[0]["skills"] + " " + student.iloc[0]["location"]
    student_vec = vectorizer.transform([student_input])

    cosine_sim = cosine_similarity(student_vec, company_tfidf_matrix).flatten()
    top_indices = cosine_sim.argsort()[-top_n:][::-1]

    results = companies_df.iloc[top_indices][["company", "role", "skills", "location", "description"]].to_dict(orient="records")
    return results

# API routes
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students_df[["id", "name"]].to_dict(orient="records"))

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    student_id = data.get("student_id", 0)
    recommendations = match_internships(student_id)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
