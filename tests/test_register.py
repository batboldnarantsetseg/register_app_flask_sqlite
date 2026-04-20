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
