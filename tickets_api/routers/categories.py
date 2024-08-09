from fastapi import APIRouter
from tickets_api.schemas.category import CategoryCreate
from tickets_api.services.category_service import CategoryService
from tickets_api.utils.fastapi import load_state

router = APIRouter()


@router.get("/{category_id}")
async def get_categories(
    category_id: int, category_service: CategoryService = load_state(CategoryService)
):
    return await category_service.get_category(category_id)


@router.get("")
async def get_all_categories(
    category_service: CategoryService = load_state(CategoryService),
):
    return await category_service.get_all_categories()


@router.post("")
async def create_category(
    category_create: CategoryCreate,
    category_service: CategoryService = load_state(CategoryService),
):
    return await category_service.create_category(category_create)


@router.put("/{category_id}")
async def update_category(
    category_id: int,
    category: CategoryCreate,
    category_service: CategoryService = load_state(CategoryService),
):
    return await category_service.update_category(category_id, category)


@router.delete("/{category_id}")
async def delete_category(
    category_id: int, category_service: CategoryService = load_state(CategoryService)
):
    await category_service.delete_category(category_id)
    return {"message": "Category deleted successfully"}


@router.post("/{category_id}/subcategories")
async def create_subcategory(
    category_id: int,
    category_create: CategoryCreate,
    category_service: CategoryService = load_state(CategoryService),
):
    return await category_service.create_subcategory(category_create, category_id)


@router.put("/{category_id}/subcategory/{subcategory_id}")
async def append_subcategory(
    category_id: int,
    subcategory_id: int,
    category_service: CategoryService = load_state(CategoryService),
):
    return await category_service.append_subcategory(category_id, subcategory_id)
