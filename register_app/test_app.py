import os
import pytest

os.environ["SECRET_KEY"] = "test-secret"
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_PASSWORD"] = "admin123"

import register_app.app as app_module
from register_app.app import app, init_db


@pytest.fixture
def client(tmp_path):
    db_path = str(tmp_path / "test.db")
    app_module.DATABASE = db_path
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


# ---------------------------------------------------------------------------
# Registration (index) tests
# ---------------------------------------------------------------------------

def test_index_get(client):
    res = client.get("/")
    assert res.status_code == 200


def test_register_success(client):
    res = client.post("/", data={
        "last_name": "Бат",
        "first_name": "Болд",
        "phone": "99112233",
        "email": "bold@example.com",
    }, follow_redirects=True)
    assert res.status_code == 200
    assert "Бүртгэл амжилттай хийгдлээ." in res.data.decode()


def test_register_missing_last_name(client):
    res = client.post("/", data={
        "last_name": "",
        "first_name": "Болд",
        "phone": "99112233",
        "email": "bold@example.com",
    }, follow_redirects=True)
    assert "Овог оруулна уу." in res.data.decode()


def test_register_missing_first_name(client):
    res = client.post("/", data={
        "last_name": "Бат",
        "first_name": "",
        "phone": "99112233",
        "email": "bold@example.com",
    }, follow_redirects=True)
    assert "Нэр оруулна уу." in res.data.decode()


def test_register_missing_phone(client):
    res = client.post("/", data={
        "last_name": "Бат",
        "first_name": "Болд",
        "phone": "",
        "email": "bold@example.com",
    }, follow_redirects=True)
    assert "Утасны дугаар оруулна уу." in res.data.decode()


def test_register_invalid_phone(client):
    res = client.post("/", data={
        "last_name": "Бат",
        "first_name": "Болд",
        "phone": "abc",
        "email": "bold@example.com",
    }, follow_redirects=True)
    assert "Утасны дугаарын формат буруу байна." in res.data.decode()


def test_register_missing_email(client):
    res = client.post("/", data={
        "last_name": "Бат",
        "first_name": "Болд",
        "phone": "99112233",
        "email": "",
    }, follow_redirects=True)
    assert "Имэйл оруулна уу." in res.data.decode()


def test_register_invalid_email(client):
    res = client.post("/", data={
        "last_name": "Бат",
        "first_name": "Болд",
        "phone": "99112233",
        "email": "not-an-email",
    }, follow_redirects=True)
    assert "Имэйл хаяг зөв форматтай биш байна." in res.data.decode()


def test_register_duplicate_email(client):
    data = {
        "last_name": "Бат",
        "first_name": "Болд",
        "phone": "99112233",
        "email": "dup@example.com",
    }
    client.post("/", data=data, follow_redirects=True)
    res = client.post("/", data=data, follow_redirects=True)
    assert "өмнө нь бүртгэгдсэн байна." in res.data.decode()


# ---------------------------------------------------------------------------
# Admin login / logout tests
# ---------------------------------------------------------------------------

def test_admin_login_get(client):
    res = client.get("/admin/login")
    assert res.status_code == 200


def test_admin_login_success(client):
    res = client.post("/admin/login", data={
        "username": "admin",
        "password": "admin123",
    }, follow_redirects=True)
    assert res.status_code == 200
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


# ---------------------------------------------------------------------------
# Admin dashboard / protected routes
# ---------------------------------------------------------------------------

def test_admin_dashboard_requires_login(client):
    res = client.get("/admin", follow_redirects=True)
    assert "Админ хуудсанд нэвтрэх шаардлагатай." in res.data.decode()


def test_admin_dashboard_accessible_when_logged_in(client):
    client.post("/admin/login", data={"username": "admin", "password": "admin123"})
    res = client.get("/admin")
    assert res.status_code == 200


def test_admin_dashboard_shows_registration(client):
    client.post("/", data={
        "last_name": "Бат",
        "first_name": "Болд",
        "phone": "99112233",
        "email": "show@example.com",
    })
    client.post("/admin/login", data={"username": "admin", "password": "admin123"})
    res = client.get("/admin")
    assert b"show@example.com" in res.data


# ---------------------------------------------------------------------------
# Export Excel
# ---------------------------------------------------------------------------

def test_export_requires_login(client):
    res = client.get("/admin/export", follow_redirects=True)
    assert "Админ хуудсанд нэвтрэх шаардлагатай." in res.data.decode()


def test_export_returns_xlsx(client):
    client.post("/admin/login", data={"username": "admin", "password": "admin123"})
    res = client.get("/admin/export")
    assert res.status_code == 200
    assert res.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert len(res.data) > 0
