def test_export_requires_login(client):
    res = client.get("/admin/export", follow_redirects=True)
    assert "Админ хуудсанд нэвтрэх шаардлагатай." in res.data.decode()


def test_export_returns_xlsx(client):
    client.post("/admin/login", data={"username": "admin", "password": "admin123"})
    res = client.get("/admin/export")
    assert res.status_code == 200
    assert res.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert len(res.data) > 0
