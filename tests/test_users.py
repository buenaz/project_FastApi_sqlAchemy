from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_user():
    test_user = {
        "username": "test_user",
        "email": "test@example.com",
        "role": "test_role"
    }

    response = client.post("/users/add", params=test_user)

    assert response.status_code == 200
    assert "test_user" in response.json()


def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    if len(response.json()) > 0:
        user = response.json()[0]
        assert "username" in user
        assert "email" in user


def test_delete_user():
    test_user = {
        "username": "user_to_delete",
        "email": "delete@example.com",
        "role": "test_role"
    }
    add_response = client.post("/users/add", params=test_user)

    user_id = add_response

    delete_params = {"id": user_id}
    response = client.post("/users/delete", params=delete_params)

    assert response.status_code == 200
    assert response.json() == "Пользователь удален"


def test_update_user():
    test_user = {
        "username": "user_to_update",
        "email": "old@example.com",
        "role": "test_role"
    }
    add_response = client.post("/users/add", params=test_user)

    update_params = {
        "id": 1,
        "new_email": "new@example.com"
    }
    response = client.patch("/users/update", params=update_params)

    assert response.status_code == 200
    assert "обновлен" in response.json()


def test_main_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Manager-App"


def test_start_endpoint():
    response = client.get("/start")
    assert response.status_code == 200
    assert response.json() == "Таблицы созданы"


def test_finish_endpoint():
    response = client.get("/finish")
    assert response.status_code == 200
    assert response.json() == "Таблицы очищены"


def setup_test_db():
    client.get("/start")


def teardown_test_db():
    client.get("/finish")