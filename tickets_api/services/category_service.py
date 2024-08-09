from fastapi import HTTPException

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import joinedload

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
                .options(joinedload(Category.sub_categories))
                .filter_by(id=category_id)
            )
            result = await session.execute(stmt)
            category = result.scalars().first()
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            category.sub_categories
            return category

    async def update_category(self, category_id, category_data):
        async with self.session() as session:
            category = await session.get(Category, category_id)
            if not category:
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
                raise HTTPException(status_code=404, detail="Category not found")
            await session.delete(category)
            await session.commit()

    async def get_all_categories(self):
        async with self.session() as session:
            stmt = select(Category).where(Category.parent_id.is_(None))
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

    async def append_subcategory(self, category_id, subcategory_id):
        async with self.session() as session:
            category = await session.get(Category, category_id)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            subcategory = await session.get(Category, subcategory_id)
            if not subcategory:
                raise HTTPException(status_code=404, detail="Subcategory not found")
            category.sub_categories.append(subcategory)
            await session.commit()
            await session.refresh(category)
            return category
