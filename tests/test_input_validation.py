def test_invalid_email_registration(test_client):
    response = test_client.post("/api/v1/users/", json={
        "email": "invalid-email",
        "password": "pass"
    })
    assert response.status_code == 422
