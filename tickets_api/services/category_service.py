from fastapi import HTTPException
from loguru import logger

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import selectinload

from tickets_api.database.repository import SqlAlchemyRepositoryMixin
from tickets_api.schemas.category import CategoryCreate
from tickets_api.database.models.category import Category


class CategoryService(SqlAlchemyRepositoryMixin):
    def __init__(self, db_engine: AsyncEngine):
        super().__init__(db_engine)

    async def create_category(self, category_data: CategoryCreate):
        new_category = Category(
            name=category_data.name,
            description=category_data.description,
            active=category_data.active,
            parent_id=None,
        )
        async with self.session() as session:
            session.add(new_category)
            await session.commit()
            await session.refresh(new_category)
            return new_category

    async def get_category(self, category_id: int):
        async with self.session() as session:
            stmt = (
                select(Category)
                .options(selectinload(Category.sub_categories, recursion_depth=-1))
                .filter_by(id=category_id)
            )
            result = await session.execute(stmt)
            category = result.scalars().first()
            if not category:
                logger.error(f"Category {category_id} not found for retrieval")
                raise HTTPException(status_code=404, detail="Category not found")
            category.sub_categories
            return category

    async def update_category(self, category_id, category_data):
        async with self.session() as session:
            category = await session.get(Category, category_id)
            if not category:
                logger.error(f"Category {category_id} not found for update")
                raise HTTPException(status_code=404, detail="Category not found")
            category.name = category_data.name
            category.description = category_data.description
            category.active = category_data.active
            await session.commit()
            await session.refresh(category)
            return category

    async def delete_category(self, category_id):
        async with self.session() as session:
            category = await session.get(Category, category_id)
            if not category:
                logger.error(f"Category {category_id} not found for deletion")
                raise HTTPException(status_code=404, detail="Category not found")
            await session.delete(category)
            await session.commit()

    async def get_all_categories(self):
        async with self.session() as session:
            stmt = (
                select(Category)
                .where(Category.parent_id.is_(None))
                .options(selectinload(Category.sub_categories, recursion_depth=-1))
            )
            result = await session.execute(stmt)
            return list(result.scalars().unique().all())

    async def create_subcategory(self, category_data: CategoryCreate, parent_id: int):
        new_category = Category(
            name=category_data.name,
            description=category_data.description,
            active=category_data.active,
            parent_id=parent_id,
        )
        async with self.session() as session:
            session.add(new_category)
            await session.commit()
            await session.refresh(new_category)
            return new_category

    def get_all_subcategory_ids(self, category):
        sub_categories = category.sub_categories
        subcategory_ids = []
        for subcategory in sub_categories:
            subcategory_ids.append(subcategory.id)
            subcategory_ids.extend(self.get_all_subcategory_ids(subcategory))
        return subcategory_ids

    async def append_subcategory(self, category_id, subcategory_id):
        async with self.session() as session:
            result = await session.execute(
                select(Category)
                .where(Category.id == category_id)
                .options(selectinload(Category.sub_categories, recursion_depth=-1))
            )
            category = result.scalars().first()
            if not category:
                logger.error(
                    f"Error appending subcategory. Category {category_id} not found"
                )
                raise HTTPException(status_code=404, detail="Category not found")
            result = await session.execute(
                select(Category)
                .where(Category.id == subcategory_id)
                .options(selectinload(Category.sub_categories, recursion_depth=-1))
            )
            subcategory = result.scalars().first()
            if not subcategory:
                logger.error(
                    f"Error appending subcategory. Subcategory {subcategory_id} not found"
                )
                raise HTTPException(status_code=404, detail="Subcategory not found")

            subcategory_ids = self.get_all_subcategory_ids(subcategory)
            if category_id in subcategory_ids:
                logger.error(
                    f"Error appending subcategory. Subcategory {subcategory_id} is a parent of category {category_id}"
                )
                raise HTTPException(
                    status_code=400,
                    detail=f"Forbidden operation. Subcategory {subcategory_id} is a parent of category {category_id}",
                )
            category.sub_categories.append(subcategory)
            await session.commit()
            await session.refresh(category)
            return category
