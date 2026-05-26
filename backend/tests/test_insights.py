"""
TDD — Salary insights tests.
Written BEFORE the implementation (red phase), then made green.
"""
import pytest


class TestSalaryStats:
    def _seed_employees(self, client):
        employees = [
            {"full_name": "Alice A", "job_title": "Engineer", "department": "Engineering",
             "country": "USA", "salary": 80000, "email": "a@ex.com"},
            {"full_name": "Bob B", "job_title": "Engineer", "department": "Engineering",
             "country": "USA", "salary": 100000, "email": "b@ex.com"},
            {"full_name": "Carol C", "job_title": "Manager", "department": "HR",
             "country": "USA", "salary": 120000, "email": "c@ex.com"},
            {"full_name": "Dave D", "job_title": "Engineer", "department": "Engineering",
             "country": "UK", "salary": 70000, "email": "d@ex.com"},
            {"full_name": "Eve E", "job_title": "Analyst", "department": "Finance",
             "country": "UK", "salary": 60000, "email": "e@ex.com"},
        ]
        for emp in employees:
            client.post("/employees/", json=emp)

    def test_salary_stats_for_country(self, client):
        self._seed_employees(client)
        response = client.get("/insights/salary-stats?country=USA")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 3
        assert data["min_salary"] == 80000
        assert data["max_salary"] == 120000
        assert abs(data["avg_salary"] - 100000) < 0.01

    def test_salary_stats_median(self, client):
        self._seed_employees(client)
        response = client.get("/insights/salary-stats?country=USA")
        data = response.json()
        # Sorted USA salaries: [80000, 100000, 120000] → median = 100000
        assert data["median_salary"] == 100000

    def test_salary_stats_for_job_title_in_country(self, client):
        self._seed_employees(client)
        response = client.get("/insights/salary-stats?country=USA&job_title=Engineer")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2
        assert data["min_salary"] == 80000
        assert data["max_salary"] == 100000

    def test_salary_stats_returns_404_for_unknown_country(self, client):
        response = client.get("/insights/salary-stats?country=ATLANTIS")
        assert response.status_code == 404

    def test_salary_stats_no_filter_returns_global(self, client):
        self._seed_employees(client)
        response = client.get("/insights/salary-stats")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 5


class TestDepartmentStats:
    def test_department_stats_returns_list(self, client):
        employees = [
            {"full_name": "A A", "job_title": "Dev", "department": "Engineering",
             "country": "USA", "salary": 90000, "email": "aa@ex.com"},
            {"full_name": "B B", "job_title": "Dev", "department": "Engineering",
             "country": "USA", "salary": 110000, "email": "bb@ex.com"},
            {"full_name": "C C", "job_title": "HR", "department": "People",
             "country": "USA", "salary": 70000, "email": "cc@ex.com"},
        ]
        for emp in employees:
            client.post("/employees/", json=emp)

        response = client.get("/insights/department-stats")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        eng = next(d for d in data if d["department"] == "Engineering")
        assert eng["count"] == 2
        assert abs(eng["avg_salary"] - 100000) < 0.01


class TestHeadcountByCountry:
    def test_headcount_by_country(self, client):
        employees = [
            {"full_name": "X X", "job_title": "Dev", "country": "USA", "salary": 90000, "email": "xx@ex.com"},
            {"full_name": "Y Y", "job_title": "Dev", "country": "USA", "salary": 80000, "email": "yy@ex.com"},
            {"full_name": "Z Z", "job_title": "Dev", "country": "India", "salary": 50000, "email": "zz@ex.com"},
        ]
        for emp in employees:
            client.post("/employees/", json=emp)

        response = client.get("/insights/headcount-by-country")
        assert response.status_code == 200
        data = response.json()
        usa = next(d for d in data if d["country"] == "USA")
        assert usa["headcount"] == 2


class TestTopEarners:
    def test_top_earners_returns_limit(self, client):
        for i in range(15):
            client.post("/employees/", json={
                "full_name": f"Person {i}",
                "job_title": "Dev",
                "country": "USA",
                "salary": i * 10000,
                "email": f"person{i}@ex.com",
            })

        response = client.get("/insights/top-earners?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        # Should be ordered descending by salary
        salaries = [d["salary"] for d in data]
        assert salaries == sorted(salaries, reverse=True)


class TestSalaryPercentile:
    def test_salary_percentile_calculation(self, client):
        # Create 4 employees in USA with salaries [30k, 50k, 70k, 90k]
        ids = []
        for i, salary in enumerate([30000, 50000, 70000, 90000]):
            r = client.post("/employees/", json={
                "full_name": f"Emp {i}",
                "job_title": "Dev",
                "country": "USA",
                "salary": salary,
                "email": f"emp{i}@ex.com",
            })
            ids.append(r.json()["id"])

        # Employee with 70k: 2 out of 4 are below → 50th percentile
        response = client.get(f"/insights/salary-percentile/{ids[2]}")
        assert response.status_code == 200
        data = response.json()
        assert data["percentile"] == 50.0

    def test_salary_percentile_404_for_unknown(self, client):
        response = client.get("/insights/salary-percentile/99999")
        assert response.status_code == 404
