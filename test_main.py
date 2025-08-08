import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_get_recipes():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/recipes/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_recipe():
    new_recipe = {
        "title": "Борщ",
        "cooking_time": 120.0,
        "ingredients": "Свекла, картофель, капуста, морковь, лук",
        "description": "Классический рецепт борща",
    }
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.post("/recipes/", json=new_recipe)
        assert response.status_code == 200
        new_recipe = response.json()
        assert new_recipe["title"] == "Борщ"
        assert new_recipe["cooking_time"] == 120.0


@pytest.mark.asyncio
async def test_get_recipe_detail():
    recipe_data = {
        "title": "Окрошка",
        "cooking_time": 30.0,
        "ingredients": "Кефир, картофель, редис, укроп, яйцо, огурец",
        "description": "Освежающее летнее блюдо",
    }

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        create_response = await client.post("/recipes/", json=recipe_data)
        assert create_response.status_code == 200
        response_data = create_response.json()
        recipe_id = response_data.get("recipe_id")
        assert recipe_id is not None
        detail_response = await client.get(f"/recipes/{recipe_id}")
        assert detail_response.status_code == 200
        detail_data = detail_response.json()
        assert detail_data["title"] == "Окрошка"
        assert detail_data["cooking_time"] == 30.0
