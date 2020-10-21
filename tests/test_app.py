import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_predict_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/predict", json={"artist": "shakira", "title": "waka waka"})
    assert response.status_code == 200

    data = response.json()
    assert len(data.keys()) == 1

    recommendations = data["recommendations"]
    assert len(recommendations) == 10

    for recommendation in recommendations:
        keys = recommendation.keys()
        assert len(keys) == 2
        assert "artists" in keys
        assert "title" in keys

        artists = recommendation["artists"]
        assert isinstance(artists, list)
        assert len(artists) > 0
        assert isinstance(recommendation["title"], str)


@pytest.mark.asyncio
async def test_predict_failure():
    artist = "asdf"
    title = ";lkj"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/predict", json={"artist": artist, "title": title})
    assert response.status_code == 200

    data = response.json()
    assert len(data.keys()) == 1

    assert data["error"] == f"{title} by {artist} not found."