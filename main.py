import logging
from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from models import Recipe
from schemas import RecipeIn, RecipeOut
from database import engine
import models

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
logger = logging.getLogger("app")
@app.get('/recipes/', response_model=List[RecipeOut])
async def get_recipes():
    """Получить список всех рецептов, отсортированных по количеству просмотров и времени приготовления."""
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(Recipe).order_by(Recipe.views.desc(), Recipe.cooking_time))
            return result.scalars().all()

@app.get('/recipes/{recipe_id}', response_model=RecipeOut)
async def get_recipe_detail(recipe_id: int):
    # """Получить детальную информацию о конкретном рецепте по идентификатору."""
    # logger.info(f"Запрос детали рецепта: {recipe_id}")
    async with SessionLocal() as session:
        async with session.begin():
            recipe = await session.get(Recipe, recipe_id)
            if not recipe:
                raise HTTPException(status_code=404, detail="Рецепт не найден")
            recipe.views += 1
            await session.commit()
            return recipe


@app.post('/recipes/', response_model=RecipeOut)
async def create_recipe(recipe: RecipeIn):
    """Создать новый рецепт на основе предоставленных данных."""
    new_recipe = Recipe(**recipe.dict())
    async with SessionLocal() as session:
        try:
            async with session.begin():
                session.add(new_recipe)
            await session.refresh(new_recipe)
            return new_recipe
        except Exception as e:
            logger.error(f"Ошибка создания рецепта: {e}")
            raise HTTPException(status_code=400, detail=str(e))



