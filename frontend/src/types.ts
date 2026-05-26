export interface Employee {
  id: number;
  full_name: string;
  job_title: string;
  department: string | null;
  country: string;
  salary: number;
  currency: string;
  email: string | null;
  hire_date: string | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface EmployeeCreate {
  full_name: string;
  job_title: string;
  department?: string;
  country: string;
  salary: number;
  currency?: string;
  email?: string;
  hire_date?: string;
}

export interface EmployeeUpdate {
  full_name?: string;
  job_title?: string;
  department?: string;
  country?: string;
  salary?: number;
  currency?: string;
  email?: string;
  hire_date?: string;
}

export interface PaginatedEmployees {
  total: number;
  page: number;
  page_size: number;
  employees: Employee[];
}

export interface SalaryStats {
  country: string | null;
  job_title: string | null;
  count: number;
  min_salary: number;
  max_salary: number;
  avg_salary: number;
  median_salary: number;
}

export interface DepartmentStats {
  department: string;
  count: number;
  avg_salary: number;
  min_salary: number;
  max_salary: number;
}

export interface CountryHeadcount {
  country: string;
  headcount: number;
  avg_salary: number;
}

export interface TopEarner {
  id: number;
  full_name: string;
  job_title: string;
  department: string | null;
  country: string;
  salary: number;
  currency: string;
}
