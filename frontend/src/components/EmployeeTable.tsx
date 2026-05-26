import React, { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from 'react-query';
import { getEmployees, createEmployee, updateEmployee, deleteEmployee } from '../api';
import { Employee, EmployeeCreate } from '../types';
import EmployeeForm from './EmployeeForm';
import DeleteDialog from './DeleteDialog';

const fmt = (n: number) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);

const EmployeeTable: React.FC = () => {
  const queryClient = useQueryClient();

  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [countryFilter, setCountryFilter] = useState('');
  const [deptFilter, setDeptFilter] = useState('');

  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Employee | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Employee | null>(null);

  const PAGE_SIZE = 50;

  const { data, isLoading, isError } = useQuery(
    ['employees', page, search, countryFilter, deptFilter],
    () => getEmployees({ page, page_size: PAGE_SIZE, search: search || undefined, country: countryFilter || undefined, department: deptFilter || undefined }),
    { keepPreviousData: true }
  );

  const createMut = useMutation(createEmployee, {
    onSuccess: () => { queryClient.invalidateQueries('employees'); setFormOpen(false); },
  });

  const updateMut = useMutation(
    (payload: { id: number; data: EmployeeCreate }) => updateEmployee(payload.id, payload.data),
    { onSuccess: () => { queryClient.invalidateQueries('employees'); setFormOpen(false); setEditing(null); } }
  );

  const deleteMut = useMutation(deleteEmployee, {
    onSuccess: () => { queryClient.invalidateQueries('employees'); setDeleteTarget(null); },
  });

  const handleSave = (formData: EmployeeCreate) => {
    if (editing) {
      updateMut.mutate({ id: editing.id, data: formData });
    } else {
      createMut.mutate(formData);
    }
  };

  const totalPages = data ? Math.ceil(data.total / PAGE_SIZE) : 1;

  return (
    <div className="page">
      <div className="page-header">
        <h1>Employees</h1>
        <button className="btn btn-primary" onClick={() => { setEditing(null); setFormOpen(true); }}>
          + Add Employee
        </button>
      </div>

      {/* Filters */}
      <div className="filters">
        <input
          placeholder="Search name, title, email..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1); }}
          className="filter-input"
        />
        <input
          placeholder="Filter by country"
          value={countryFilter}
          onChange={(e) => { setCountryFilter(e.target.value); setPage(1); }}
          className="filter-input"
        />
        <input
          placeholder="Filter by department"
          value={deptFilter}
          onChange={(e) => { setDeptFilter(e.target.value); setPage(1); }}
          className="filter-input"
        />
      </div>

      {/* Stats bar */}
      {data && (
        <p className="results-info">
          Showing {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, data.total)} of {data.total.toLocaleString()} employees
        </p>
      )}

      {isLoading && <div className="loading">Loading...</div>}
      {isError && <div className="error-msg">Failed to load employees. Is the backend running?</div>}

      {data && (
        <>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Job Title</th>
                  <th>Department</th>
                  <th>Country</th>
                  <th>Salary</th>
                  <th>Email</th>
                  <th>Hire Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {data.employees.map((emp) => (
                  <tr key={emp.id}>
                    <td><strong>{emp.full_name}</strong></td>
                    <td>{emp.job_title}</td>
                    <td>{emp.department ?? '—'}</td>
                    <td>{emp.country}</td>
                    <td>{fmt(emp.salary)}</td>
                    <td>{emp.email ?? '—'}</td>
                    <td>{emp.hire_date ?? '—'}</td>
                    <td>
                      <button className="btn-icon" onClick={() => { setEditing(emp); setFormOpen(true); }}>✏️</button>
                      <button className="btn-icon btn-icon-danger" onClick={() => setDeleteTarget(emp)}>🗑️</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="pagination">
            <button className="btn btn-secondary" onClick={() => setPage(1)} disabled={page === 1}>«</button>
            <button className="btn btn-secondary" onClick={() => setPage((p) => p - 1)} disabled={page === 1}>‹ Prev</button>
            <span className="page-info">Page {page} of {totalPages}</span>
            <button className="btn btn-secondary" onClick={() => setPage((p) => p + 1)} disabled={page === totalPages}>Next ›</button>
            <button className="btn btn-secondary" onClick={() => setPage(totalPages)} disabled={page === totalPages}>»</button>
          </div>
        </>
      )}

      <EmployeeForm
        isOpen={formOpen}
        employee={editing}
        onSave={handleSave}
        onCancel={() => { setFormOpen(false); setEditing(null); }}
        loading={createMut.isLoading || updateMut.isLoading}
      />

      <DeleteDialog
        isOpen={!!deleteTarget}
        title={deleteTarget?.full_name ?? ''}
        onConfirm={() => deleteTarget && deleteMut.mutate(deleteTarget.id)}
        onCancel={() => setDeleteTarget(null)}
        loading={deleteMut.isLoading}
      />
    </div>
  );
};

export default EmployeeTable;
