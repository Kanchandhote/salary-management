import React, { useState, useEffect } from 'react';
import { Employee, EmployeeCreate } from '../types';

interface Props {
  isOpen: boolean;
  employee?: Employee | null;
  onSave: (data: EmployeeCreate) => void;
  onCancel: () => void;
  loading?: boolean;
}

const EMPTY: EmployeeCreate = {
  full_name: '',
  job_title: '',
  department: '',
  country: '',
  salary: 0,
  currency: 'USD',
  email: '',
  hire_date: '',
};

const EmployeeForm: React.FC<Props> = ({ isOpen, employee, onSave, onCancel, loading }) => {
  const [form, setForm] = useState<EmployeeCreate>(EMPTY);
  const [errors, setErrors] = useState<Partial<Record<keyof EmployeeCreate, string>>>({});

  useEffect(() => {
    if (employee) {
      setForm({
        full_name: employee.full_name,
        job_title: employee.job_title,
        department: employee.department ?? '',
        country: employee.country,
        salary: employee.salary,
        currency: employee.currency,
        email: employee.email ?? '',
        hire_date: employee.hire_date ?? '',
      });
    } else {
      setForm(EMPTY);
    }
    setErrors({});
  }, [employee, isOpen]);

  const validate = (): boolean => {
    const errs: Partial<Record<keyof EmployeeCreate, string>> = {};
    if (!form.full_name.trim()) errs.full_name = 'Full name is required';
    if (!form.job_title.trim()) errs.job_title = 'Job title is required';
    if (!form.country.trim()) errs.country = 'Country is required';
    if (form.salary < 0) errs.salary = 'Salary must be non-negative';
    if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email))
      errs.email = 'Invalid email address';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: name === 'salary' ? parseFloat(value) || 0 : value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) onSave(form);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>{employee ? 'Edit Employee' : 'Add Employee'}</h2>
        <form onSubmit={handleSubmit} noValidate>
          <div className="form-grid">
            <div className="form-group">
              <label>Full Name *</label>
              <input name="full_name" value={form.full_name} onChange={handleChange} />
              {errors.full_name && <span className="error">{errors.full_name}</span>}
            </div>
            <div className="form-group">
              <label>Job Title *</label>
              <input name="job_title" value={form.job_title} onChange={handleChange} />
              {errors.job_title && <span className="error">{errors.job_title}</span>}
            </div>
            <div className="form-group">
              <label>Department</label>
              <input name="department" value={form.department} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>Country *</label>
              <input name="country" value={form.country} onChange={handleChange} />
              {errors.country && <span className="error">{errors.country}</span>}
            </div>
            <div className="form-group">
              <label>Salary *</label>
              <input name="salary" type="number" min="0" step="0.01" value={form.salary} onChange={handleChange} />
              {errors.salary && <span className="error">{errors.salary}</span>}
            </div>
            <div className="form-group">
              <label>Currency</label>
              <select name="currency" value={form.currency} onChange={handleChange}>
                <option>USD</option>
                <option>EUR</option>
                <option>GBP</option>
                <option>INR</option>
                <option>CAD</option>
                <option>AUD</option>
              </select>
            </div>
            <div className="form-group">
              <label>Email</label>
              <input name="email" type="email" value={form.email} onChange={handleChange} />
              {errors.email && <span className="error">{errors.email}</span>}
            </div>
            <div className="form-group">
              <label>Hire Date</label>
              <input name="hire_date" type="date" value={form.hire_date} onChange={handleChange} />
            </div>
          </div>
          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onCancel} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Saving...' : employee ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EmployeeForm;
