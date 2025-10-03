from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Load datasets (CSV)
students_df = pd.read_csv("Student_intership.csv")
companies_df = pd.read_csv("Company_internship.csv")

# Normalize column names
students_df.columns = students_df.columns.str.strip().str.lower()
companies_df.columns = companies_df.columns.str.strip().str.lower()

# Preprocess company dataset
companies_df["combined_features"] = (
    companies_df["skills"].astype(str) + " " + companies_df["location"].astype(str)
)

# Fit TF-IDF on companies
vectorizer = TfidfVectorizer(stop_words="english")
company_tfidf_matrix = vectorizer.fit_transform(companies_df["combined_features"])

# Function: match by skills + location (instead of student_id)
def get_recommendations(skills, location, top_n=5):
    if not skills and not location:
        return []

    # Combine student input
    student_input = f"{skills} {location}"
    student_vec = vectorizer.transform([student_input])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(student_vec, company_tfidf_matrix).flatten()
    top_indices = cosine_sim.argsort()[-top_n:][::-1]

    results = companies_df.iloc[top_indices][
        ["company_name", "job_title", "skills", "location", "job_description"]
    ].to_dict(orient="records")

    return results

# Old API (keep if needed)
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students_df[["student_id", "name"]].to_dict(orient="records"))

# New API for frontend
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    name = data.get("name")
    skills = data.get("skills", "")
    location = data.get("location", "")

    recommendations = get_recommendations(skills, location)

    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
