import React, { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [formData, setFormData] = useState({
    name: "",
    skills: "",
    location: "",
  });
  const [recommendations, setRecommendations] = useState([]);

  // handle form input changes
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // submit student details
  const handleSubmit = (e) => {
    e.preventDefault();

    axios
      .post("http://127.0.0.1:5000/recommend", formData)
      .then((res) => {
        if (Array.isArray(res.data)) setRecommendations(res.data);
        else console.error("Unexpected response:", res.data);
      })
      .catch((err) => console.error("Error fetching recommendations:", err));
  };

  return (
    <div
      className="min-vh-100 d-flex flex-column justify-content-center align-items-center"
      style={{
        background: "linear-gradient(135deg, #74ebd5, #ACB6E5)",
        fontFamily: "Arial, sans-serif",
        padding: "20px",
      }}
    >
      <div className="container" style={{ maxWidth: "900px" }}>
        <div className="text-center mb-5">
          <h1 className="text-white fw-bold">🎓 Student Internship Matcher</h1>
          <p className="text-light">
            Enter your details to find the best internships for your skills and location
          </p>
        </div>

        {/* Student Details Form */}
        <form className="row g-3 mb-4" onSubmit={handleSubmit}>
          <div className="col-md-4">
            <input
              type="text"
              className="form-control"
              name="name"
              placeholder="Your Name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="col-md-4">
            <input
              type="text"
              className="form-control"
              name="skills"
              placeholder="Your Skills (comma separated)"
              value={formData.skills}
              onChange={handleChange}
              required
            />
          </div>
          <div className="col-md-4">
            <input
              type="text"
              className="form-control"
              name="location"
              placeholder="Preferred Location"
              value={formData.location}
              onChange={handleChange}
              required
            />
          </div>
          <div className="col-12 text-center">
            <button type="submit" className="btn btn-primary">
              Find Internships
            </button>
          </div>
        </form>

        {/* Recommendations */}
        <h3 className="text-white mb-4">Recommended Internships:</h3>

        {recommendations.length === 0 ? (
          <p className="text-light">No recommendations yet. Enter your details above.</p>
        ) : (
          <div className="row">
            {recommendations.map((rec, idx) => (
              <div key={idx} className="col-md-6 mb-4">
                <div className="card shadow-sm h-100">
                  <div className="card-body">
                    <h5 className="card-title">{rec.company_name}</h5>
                    <h6 className="card-subtitle mb-2 text-muted">{rec.job_title}</h6>
                    <p className="card-text">
                      <strong>Skills:</strong> {rec.skills} <br />
                      <strong>Location:</strong> {rec.location} <br />
                      <strong>Description:</strong> {rec.job_description}
                    </p>
                    <a href="#" className="btn btn-outline-primary btn-sm">
                      Apply Now
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
