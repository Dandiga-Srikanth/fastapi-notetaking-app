from .config import test_user_account, test_user_account_update_details

def register_user(test_client, seed_roles_and_permissions):

    response = test_client.post("/api/v1/users/",
                                json=test_user_account,
                                headers={"Content-Type": "application/json"}
                            )
    return response

def test_register_user(test_client, seed_roles_and_permissions):

    response = register_user(test_client, seed_roles_and_permissions)

    assert response.status_code == 201
    assert response.json()["email"] == test_user_account.get("email","")

def test_register_duplicate_user(test_client, seed_roles_and_permissions):

    response = register_user(test_client, seed_roles_and_permissions)
    assert response.status_code == 201
    assert response.json()["email"] == test_user_account.get("email","")

    response = register_user(test_client, seed_roles_and_permissions)
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists."

def test_get_all_users(test_client, seed_roles_and_permissions):
    response = test_client.get("/api/v1/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id(test_client, seed_roles_and_permissions):

    create_response = register_user(test_client, seed_roles_and_permissions)
    
    assert create_response.status_code == 201
    assert create_response.json()["email"] == test_user_account.get("email","")

    user_id = create_response.json()["id"]
    response = test_client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_update_user(test_client, seed_roles_and_permissions):
    
    create_response = register_user(test_client, seed_roles_and_permissions)
    
    assert create_response.status_code == 201
    assert create_response.json()["email"] == test_user_account.get("email","")

    user_id = create_response.json()["id"]
    response = test_client.put(f"/api/v1/users/{user_id}", json=test_user_account_update_details, headers={"Content-Type": "application/json"})

    assert response.status_code == 200
    assert response.json()["firstName"] == test_user_account_update_details.get("firstName")


def test_delete_user(test_client, seed_roles_and_permissions):

    create_response = register_user(test_client, seed_roles_and_permissions)
    
    assert create_response.status_code == 201
    assert create_response.json()["email"] == test_user_account.get("email","")

    user_id = create_response.json()["id"]
    response = test_client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204
