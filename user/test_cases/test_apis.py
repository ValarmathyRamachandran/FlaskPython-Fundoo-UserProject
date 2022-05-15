import json

import pytest
from app import app

reg_data = {
    "first_name": "Bala",
    "last_name": "Venkat",
    "user_name": "bala1",
    "email": "balaji271192@gmail.com",
    "password": "bala@123",
    "confirm_password": "bala@123"
}

data = json.dumps(reg_data)

            
def test_registration():
    """
       testing login register api is posted and check which status code is returned
    """
    # response = app.test_client().post('/registration', data=reg_data)
    response = app.test_client().post('/registration', data=reg_data)

    assert response.status_code == 201
 
