import json
from app import app


def test_registration():
    """
       testing login register api is posted and check which status code is returned
    """
    client = app.test_client()

    reg_data = {
        "first_name": "Bala",
        "last_name": "Venkat",
        "user_name": "bala1",
        "email": "balaji271192@gmail.com",
        "password": "bala@123",
        "confirm_password": "bala@123"
    }

    response = client.post('/registration', data=json.dumps(reg_data))
    assert response.status_code == 200


def test_get_user():
    client = app.test_client()
    url = '/getallusers'

    response = client.get(url)
    result = json.loads(response.data).get('msg')
    assert response.status_code == 200
    assert type(result) is list



test_registration()
test_get_user()
