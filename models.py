import sqlalchemy

from database import Base


class Recipe(Base):
    __tablename__ = "recipe"

    recipe_id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    views = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    cooking_time = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    ingredients = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
