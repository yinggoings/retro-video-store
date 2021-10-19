from app.models.video import Video
from app.models.customer import Customer

VIDEO_TITLE = "A Brand New Video"
VIDEO_ID = 1
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_ID = 1
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

def test_checkout_video(client, one_video, one_customer):

    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()


    assert response.status_code == 200
    assert response_body["video_id"] == 1
    assert response_body["customer_id"] == 1
    assert response_body["videos_checked_out_count"] == 1
    assert response_body["available_inventory"] == 0

def test_checkout_video_no_inventory(client, one_checked_out_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == "Could not perform checkout"

def test_checkin_video(client, one_checked_out_video):
    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["video_id"] == 1
    assert response_body["customer_id"] == 1
    assert response_body["videos_checked_out_count"] == 0
    assert response_body["available_inventory"] == 1

def test_checkin_video_not_checked_out(client, one_video, one_customer):

    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "No outstanding rentals for customer # 1 and video 1"}
    

def test_rentals_by_video(client, one_checked_out_video):
    response = client.get("/videos/1/rentals")

    response_body = response.get_json()

    response.status_code == 200
    len(response_body) == 1
    response_body[0]["name"] == CUSTOMER_NAME

def test_rentals_by_video_video_not_found(client):
    response = client.get("/videos/1/rentals")

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["message"] == "Video 1 was not found"

def test_rentals_by_video_video_no_rental(client, one_video):
    response = client.get("/videos/1/rentals")

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

#def test_rentals_by_customer(client, one_checked_out_video):
