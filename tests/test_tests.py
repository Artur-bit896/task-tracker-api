def test_create_task(client):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Тестовая задача",
            "description": "Проверка создания задачи",
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Тестовая задача"
    assert response.json()["status"] == "todo"

    data = response.json()
    assert data["title"] == "Тестовая задача"
    assert data["description"] == "Проверка создания задачи"
    assert data["status"] == "todo"
    assert "id" in data


def test_get_task_by_id(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Задача для поиска"},
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Задача для поиска"


def test_get_task_not_found(client):
    response = client.get("/api/v1/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Старое название"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Новое название"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Новое название"


def test_delete_task(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Задача для удаления"},
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 204

    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_filter_tasks_by_status(client):
    client.post(
        "/api/v1/tasks",
        json={"title": "Задача 1", "status": "todo"},
    )
    client.post(
        "/api/v1/tasks",
        json={"title": "Задача 2", "status": "done"},
    )

    response = client.get("/api/v1/tasks?status=todo")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Задача 1"
    assert tasks[0]["status"] == "todo"


def test_create_task_empty_title(client):
    response = client.post(
        "/api/v1/tasks",
        json={"title": ""},
    )

    assert response.status_code == 422
