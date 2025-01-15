import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch
from app.main import app
from app.services import ProvinceService
from app.schemas import ProvinceSchema, QueryGeographySchema

client = TestClient(app)

# Mock data
mock_province = ProvinceSchema(
    code=1,
    name_th="Bangkok",
    name_en="Bangkok",
    geography_id=1
)

@pytest.fixture
def mock_session():
    """Fixture to mock AsyncSession."""
    return AsyncMock(spec=AsyncSession)

@pytest.mark.asyncio
async def test_get_provinces(mock_session):
    """Test the GET /province/ endpoint."""
    # Mock the service call
    with patch.object(
        ProvinceService, "get_provinces", return_value=[mock_province]
    ) as mock_service:
        response = client.get("/province/")
        mock_service.assert_called_once()

        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "message": "Provinces retrieved successfully",
            "data": [
                {
                    "code": 1,
                    "name_th": "Bangkok",
                    "name_en": "Bangkok",
                    "geography_id": 1
                }
            ]
        }

@pytest.mark.asyncio
async def test_create_province_success(mock_session):
    """Test the POST /province/ endpoint with success."""
    mock_session.add = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    with patch.object(
        ProvinceService, "create_province", return_value=mock_province
    ) as mock_service:
        response = client.post(
            "/province/",
            json={
                "code": 1,
                "name_th": "Bangkok",
                "name_en": "Bangkok",
                "geography_id": 1
            }
        )
        mock_service.assert_called_once()
        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "message": "Province created successfully",
            "data": {
                "code": 1,
                "name_th": "Bangkok",
                "name_en": "Bangkok",
                "geography_id": 1
            }
        }

@pytest.mark.asyncio
async def test_create_province_conflict(mock_session):
    """Test the POST /province/ endpoint when the province already exists."""
    with patch.object(
        ProvinceService, "create_province", return_value=False
    ) as mock_service:
        response = client.post(
            "/province/",
            json={
                "code": 1,
                "name_th": "Bangkok",
                "name_en": "Bangkok",
                "geography_id": 1
            }
        )
        mock_service.assert_called_once()
        assert response.status_code == 400
        assert response.json() == {
            "detail": {
                "success": False,
                "error_code": 400,
                "message": "Province already exists"
            }
        }

@pytest.mark.asyncio
async def test_update_province_not_found(mock_session):
    """Test the PUT /province/{code} endpoint when the province is not found."""
    with patch.object(
        ProvinceService, "update_province", return_value=False
    ) as mock_service:
        response = client.put(
            "/province/1",
            json={
                "code": 1,
                "name_th": "Bangkok Updated",
                "name_en": "Bangkok Updated",
                "geography_id": 1
            }
        )
        mock_service.assert_called_once()
        assert response.status_code == 404
        assert response.json() == {
            "success": False,
            "error_code": 404,
            "message": "Province not found"
        }

@pytest.mark.asyncio
async def test_delete_province_success(mock_session):
    """Test the DELETE /province/{code} endpoint with success."""
    with patch.object(
        ProvinceService, "delete_province", return_value=True
    ) as mock_service:
        response = client.delete("/province/1")
        mock_service.assert_called_once()
        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "message": "Province deleted successfully"
        }

@pytest.mark.asyncio
async def test_delete_province_not_found(mock_session):
    """Test the DELETE /province/{code} endpoint when the province is not found."""
    with patch.object(
        ProvinceService, "delete_province", return_value=False
    ) as mock_service:
        response = client.delete("/province/1")
        mock_service.assert_called_once()
        assert response.status_code == 404
        assert response.json() == {
            "detail": {
                "success": False,
                "error_code": 404,
                "message": "Province not found"
            }
        }
