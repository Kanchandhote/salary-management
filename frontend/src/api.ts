import axios from 'axios';
import {
  Employee,
  EmployeeCreate,
  EmployeeUpdate,
  PaginatedEmployees,
  SalaryStats,
  DepartmentStats,
  CountryHeadcount,
  TopEarner,
} from './types';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// ── Employees ──────────────────────────────────────────────────────────────

export interface GetEmployeesParams {
  page?: number;
  page_size?: number;
  search?: string;
  country?: string;
  job_title?: string;
  department?: string;
}

export const getEmployees = async (params: GetEmployeesParams): Promise<PaginatedEmployees> => {
  const { data } = await api.get('/employees/', { params });
  return data;
};

export const getEmployee = async (id: number): Promise<Employee> => {
  const { data } = await api.get(`/employees/${id}`);
  return data;
};

export const createEmployee = async (payload: EmployeeCreate): Promise<Employee> => {
  const { data } = await api.post('/employees/', payload);
  return data;
};

export const updateEmployee = async (id: number, payload: EmployeeUpdate): Promise<Employee> => {
  const { data } = await api.put(`/employees/${id}`, payload);
  return data;
};

export const deleteEmployee = async (id: number): Promise<void> => {
  await api.delete(`/employees/${id}`);
};

// ── Insights ───────────────────────────────────────────────────────────────

export const getSalaryStats = async (country?: string, job_title?: string): Promise<SalaryStats> => {
  const { data } = await api.get('/insights/salary-stats', { params: { country, job_title } });
  return data;
};

export const getDepartmentStats = async (): Promise<DepartmentStats[]> => {
  const { data } = await api.get('/insights/department-stats');
  return data;
};

export const getHeadcountByCountry = async (): Promise<CountryHeadcount[]> => {
  const { data } = await api.get('/insights/headcount-by-country');
  return data;
};

export const getTopEarners = async (limit = 10): Promise<TopEarner[]> => {
  const { data } = await api.get('/insights/top-earners', { params: { limit } });
  return data;
};
