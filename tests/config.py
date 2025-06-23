from app.core.environment_variables import EnvironmentVariables
test_user_account = {
        "email": "john@example.com",
        "password": EnvironmentVariables.TEST_USER_ACCOUNT_PASSWORD,
        "firstName": "John",
        "lastName": "Doe",
        "roleName": "Viewer"
    }

test_user_account_update_details = {
        "firstName": "John Updated",
        "lastName": "Doe Updated"
    }

test_note_record = {
        "title": "My Note",
        "content": "This is a note."
    }