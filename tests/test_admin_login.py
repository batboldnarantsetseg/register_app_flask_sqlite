def test_admin_login_get(client):
    res = client.get("/admin/login")
    assert res.status_code == 200


def test_admin_login_success(client):
    res = client.post("/admin/login", data={
        "username": "admin",
        "password": "admin123",
    }, follow_redirects=True)
    assert "амжилттай нэвтэрлээ." in res.data.decode()


def test_admin_login_wrong_password(client):
    res = client.post("/admin/login", data={
        "username": "admin",
        "password": "wrong",
    }, follow_redirects=True)
    assert "Нэвтрэх нэр эсвэл нууц үг буруу байна." in res.data.decode()


def test_admin_login_wrong_username(client):
    res = client.post("/admin/login", data={
        "username": "hacker",
        "password": "admin123",
    }, follow_redirects=True)
    assert "Нэвтрэх нэр эсвэл нууц үг буруу байна." in res.data.decode()


def test_admin_logout(client):
    client.post("/admin/login", data={"username": "admin", "password": "admin123"})
    res = client.get("/admin/logout", follow_redirects=True)
    assert "Системээс гарлаа." in res.data.decode()
