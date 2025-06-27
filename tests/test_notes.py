from .config import test_user_account, test_note_record
from .test_users import register_user

def get_auth_token(test_client, seed_roles_and_permissions):
    response  = register_user(test_client, seed_roles_and_permissions)

    response = test_client.post("/api/v1/auth/login", data={
        "username": test_user_account.get("email", ""),
        "password": test_user_account.get("password","")
    })

    return response.json()["access_token"]

def create_note(test_client, token):
    response = test_client.post("/api/v1/notes/",
                                json=test_note_record,
                                headers={"Authorization": f"Bearer {token}"}
                            )

    return response

def test_create_note(test_client, seed_roles_and_permissions):
    token = get_auth_token(test_client, seed_roles_and_permissions)
    response = create_note(test_client, token)
    
    assert response.status_code == 201
    assert response.json()["title"] == "My Note"

def test_get_all_notes(test_client, seed_roles_and_permissions):
    token = get_auth_token(test_client, seed_roles_and_permissions)
    response = create_note(test_client, token)
    response = test_client.get("/api/v1/notes", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_specific_note(test_client, seed_roles_and_permissions):
    token = get_auth_token(test_client, seed_roles_and_permissions)
    create_response = response = create_note(test_client, token)
    
    note_id = create_response.json()["id"]
    response = test_client.get(f"/api/v1/notes/{note_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == note_id


def test_update_note(test_client, seed_roles_and_permissions):
    token = get_auth_token(test_client, seed_roles_and_permissions)
    create_response = response = create_note(test_client, token)
    
    note_id = create_response.json()["id"]
    response = test_client.put(f"/api/v1/notes/{note_id}", json={
        "title": "Updated Title",
        "content": "After update"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_delete_note(test_client, seed_roles_and_permissions):
    token = get_auth_token(test_client, seed_roles_and_permissions)
    create_response = response = create_note(test_client, token)
    
    note_id = create_response.json()["id"]
    response = test_client.delete(f"/api/v1/notes/{note_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204
