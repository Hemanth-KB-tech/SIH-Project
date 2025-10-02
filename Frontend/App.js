import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  // Load students only once (no dependency loop!)
  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/students")
      .then((res) => {
        if (Array.isArray(res.data)) {
          setStudents(res.data);
        } else {
          console.error("Unexpected response:", res.data);
        }
      })
      .catch((err) => console.error("Error fetching students:", err));
  }, []); // ✅ runs only once

  // Handle form submit
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedStudent) return;

    axios
      .post("http://127.0.0.1:5000/recommend", {
        student_id: parseInt(selectedStudent, 10),
      })
      .then((res) => {
        if (Array.isArray(res.data)) {
          setRecommendations(res.data);
        } else {
          console.error("Unexpected response:", res.data);
        }
      })
      .catch((err) => console.error("Error fetching recommendations:", err));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>🎓 Student Internship Matcher</h2>

      <form onSubmit={handleSubmit}>
        <select
          value={selectedStudent}
          onChange={(e) => setSelectedStudent(e.target.value)}
        >
          <option value="">-- Select a student --</option>
          {students.map((student) => (
            <option key={student.student_id} value={student.student_id}>
              {student.name} (ID: {student.student_id})
            </option>
          ))}
        </select>
        <button type="submit" style={{ marginLeft: "10px" }}>
          Find Internships
        </button>
      </form>

      <h3 style={{ marginTop: "20px" }}>Recommended Internships:</h3>
      {recommendations.length === 0 ? (
        <p>No recommendations yet. Select a student above.</p>
      ) : (
        <table border="1" cellPadding="5" style={{ marginTop: "10px" }}>
          <thead>
            <tr>
              <th>Company</th>
              <th>Role</th>
              <th>Skills</th>
              <th>Location</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {recommendations.map((rec, idx) => (
              <tr key={idx}>
                <td>{rec.company_name}</td>
                <td>{rec.job_title}</td>
                <td>{rec.skills}</td>
                <td>{rec.location}</td>
                <td>{rec.job_description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;

