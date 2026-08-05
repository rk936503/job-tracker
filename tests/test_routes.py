def test_home_redirects_when_logged_out(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_register_and_login_flow(client):
    # Register the first (and only) user
    response = client.post("/register", data={
        "username": "testuser",
        "password": "testpass123"
    }, follow_redirects=True)
    assert response.status_code == 200

    # Log in with that user
    response = client.post("/login", data={
        "username": "testuser",
        "password": "testpass123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data


def test_register_closes_after_first_user(client):
    client.post("/register", data={"username": "user1", "password": "pass123"})
    response = client.post("/register", data={
        "username": "user2",
        "password": "pass456"
    }, follow_redirects=True)
    assert b"Registration is closed" in response.data


def test_add_application_requires_login(client):
    response = client.get("/add", follow_redirects=False)
    assert response.status_code == 302


def test_add_and_view_application(client):
    client.post("/register", data={"username": "testuser", "password": "testpass123"})
    client.post("/login", data={"username": "testuser", "password": "testpass123"})

    response = client.post("/add", data={
        "company": "Acme Corp",
        "role": "Backend Developer",
        "status": "Applied",
        "date_applied": "2026-08-05",
        "notes": "Referred by a friend",
        "job_url": "https://example.com/job/123"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Acme Corp" in response.data