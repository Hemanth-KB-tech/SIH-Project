import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  // Load students on mount
  useEffect(() => {
    axios.get("http://127.0.0.1:5000/students")
      .then(res => setStudents(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedStudent) return;

    axios.post("http://127.0.0.1:5000/recommend", { student_id: parseInt(selectedStudent) })
      .then(res => setRecommendations(res.data))
      .catch(err => console.error(err));
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Student Internship Matcher</h2>
      <form onSubmit={handleSubmit}>
        <select value={selectedStudent} onChange={(e) => setSelectedStudent(e.target.value)}>
          <option value="">Select a student</option>
          {students.map(student => (
            <option key={student.id} value={student.id}>{student.name}</option>
          ))}
        </select>
        <button type="submit" style={{ marginLeft: "10px" }}>Find Internships</button>
      </form>

      <h3>Recommendations:</h3>
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
              <td>{rec.company}</td>
              <td>{rec.role}</td>
              <td>{rec.skills}</td>
              <td>{rec.location}</td>
              <td>{rec.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
