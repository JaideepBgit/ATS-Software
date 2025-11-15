import React, { useState, useEffect } from 'react';
import './JobTracking.css';

function JobTracking({ companyName, roleName, onClose }) {
  const [applications, setApplications] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    company: companyName || '',
    job_title: roleName || '',
    portal: 'LinkedIn',
    employment_type: 'Full Time'
  });
  const [alreadyApplied, setAlreadyApplied] = useState(false);

  useEffect(() => {
    loadApplications();
    loadStatistics();
    if (companyName && roleName) {
      checkIfApplied(companyName, roleName);
    }
  }, [companyName, roleName]);

  const loadApplications = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/job-applications');
      const data = await response.json();
      setApplications(data.applications || []);
    } catch (error) {
      console.error('Error loading applications:', error);
    }
  };

  const loadStatistics = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/job-applications/statistics');
      const data = await response.json();
      setStatistics(data);
    } catch (error) {
      console.error('Error loading statistics:', error);
    }
  };

  const checkIfApplied = async (company, jobTitle) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/job-applications/check?company=${encodeURIComponent(company)}&job_title=${encodeURIComponent(jobTitle)}`
      );
      const data = await response.json();
      setAlreadyApplied(data.already_applied);
    } catch (error) {
      console.error('Error checking application:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/job-application', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (data.success) {
        alert(`✅ Job application logged!\n\nCompany: ${data.company}\nPosition: ${data.job_title}\nTotal Applications: ${data.total_applications}`);
        setShowForm(false);
        loadApplications();
        loadStatistics();
        setAlreadyApplied(true);
      } else {
        alert('❌ Error logging application: ' + data.error);
      }
    } catch (error) {
      alert('❌ Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="job-tracking-overlay">
      <div className="job-tracking-modal">
        <div className="job-tracking-header">
          <h2>📊 Job Application Tracker</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="job-tracking-content">
          {/* Statistics Section */}
          {statistics && (
            <div className="statistics-section">
              <h3>Statistics</h3>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-value">{statistics.total}</div>
                  <div className="stat-label">Total Applications</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{statistics.recent_7_days}</div>
                  <div className="stat-label">Last 7 Days</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">
                    {Object.keys(statistics.by_portal).length}
                  </div>
                  <div className="stat-label">Portals Used</div>
                </div>
              </div>

              {Object.keys(statistics.by_portal).length > 0 && (
                <div className="portal-breakdown">
                  <h4>By Portal:</h4>
                  {Object.entries(statistics.by_portal).map(([portal, count]) => (
                    <div key={portal} className="portal-item">
                      <span>{portal}</span>
                      <span className="portal-count">{count}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Quick Add Section */}
          {companyName && roleName && !alreadyApplied && (
            <div className="quick-add-section">
              <div className="quick-add-prompt">
                <p>Did you apply for this job?</p>
                <p className="job-info">
                  <strong>{roleName}</strong> at <strong>{companyName}</strong>
                </p>
                <button 
                  className="btn-primary"
                  onClick={() => setShowForm(true)}
                >
                  Yes, Log Application
                </button>
              </div>
            </div>
          )}

          {alreadyApplied && companyName && roleName && (
            <div className="already-applied-notice">
              ⚠️ You've already logged an application for <strong>{roleName}</strong> at <strong>{companyName}</strong>
            </div>
          )}

          {/* Application Form */}
          {showForm && (
            <div className="application-form">
              <h3>Log Job Application</h3>
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Company Name *</label>
                  <input
                    type="text"
                    name="company"
                    value={formData.company}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Job Title *</label>
                  <input
                    type="text"
                    name="job_title"
                    value={formData.job_title}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Portal</label>
                  <select
                    name="portal"
                    value={formData.portal}
                    onChange={handleInputChange}
                  >
                    <option value="LinkedIn">LinkedIn</option>
                    <option value="Indeed">Indeed</option>
                    <option value="Glassdoor">Glassdoor</option>
                    <option value="Company Website">Company Website</option>
                    <option value="Referral">Referral</option>
                    <option value="Recruiter">Recruiter</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Employment Type</label>
                  <select
                    name="employment_type"
                    value={formData.employment_type}
                    onChange={handleInputChange}
                  >
                    <option value="Full Time">Full Time</option>
                    <option value="Part Time">Part Time</option>
                    <option value="Contract">Contract</option>
                    <option value="Freelance">Freelance</option>
                    <option value="Internship">Internship</option>
                  </select>
                </div>

                <div className="form-actions">
                  <button 
                    type="button" 
                    className="btn-secondary"
                    onClick={() => setShowForm(false)}
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit" 
                    className="btn-primary"
                    disabled={loading}
                  >
                    {loading ? 'Logging...' : 'Log Application'}
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Applications List */}
          <div className="applications-list">
            <div className="list-header">
              <h3>Recent Applications</h3>
              {!showForm && (
                <button 
                  className="btn-secondary btn-small"
                  onClick={() => {
                    setFormData({
                      company: '',
                      job_title: '',
                      portal: 'LinkedIn',
                      employment_type: 'Full Time'
                    });
                    setShowForm(true);
                  }}
                >
                  + Add New
                </button>
              )}
            </div>

            {applications.length === 0 ? (
              <div className="no-applications">
                <p>No applications tracked yet.</p>
                <p>Start logging your job applications to track your progress!</p>
              </div>
            ) : (
              <div className="applications-table">
                <table>
                  <thead>
                    <tr>
                      <th>Company</th>
                      <th>Job Title</th>
                      <th>Portal</th>
                      <th>Type</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {applications.slice(0, 20).map((app, index) => (
                      <tr key={index}>
                        <td><strong>{app.company}</strong></td>
                        <td>{app.job}</td>
                        <td><span className="portal-badge">{app.portal}</span></td>
                        <td>{app.type}</td>
                        <td>{app.date}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          <div className="excel-info">
            <p>💾 All applications are saved to: <code>data/jobs_applied/job_applicaiton.xlsx</code></p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default JobTracking;
