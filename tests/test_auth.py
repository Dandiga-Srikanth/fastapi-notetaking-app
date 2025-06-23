from .config import test_user_account
def test_user_registration(test_client, seed_roles):

    response = test_client.post("/api/v1/users/", 
                                json=test_user_account,
                                headers={"Content-Type": "application/json"}
                            )

    assert response.status_code == 201
    assert response.json()["email"] == test_user_account.get('email','')

def test_user_login(test_client, seed_roles):

    response = test_client.post("/api/v1/users/", 
                                json=test_user_account,
                                headers={"Content-Type": "application/json"}
                            )

    assert response.status_code == 201
    assert response.json()["email"] == test_user_account.get('email','')

    response = test_client.post("/api/v1/auth/login/", data={
        "username": test_user_account.get("email",""),
        "password": test_user_account.get("password","")
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    assert response.status_code == 200
    assert "access_token" in response.json()
