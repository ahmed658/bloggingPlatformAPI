from app import schemas
import jwt
from app.config import settings
import pytest

def test_register_user(client):
    res = client.post("/users/",
                      json = {
    "username": "gammaassets-user",
    "password": "password-for-gammaassets-user",
    "first_name": "ahmed",
    "last_name": "maher",
    "email": "ahmedmaherbf@gmail.com"})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "ahmedmaherbf@gmail.com"
    assert res.status_code == 201
    
def test_login_user(client, test_user):
    res = client.post("/login", data = {
                          "username": test_user['username'],
                          "password": test_user['password']
                      })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['user_id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    
@pytest.mark.parametrize("username, password, status_code", [("gammaassets-user", "wrong-password", 403),
                                                             ("wrong-user", "password-for-gammaassets-user", 403),
                                                             ("random-user", "random-password", 403),
                                                             (None, "password-for-gammaassets-user", 403),
                                                             ("gammaassets-user", None, 403)])
def test_incorrect_login_user(client, test_user, username, password, status_code):
    res = client.post("/login", data = {
                          "username": username,
                          "password": password
                      })
    assert res.status_code == status_code
#    assert res.json().get('detail') == "Invalid credentials"

def test_non_admin_user_list_all_users(authorized_client):
    res = authorized_client.get("/users")
    assert res.status_code == 403
    
def test_update_current_user(authorized_client, test_user):
    update_data = {
        "first_name": "UpdatedName",
        "phone": "+201001776665"
    }
    res = authorized_client.put("/users", json=update_data)
    
    print(res.json())
    
    updated_user = schemas.UserOut(**res.json())
    assert res.status_code == 200
    assert updated_user.first_name == "UpdatedName"
    assert updated_user.phone == "tel:+20-10-01776665"

def test_non_user_update_other_user(client, test_user):
    update_data = {
        "first_name": "NewName",
        "email": "newemail@example.com"
    }
    res = client.put(f"/users/{test_user['username']}", json=update_data)
    
    assert res.status_code == 401

def test_update_user(authorized_client, test_user):
    user_update_data = {
        "email": "updated@example.com"
    }
    res = authorized_client.put(f"/users/{test_user['username']}", json=user_update_data)
    
    assert res.status_code == 403

def test_admin_delete_user(authorized_client, test_user):
    res = authorized_client.delete(f"/users/{test_user['username']}")
    
    assert res.status_code == 403  # Ensure this user isn't admin by default.

# Test editing the current user
def test_update_current_user(authorized_client, session, test_user):
    updated_data = {
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
        "email": "updatedemail@example.com"
    }
    res = authorized_client.put("/users/", json=updated_data)
    assert res.status_code == 200
    updated_user = res.json()
    assert updated_user['first_name'] == updated_data['first_name']
    assert updated_user['last_name'] == updated_data['last_name']
    assert updated_user['email'] == updated_data['email']

# Test editing another user as admin
def test_update_other_user_as_admin(admin_client, session, test_user):
    updated_data = {
        "first_name": "AdminUpdatedFirstName",
        "last_name": "AdminUpdatedLastName",
        "email": "adminupdatedemail@example.com"
    }
    res = admin_client.put(f"/users/{test_user['username']}", json=updated_data)
    assert res.status_code == 200
    updated_user = res.json()
    assert updated_user['first_name'] == updated_data['first_name']
    assert updated_user['last_name'] == updated_data['last_name']
    assert updated_user['email'] == updated_data['email']

# Test non-admin user editing another user
def test_non_admin_update_other_user(authorized_client, session, test_user):
    updated_data = {
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
        "email": "updatedemail@example.com"
    }
    res = authorized_client.put(f"/users/{test_user['username']}", json=updated_data)
    assert res.status_code == 403

# Test listing all users as admin
def test_admin_list_users(admin_client, session, test_user):
    res = admin_client.get("/users")
    assert res.status_code == 200
    users = res.json()
    assert isinstance(users, list)
    assert len(users) >= 1

# Test non-admin user listing all users
def test_non_admin_list_users(authorized_client, session):
    res = authorized_client.get("/users")
    assert res.status_code == 403

# Test deleting the current user
# To be implemented

# Test deleting another user as admin
def test_admin_delete_user(admin_client, session, test_user):
    res = admin_client.delete(f"/users/{test_user['username']}")
    assert res.status_code == 204

# Test deleting a non-existent user as admin
def test_admin_delete_non_existent_user(admin_client, session):
    res = admin_client.delete("/users/nonexistentuser")
    assert res.status_code == 404