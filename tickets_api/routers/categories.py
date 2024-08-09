from fastapi import APIRouter
from tickets_api.schemas.category import CategoryCreate
from tickets_api.services.category_service import CategoryService
from tickets_api.utils.fastapi import load_state
from loguru import logger

router = APIRouter()


@router.get("/{category_id}")
async def get_categories(
    category_id: int, category_service: CategoryService = load_state(CategoryService)
):
    result = await category_service.get_category(category_id)
    logger.info(f"Category {category_id} found")
    return result


@router.get("")
async def get_all_categories(
    category_service: CategoryService = load_state(CategoryService),
):
    result = await category_service.get_all_categories()
    logger.info("All categories returned")
    return result


@router.post("")
async def create_category(
    category_create: CategoryCreate,
    category_service: CategoryService = load_state(CategoryService),
):
    result = await category_service.create_category(category_create)
    logger.info(f"Category {result.id} created")
    return result


@router.put("/{category_id}")
async def update_category(
    category_id: int,
    category: CategoryCreate,
    category_service: CategoryService = load_state(CategoryService),
):
    result = await category_service.update_category(category_id, category)
    logger.info(f"Category {category_id} updated")
    return result


@router.delete("/{category_id}")
async def delete_category(
    category_id: int, category_service: CategoryService = load_state(CategoryService)
):
    await category_service.delete_category(category_id)
    logger.info(f"Category {category_id} deleted")
    return {"message": "Category deleted successfully"}


@router.post("/{category_id}/subcategories")
async def create_subcategory(
    category_id: int,
    category_create: CategoryCreate,
    category_service: CategoryService = load_state(CategoryService),
):
    result = await category_service.create_subcategory(category_create, category_id)
    logger.info(f"Category {result.id} created as subcategory of {category_id}")
    return result


@router.put("/{category_id}/subcategory/{subcategory_id}")
async def append_subcategory(
    category_id: int,
    subcategory_id: int,
    category_service: CategoryService = load_state(CategoryService),
):
    result = await category_service.append_subcategory(category_id, subcategory_id)
    logger.info(f"Subcategory {subcategory_id} appended to category {category_id}")
    return result
