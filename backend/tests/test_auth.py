def test_register_success(client):
    """Test successful user registration"""
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"
    print("✅ Register success test passed")

def test_register_duplicate_email(client, registered_user):
    """Test that duplicate email is rejected"""
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 409
    print("✅ Duplicate email test passed")

def test_register_short_password(client):
    """Test that short password is rejected"""
    response = client.post("/auth/register", json={
        "email": "test2@example.com",
        "password": "123"
    })
    assert response.status_code == 400
    print("✅ Short password test passed")

def test_login_success(client, registered_user):
    """Test successful login"""
    response = client.post("/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    print("✅ Login success test passed")

def test_login_wrong_password(client, registered_user):
    """Test that wrong password is rejected"""
    response = client.post("/auth/login", json={
        "email": registered_user["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    print("✅ Wrong password test passed")

def test_protected_route_without_token(client):
    """Test that protected routes reject unauthenticated requests"""
    response = client.get("/documents/")
    assert response.status_code == 401
    print("✅ Protected route test passed")

def test_protected_route_with_token(client, auth_headers):
    """Test that protected routes work with valid token"""
    response = client.get("/documents/", headers=auth_headers)
    assert response.status_code == 200
    print("✅ Authenticated route test passed")