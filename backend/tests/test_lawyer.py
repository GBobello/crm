import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_token():
    login_data = {"username": "admin", "password": "admin"}  # altere se necessário
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_lawyer_success(auth_token):
    lawyer_data = {
        "username": "newlawyer",
        "password": "123456",
        "name": "João Silva",
        "email": "joao@example.com",
        "document": "07168369989",
        "phone": "47999950797",
        "oab": "123456",
        "oab_state": "SC",
        "position_id": 1
    }

    response = client.post("/lawyers/", json=lawyer_data, headers=auth_token)
    assert response.status_code in [200, 201]


def test_get_lawyers_success(auth_token):
    response = client.get("/lawyers/", headers=auth_token)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_lawyer_not_found(auth_token):
    update_data = {"name": "Novo Nome"}
    response = client.put("/lawyers/999", json=update_data, headers=auth_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Advogado não encontrado"


def test_delete_lawyer_not_found(auth_token):
    response = client.delete("/lawyers/999", headers=auth_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Advogado não encontrado"
