from app.models.video import Video
from app.models.customer import Customer

def test_checkout_video(client, one_video, one_customer):

    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()


    response.status == 200
    response_body["video_id"] == 1
    response_body["customer_id"] == 1
    response_body["videos_checked_out_count"] == 1
    response_body["available_inventory"] == 0
    #"due_date": new_rental.due_date

def test_checkout_video_no_inventory(client, one_checked_out_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    response.status == 400
    response_body == {"message": "Could not perform checkout"}

def test_checkin_video(client, one_checked_out_video):
    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    response.status == 200
    response_body["video_id"] == 1
    response_body["customer_id"] == 1
    response_body["videos_checked_out_count"] == 0
    response_body["available_inventory"] == 1

def test_checkin_video_not_checked_out(client, one_video, one_customer):

    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    response.status == 400
    response_body == {"message": "No outstanding rentals for customer # 1 and video 1"}
    

