import React from 'react';
import { BrowserRouter, Routes, Route, NavLink, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import EmployeeTable from './components/EmployeeTable';
import InsightsPage from './components/InsightsPage';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: { queries: { refetchOnWindowFocus: false, staleTime: 30_000 } },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <nav className="navbar">
          <div className="navbar-brand">💼 SalaryManager</div>
          <div className="navbar-links">
            <NavLink to="/employees" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
              Employees
            </NavLink>
            <NavLink to="/insights" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
              Insights
            </NavLink>
          </div>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/employees" replace />} />
            <Route path="/employees" element={<EmployeeTable />} />
            <Route path="/insights" element={<InsightsPage />} />
          </Routes>
        </main>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
