"""
TDD — Employee CRUD tests.
Written BEFORE the implementation (red phase), then made green.
"""
import pytest


class TestCreateEmployee:
    def test_create_employee_returns_201(self, client, sample_employee_payload):
        response = client.post("/employees/", json=sample_employee_payload)
        assert response.status_code == 201

    def test_create_employee_returns_correct_data(self, client, sample_employee_payload):
        response = client.post("/employees/", json=sample_employee_payload)
        data = response.json()
        assert data["full_name"] == "Alice Smith"
        assert data["job_title"] == "Software Engineer"
        assert data["country"] == "USA"
        assert data["salary"] == 95000.0
        assert "id" in data

    def test_create_employee_with_minimum_fields(self, client):
        payload = {
            "full_name": "Bob Jones",
            "job_title": "Analyst",
            "country": "UK",
            "salary": 50000.0,
        }
        response = client.post("/employees/", json=payload)
        assert response.status_code == 201
        assert response.json()["currency"] == "USD"  # default

    def test_create_employee_rejects_negative_salary(self, client, sample_employee_payload):
        sample_employee_payload["salary"] = -1000
        response = client.post("/employees/", json=sample_employee_payload)
        assert response.status_code == 422

    def test_create_employee_rejects_empty_full_name(self, client, sample_employee_payload):
        sample_employee_payload["full_name"] = "   "
        response = client.post("/employees/", json=sample_employee_payload)
        assert response.status_code == 422

    def test_create_employee_rejects_empty_country(self, client, sample_employee_payload):
        sample_employee_payload["country"] = ""
        response = client.post("/employees/", json=sample_employee_payload)
        assert response.status_code == 422

    def test_create_employee_salary_zero_is_valid(self, client, sample_employee_payload):
        sample_employee_payload["salary"] = 0
        response = client.post("/employees/", json=sample_employee_payload)
        assert response.status_code == 201


class TestGetEmployee:
    def test_get_existing_employee(self, client, sample_employee_payload):
        created = client.post("/employees/", json=sample_employee_payload).json()
        response = client.get(f"/employees/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]

    def test_get_nonexistent_employee_returns_404(self, client):
        response = client.get("/employees/99999")
        assert response.status_code == 404

    def test_get_employees_returns_paginated_list(self, client, sample_employee_payload):
        # Create 3 employees
        for i in range(3):
            payload = sample_employee_payload.copy()
            payload["email"] = f"user{i}@example.com"
            client.post("/employees/", json=payload)

        response = client.get("/employees/?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["employees"]) == 2
        assert data["page"] == 1

    def test_get_employees_search_by_name(self, client, sample_employee_payload):
        client.post("/employees/", json=sample_employee_payload)
        payload2 = sample_employee_payload.copy()
        payload2["full_name"] = "Charlie Brown"
        payload2["email"] = "charlie@example.com"
        client.post("/employees/", json=payload2)

        response = client.get("/employees/?search=charlie")
        data = response.json()
        assert data["total"] == 1
        assert data["employees"][0]["full_name"] == "Charlie Brown"

    def test_get_employees_filter_by_country(self, client, sample_employee_payload):
        client.post("/employees/", json=sample_employee_payload)  # USA
        payload2 = sample_employee_payload.copy()
        payload2["country"] = "Germany"
        payload2["email"] = "german@example.com"
        client.post("/employees/", json=payload2)

        response = client.get("/employees/?country=Germany")
        data = response.json()
        assert data["total"] == 1
        assert data["employees"][0]["country"] == "Germany"


class TestUpdateEmployee:
    def test_update_employee_salary(self, client, sample_employee_payload):
        created = client.post("/employees/", json=sample_employee_payload).json()
        response = client.put(
            f"/employees/{created['id']}", json={"salary": 110000.0}
        )
        assert response.status_code == 200
        assert response.json()["salary"] == 110000.0

    def test_update_employee_partial_fields(self, client, sample_employee_payload):
        created = client.post("/employees/", json=sample_employee_payload).json()
        response = client.put(
            f"/employees/{created['id']}", json={"job_title": "Senior Engineer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["job_title"] == "Senior Engineer"
        assert data["full_name"] == "Alice Smith"  # unchanged

    def test_update_nonexistent_employee_returns_404(self, client):
        response = client.put("/employees/99999", json={"salary": 50000})
        assert response.status_code == 404

    def test_update_rejects_negative_salary(self, client, sample_employee_payload):
        created = client.post("/employees/", json=sample_employee_payload).json()
        response = client.put(
            f"/employees/{created['id']}", json={"salary": -500}
        )
        assert response.status_code == 422


class TestDeleteEmployee:
    def test_delete_employee_returns_204(self, client, sample_employee_payload):
        created = client.post("/employees/", json=sample_employee_payload).json()
        response = client.delete(f"/employees/{created['id']}")
        assert response.status_code == 204

    def test_delete_removes_employee_from_db(self, client, sample_employee_payload):
        created = client.post("/employees/", json=sample_employee_payload).json()
        client.delete(f"/employees/{created['id']}")
        response = client.get(f"/employees/{created['id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_employee_returns_404(self, client):
        response = client.delete("/employees/99999")
        assert response.status_code == 404
