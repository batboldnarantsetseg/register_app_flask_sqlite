import os
import pytest

os.environ["SECRET_KEY"] = "test-secret"
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_PASSWORD"] = "admin123"

import register_app.app as app_module
from register_app.app import app, init_db


@pytest.fixture
def client(tmp_path):
    app_module.DATABASE = str(tmp_path / "test.db")
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
