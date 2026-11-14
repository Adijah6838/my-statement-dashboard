import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base
from app.api.deps import get_db
from app.models import User, Statement
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    # Seed test data
    john = User(email="john@test.com", hashed_password=get_password_hash("pass"), full_name="John Doe")
    jane = User(email="jane@test.com", hashed_password=get_password_hash("pass"), full_name="Jane Roe")
    db.add_all([john, jane])
    db.commit()
    db.refresh(john)
    db.refresh(jane)

    # John's statements (Testing official balance rules)
    # WE MUST INCLUDE THE DESCRIPTION FIELD (It is nullable=False in the model)
    db.add(Statement(user_id=john.id, transaction_type="deposit", description="Test deposit", amount=1000, status="completed")) # +1000
    db.add(Statement(user_id=john.id, transaction_type="withdrawal", description="Test withdrawal", amount=200, status="completed")) # -200
    db.add(Statement(user_id=john.id, transaction_type="transfer", description="Test transfer out", amount=500, sender_name="John Doe", receiver_name="Jane Roe", status="completed")) # -500
    db.add(Statement(user_id=john.id, transaction_type="transfer", description="Test transfer in", amount=300, sender_name="Jane Roe", receiver_name="John Doe", status="completed")) # +300
    # John's total balance: 1000 - 200 - 500 + 300 = 600.0
    
    # Jane's statements
    db.add(Statement(user_id=jane.id, transaction_type="deposit", description="Test deposit", amount=5000, status="completed")) # +5000

    db.commit()
    db.close()
    
    yield
    
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def get_token(email):
    response = client.post("/api/auth/login", data={"username": email, "password": "pass"})
    return response.json()["access_token"]

def test_login():
    response = client.post("/api/auth/login", data={"username": "john@test.com", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_unauthorized_access():
    response = client.get("/api/statements/balance")
    assert response.status_code == 401

def test_official_balance_rules():
    token = get_token("john@test.com")
    response = client.get("/api/statements/balance", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["balance"] == 600.0

def test_cross_user_isolation_balance():
    john_token = get_token("john@test.com")
    jane_token = get_token("jane@test.com")
    
    john_res = client.get("/api/statements/balance", headers={"Authorization": f"Bearer {john_token}"})
    jane_res = client.get("/api/statements/balance", headers={"Authorization": f"Bearer {jane_token}"})
    
    assert john_res.json()["balance"] == 600.0
    assert jane_res.json()["balance"] == 5000.0

def test_cross_user_isolation_statements():
    john_token = get_token("john@test.com")
    jane_token = get_token("jane@test.com")
    
    john_res = client.get("/api/statements/", headers={"Authorization": f"Bearer {john_token}"})
    jane_res = client.get("/api/statements/", headers={"Authorization": f"Bearer {jane_token}"})
    
    assert john_res.json()["total"] == 4
    assert jane_res.json()["total"] == 1

def test_pagination():
    token = get_token("john@test.com")
    res = client.get("/api/statements/?skip=0&limit=2", headers={"Authorization": f"Bearer {token}"})
    data = res.json()
    assert len(data["items"]) == 2
    assert data["total"] == 4
    assert data["limit"] == 2