def test_dashboard_requires_login(client):
    res = client.get("/admin", follow_redirects=True)
    assert "Админ хуудсанд нэвтрэх шаардлагатай." in res.data.decode()


def test_dashboard_accessible_when_logged_in(client):
    client.post("/admin/login", data={"username": "admin", "password": "admin123"})
    res = client.get("/admin")
    assert res.status_code == 200


def test_dashboard_shows_registration(client):
    client.post("/", data={
        "last_name": "Бат",
        "first_name": "Болд",
        "phone": "99112233",
        "email": "show@example.com",
    })
    client.post("/admin/login", data={"username": "admin", "password": "admin123"})
    res = client.get("/admin")
    assert b"show@example.com" in res.data
