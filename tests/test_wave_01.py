from app.models.video import Video
from app.models.customer import Customer


def test_get_tasks_no_saved_videos(client):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []