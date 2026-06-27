def test_ask_without_auth(client):
    """Test that chat requires authentication"""
    response = client.post("/chat/ask", json={
        "question": "What is this document about?"
    })
    assert response.status_code == 401
    print("✅ Chat auth test passed")

def test_ask_empty_question(client, auth_headers):
    """Test that empty question is rejected"""
    response = client.post("/chat/ask",
        json={"question": ""},
        headers=auth_headers
    )
    assert response.status_code == 422
    print("✅ Empty question test passed")

def test_ask_question_too_long(client, auth_headers):
    """Test that very long question is rejected"""
    response = client.post("/chat/ask",
        json={"question": "a" * 1001},
        headers=auth_headers
    )
    assert response.status_code == 422
    print("✅ Long question test passed")