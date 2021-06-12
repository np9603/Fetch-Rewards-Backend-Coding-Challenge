"""
Name - Nihal Surendra Parchand
Email - np9603@rit.edu
Version - Python 3.7

This is a testing file that is used to monitor the proper functioning of the main webservice/FLask application by
covering all possible scenarios and edge cases. I have used the pytest library for creating unit tests.
References:
https://docs.pytest.org/en/6.2.x/index.html
https://medium.com/analytics-vidhya/how-to-test-flask-applications-aef12ae5181c
"""

# Importing libraries
import pytest
from webservice import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_add_transaction(client):
    """
    This function is used to test the add transaction API endpoint
    """

    response = client.post('http://127.0.0.1:5000/add_transaction',
                           json={"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/add_transaction',
                           json={"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/add_transaction',
                           json={"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/add_transaction',
                           json={"payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/add_transaction',
                           json={"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"})
    assert response.status_code == 200


def test_spend_points(client):
    """
    This function is used to test the spend points API endpoint
    """

    # OK response test case
    response = client.delete('http://127.0.0.1:5000/spend_points', json={"points": 5000})
    print(response.data)
    assert response.status_code == 200

    # Error response test case
    response = client.delete('http://127.0.0.1:5000/spend_points', json={"points": 50000})
    print(response.data)
    assert response.status_code == 400


def test_show_balance(client):
    """
    This function is used to test the show balance API endpoint
    """

    response = client.get('http://127.0.0.1:5000/show_balance')
    print(response.data)
    assert response.status_code == 200
