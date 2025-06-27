from .config import test_user_account, test_note_record

def test_user_can_create_and_fetch_notes(test_client, seed_roles_and_permissions):
    
    # --------  Create User --------

    response = test_client.post("/api/v1/users/", json=test_user_account)
    assert response.status_code == 201
    assert response.json()["email"] == test_user_account.get("email","")

    # -------- Login User --------

    login_data = {
        "username": test_user_account.get("email",""),
        "password":test_user_account.get("password","")
    }
    res = test_client.post("/api/v1/auth/login/", data=login_data)
    assert res.status_code == 200
    token = res.json()["access_token"]
    assert token is not None

    headers = {"Authorization": f"Bearer {token}"}

    # -------- Create Note --------

    res = test_client.post("/api/v1/notes/", json=test_note_record, headers=headers)
    assert res.status_code == 201
    created_note = res.json()
    assert created_note["title"] == test_note_record["title"]
    note_id = created_note["id"]

    # -------- Get Note by ID --------

    res = test_client.get(f"/api/v1/notes/{note_id}", headers=headers)
    assert res.status_code == 200
    retrieved_note = res.json()
    assert retrieved_note["id"] == note_id
    assert retrieved_note["title"] == test_note_record["title"]
