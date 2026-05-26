import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  getSalaryStats,
  getDepartmentStats,
  getHeadcountByCountry,
  getTopEarners,
} from '../api';

const fmt = (n: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);

const InsightsPage: React.FC = () => {
  const [country, setCountry] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [topLimit, setTopLimit] = useState(10);

  const statsQuery = useQuery(
    ['salary-stats', country, jobTitle],
    () => getSalaryStats(country || undefined, jobTitle || undefined),
    { retry: false }
  );

  const deptQuery = useQuery('dept-stats', getDepartmentStats);
  const countryQuery = useQuery('headcount', getHeadcountByCountry);
  const topQuery = useQuery(['top-earners', topLimit], () => getTopEarners(topLimit));

  return (
    <div className="page">
      <div className="page-header">
        <h1>Salary Insights</h1>
      </div>

      {/* ── Salary Stats ────────────────────────────────────────── */}
      <section className="card">
        <h2>Salary Statistics</h2>
        <div className="filters">
          <input
            placeholder="Country (optional)"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            className="filter-input"
          />
          <input
            placeholder="Job Title (optional)"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            className="filter-input"
          />
        </div>

        {statsQuery.isLoading && <p className="loading">Loading...</p>}
        {statsQuery.isError && (
          <p className="error-msg">No data found for those filters.</p>
        )}
        {statsQuery.data && (
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Employees</span>
              <span className="stat-value">{statsQuery.data.count.toLocaleString()}</span>
            </div>
            <div className="stat-card stat-card--min">
              <span className="stat-label">Min Salary</span>
              <span className="stat-value">{fmt(statsQuery.data.min_salary)}</span>
            </div>
            <div className="stat-card stat-card--avg">
              <span className="stat-label">Avg Salary</span>
              <span className="stat-value">{fmt(statsQuery.data.avg_salary)}</span>
            </div>
            <div className="stat-card stat-card--median">
              <span className="stat-label">Median Salary</span>
              <span className="stat-value">{fmt(statsQuery.data.median_salary)}</span>
            </div>
            <div className="stat-card stat-card--max">
              <span className="stat-label">Max Salary</span>
              <span className="stat-value">{fmt(statsQuery.data.max_salary)}</span>
            </div>
          </div>
        )}
      </section>

      {/* ── Top Earners ─────────────────────────────────────────── */}
      <section className="card">
        <div className="section-header">
          <h2>Top Earners</h2>
          <select
            value={topLimit}
            onChange={(e) => setTopLimit(Number(e.target.value))}
            className="filter-select"
          >
            {[5, 10, 20, 50].map((n) => (
              <option key={n} value={n}>Top {n}</option>
            ))}
          </select>
        </div>
        {topQuery.isLoading && <p className="loading">Loading...</p>}
        {topQuery.data && (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Job Title</th>
                  <th>Department</th>
                  <th>Country</th>
                  <th>Salary</th>
                </tr>
              </thead>
              <tbody>
                {topQuery.data.map((emp, i) => (
                  <tr key={emp.id}>
                    <td><strong>{i + 1}</strong></td>
                    <td>{emp.full_name}</td>
                    <td>{emp.job_title}</td>
                    <td>{emp.department ?? '—'}</td>
                    <td>{emp.country}</td>
                    <td><strong>{fmt(emp.salary)}</strong></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* ── Headcount by Country ─────────────────────────────────── */}
      <section className="card">
        <h2>Headcount by Country</h2>
        {countryQuery.isLoading && <p className="loading">Loading...</p>}
        {countryQuery.data && (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Country</th>
                  <th>Headcount</th>
                  <th>Avg Salary</th>
                </tr>
              </thead>
              <tbody>
                {countryQuery.data.map((row) => (
                  <tr key={row.country}>
                    <td>{row.country}</td>
                    <td>{row.headcount.toLocaleString()}</td>
                    <td>{fmt(row.avg_salary)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* ── Department Stats ─────────────────────────────────────── */}
      <section className="card">
        <h2>Salary by Department</h2>
        {deptQuery.isLoading && <p className="loading">Loading...</p>}
        {deptQuery.data && (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Department</th>
                  <th>Headcount</th>
                  <th>Min</th>
                  <th>Avg</th>
                  <th>Max</th>
                </tr>
              </thead>
              <tbody>
                {deptQuery.data.map((row) => (
                  <tr key={row.department}>
                    <td>{row.department}</td>
                    <td>{row.count.toLocaleString()}</td>
                    <td>{fmt(row.min_salary)}</td>
                    <td>{fmt(row.avg_salary)}</td>
                    <td>{fmt(row.max_salary)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
};

export default InsightsPage;
