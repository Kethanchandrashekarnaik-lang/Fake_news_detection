import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TRUTHLENS" in response.data

def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data

def test_analyze_page_requires_login(client):
    response = client.get("/analyze")
    assert response.status_code == 302 # Redirects to login
    assert b"/login" in response.data
