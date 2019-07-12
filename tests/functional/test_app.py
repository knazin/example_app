import pytest

def test_home_page(test_client):
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200   