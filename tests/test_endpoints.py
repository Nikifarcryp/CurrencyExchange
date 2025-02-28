from fastapi.testclient import TestClient
from main import app
from app.core.security import hashed_password

client = TestClient(app)

def test_registration():
    response = client.get('auth/registration/', params=[hashed_password('Nik_234rftg5g')])
