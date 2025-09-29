import pandas as pd
from typing import List, Dict

# -------------------------------
# Internship Dataset (company requirements)
# -------------------------------
internships = [
    {"id": 1, "title": "Data Analyst Intern", "sector": "Data", "skills": ["Python", "SQL", "Excel"], "location": "Delhi", "education": "Undergraduate"},
    {"id": 2, "title": "Marketing Intern", "sector": "Marketing", "skills": ["Communication", "Creativity"], "location": "Mumbai", "education": "Any"},
    {"id": 3, "title": "Software Development Intern", "sector": "IT", "skills": ["Python", "Java", "Problem Solving"], "location": "Bangalore", "education": "Undergraduate"},
    {"id": 4, "title": "Research Intern", "sector": "Research", "skills": ["Writing", "Data Analysis"], "location": "Hyderabad", "education": "Postgraduate"},
    {"id": 5, "title": "Finance Intern", "sector": "Finance", "skills": ["Excel", "Accounting", "Analysis"], "location": "Delhi", "education": "Undergraduate"},
    {"id": 6, "title": "Social Media Intern", "sector": "Digital Marketing", "skills": ["Creativity", "Content Writing"], "location": "Remote", "education": "Any"},
]
intern_df = pd.DataFrame(internships)

# -------------------------------
# Student Dataset
# -------------------------------
students = [
    {"id": "S1", "name": "Amit", "education": "Undergraduate", "skills": ["Python", "SQL"], "preferred_sector": "Data", "preferred_location": "Delhi"},
    {"id": "S2", "name": "Sana", "education": "Undergraduate", "skills": ["Communication", "Creativity"], "preferred_sector": "Marketing", "preferred_location": "Mumbai"},
    {"id": "S3", "name": "Rahul", "education": "Postgraduate", "skills": ["Writing", "Data Analysis"], "preferred_sector": "Research", "preferred_location": "Hyderabad"},
    {"id": "S4", "name": "Neha", "education": "Undergraduate", "skills": ["Java", "Problem Solving"], "preferred_sector": "IT", "preferred_location": "Bangalore"},
]
student_df = pd.DataFrame(students)

# -------------------------------
# Scoring / Matching utilities
# -------------------------------
def education_compatible(student_edu: str, req_edu: str) -> int:
    # 'Any' accepts any education; otherwise exact equality required
    if req_edu.lower() == "any":
        return 1
    return 1 if student_edu.lower() == req_edu.lower() else 0

def skills_coverage(student_skills: List[str], required_skills: List[str]) -> float:
    req = set(s.lower() for s in required_skills)
    if not req:
        return 1.0
    stu = set(s.lower() for s in student_skills)
    covered = len(req & stu)
    return covered / len(req)

def location_match(student_loc: str, intern_loc: str) -> int:
    # Remote positions accept any location. Exact match otherwise.
    if intern_loc.lower() == "remote" or student_loc.lower() == "remote":
        return 1
    return 1 if student_loc.lower() == intern_loc.lower() else 0

def sector_match(student_sector: str, intern_sector: str) -> int:
    return 1 if student_sector.lower() == intern_sector.lower() else 0

def compute_match_score(student: Dict, internship: Dict, weights: Dict = None) -> Dict:
    """
    Compute detailed match info and combined score (0-100).
    weights: dict with keys 'skills','education','sector','location'
    """
    if weights is None:
        weights = {"skills": 0.6, "education": 0.2, "sector": 0.15, "location": 0.05}

    scov = skills_coverage(student["skills"], internship["skills"])
    edu = education_compatible(student["education"], internship["education"])
    sec = sector_match(student["preferred_sector"], internship["sector"])
    loc = location_match(student["preferred_location"], internship["location"])

    total = (weights["skills"] * scov +
             weights["education"] * edu +
             weights["sector"] * sec +
             weights["location"] * loc)

    return {
        "intern_id": internship["id"],
        "title": internship["title"],
        "sector": internship["sector"],
        "location": internship["location"],
        "required_skills": internship["skills"],
        "skill_coverage_pct": round(scov * 100, 2),
        "education_match": bool(edu),
        "sector_match": bool(sec),
        "location_match": bool(loc),
        "score_pct": round(total * 100, 2)
    }

def recommend_internships_for_student(student: Dict, internships_list: List[Dict], top_n: int = 2, weights: Dict = None) -> List[Dict]:
    scored = []
    for _, intern in pd.DataFrame(internships_list).iterrows():
        info = compute_match_score(student, intern.to_dict(), weights=weights)
        scored.append(info)
    scored_sorted = sorted(scored, key=lambda x: x["score_pct"], reverse=True)
    return scored_sorted[:top_n]

# -------------------------------
# Helper to recommend for all students and print results
# -------------------------------
def recommend_all_students(student_df: pd.DataFrame, intern_df: pd.DataFrame, top_n: int = 2, weights: Dict = None):
    print("\n--- Internships Dataset ---")
    print(intern_df.to_string(index=False))
    print("\n--- Students Dataset ---")
    print(student_df.to_string(index=False))

    for _, student in student_df.iterrows():
        print("\n" + "="*60)
        print(f"Recommendations for {student['name']} (Education: {student['education']}, Skills: {student['skills']}, Preferred Sector: {student['preferred_sector']}, Preferred Location: {student['preferred_location']})")
        recs = recommend_internships_for_student(student.to_dict(), internships, top_n=top_n, weights=weights)
        for r in recs:
            print(f"- {r['title']} | Sector: {r['sector']} | Location: {r['location']} | Match Score: {r['score_pct']}%")
            print(f"  -> Skill coverage: {r['skill_coverage_pct']}% | Education match: {r['education_match']} | Sector match: {r['sector_match']} | Location match: {r['location_match']}")
        # Also print top matching internship across all (optional)
        all_matches = [compute_match_score(student.to_dict(), i, weights=weights) for i in internships]
        best = max(all_matches, key=lambda x: x["score_pct"])
        print(f"Best overall match: {best['title']} ({best['score_pct']}%)")
    print("\nDone.\n")

# -------------------------------
# Run in console
# -------------------------------
if _name_ == "_main_":
    # You can tune weights here if you want to favor skills vs education vs sector vs location
    weights = {"skills": 0.6, "education": 0.2, "sector": 0.15, "location": 0.05}
    recommend_all_students(student_df, intern_df, top_n=2, weights=weights)
