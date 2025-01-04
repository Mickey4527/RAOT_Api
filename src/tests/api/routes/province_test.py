import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app 
from src.schemas import ProvinceSchema, QueryGeographySchema, Result
from src.models import Province
from src.routers.deps import SessionDep

# Create test client
client = TestClient(app)


@pytest.fixture
async def test_session():
    """
    Fixture for providing a test database session.
    Replace with the appropriate session for testing (e.g., SQLite in-memory).
    """
    async with AsyncSession(bind=app.state.engine) as session:
        yield session


# Override dependencies for testing
app.dependency_overrides[SessionDep] = lambda: test_session


def test_get_provinces_empty_response(test_session):
    response = client.get("/province/")
    assert response.status_code == 404
    result = response.json()
    assert result["success"] is False
    assert result["message"] == "Provinces not found"


@pytest.mark.asyncio
async def test_create_province(test_session):
    data = {
        "name_th": "กรุงเทพมหานคร",
        "name_en": "Bangkok",
        "code": 1,
        "geography_id": 1,
    }
    response = client.post("/province/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert result["message"] == "Province created successfully"
    assert result["data"]["name_th"] == data["name_th"]
    assert result["data"]["name_en"] == data["name_en"]


@pytest.mark.asyncio
async def test_create_duplicate_province(test_session):
    data = {
        "name_th": "กรุงเทพมหานคร",
        "name_en": "Bangkok",
        "code": 1,
        "geography_id": 1,
    }
    # First creation
    client.post("/province/", json=data)

    # Duplicate creation
    response = client.post("/province/", json=data)
    assert response.status_code == 400
    result = response.json()
    assert result["success"] is False
    assert result["message"] == "Province already exists"


@pytest.mark.asyncio
async def test_update_province(test_session):
    # Create province first
    data_create = {
        "name_th": "เชียงใหม่",
        "name_en": "Chiang Mai",
        "code": 2,
        "geography_id": 1,
    }
    client.post("/province/", json=data_create)

    # Update province
    data_update = {
        "name_th": "เชียงใหม่",
        "name_en": "Chiang Mai Updated",
        "code": 2,
        "geography_id": 1,
    }
    response = client.put("/province/2", json=data_update)
    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert result["message"] == "Province updated successfully"


@pytest.mark.asyncio
async def test_update_nonexistent_province(test_session):
    data_update = {
        "name_th": "ไม่มีอยู่จริง",
        "name_en": "Nonexistent",
        "code": 99,
        "geography_id": 1,
    }
    response = client.put("/province/99", json=data_update)
    assert response.status_code == 404
    result = response.json()
    assert result["success"] is False
    assert result["message"] == "Province not found"


@pytest.mark.asyncio
async def test_delete_province(test_session):
    # Create province first
    data_create = {
        "name_th": "ภูเก็ต",
        "name_en": "Phuket",
        "code": 3,
        "geography_id": 1,
    }
    client.post("/province/", json=data_create)

    # Delete province
    response = client.delete("/province/3")
    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert result["message"] == "Province deleted successfully"


@pytest.mark.asyncio
async def test_delete_nonexistent_province(test_session):
    response = client.delete("/province/99")
    assert response.status_code == 404
    result = response.json()
    assert result["success"] is False
    assert result["message"] == "Province not found"
