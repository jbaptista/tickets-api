import pytest


@pytest.mark.asyncio
async def test_create_category(app_client):
    app_client_instance = await app_client
    response = app_client_instance.post(
        "/categories",
        json={
            "name": "Test Category",
            "description": "Test Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "Test Description"
    assert data["active"] is True


@pytest.mark.asyncio
async def test_get_category(app_client):
    app_client_instance = await app_client
    response = app_client_instance.post(
        "/categories",
        json={
            "name": "Test Category",
            "description": "Test Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    category_id = data["id"]
    response = app_client_instance.get(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "Test Description"
    assert data["active"] == True


@pytest.mark.asyncio
async def test_get_all_categories(app_client):
    app_client_instance = await app_client
    response = app_client_instance.post(
        "/categories",
        json={
            "name": "Test Category",
            "description": "Test Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    response = app_client_instance.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Category"
    assert data[0]["description"] == "Test Description"
    assert data[0]["active"] == True


@pytest.mark.asyncio
async def test_update_category(app_client):
    app_client_instance = await app_client
    response = app_client_instance.post(
        "/categories",
        json={
            "name": "Test Category",
            "description": "Test Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    category_id = data["id"]
    response = app_client_instance.put(
        f"/categories/{category_id}",
        json={
            "name": "Updated Test Category",
            "description": "Updated Test Description",
            "active": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Test Category"
    assert data["description"] == "Updated Test Description"
    assert data["active"] == False


@pytest.mark.asyncio
async def test_delete_category(app_client):
    app_client_instance = await app_client
    response = app_client_instance.post(
        "/categories",
        json={
            "name": "Test Category",
            "description": "Test Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    category_id = data["id"]
    response = app_client_instance.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Category deleted successfully"


@pytest.mark.asyncio
async def test_create_subcategory(app_client):
    app_client_instance = await app_client
    response = app_client_instance.post(
        "/categories",
        json={
            "name": "Test Category",
            "description": "Test Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    category_id = data["id"]
    response = app_client_instance.post(
        f"/categories/{category_id}/subcategories",
        json={
            "name": "Test Subcategory",
            "description": "Test Subcategory Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Subcategory"
    assert data["description"] == "Test Subcategory Description"
    assert data["active"] == True
    assert data["parent_id"] == category_id


@pytest.mark.asyncio
async def test_append_subcategory(app_client):
    app_client_instance = await app_client
    response = app_client_instance.post(
        "/categories",
        json={
            "name": "Test Category",
            "description": "Test Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    category_id = data["id"]
    response = app_client_instance.post(
        "/categories",
        json={
            "name": "Test Subcategory",
            "description": "Test Subcategory Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    subcategory_id = data["id"]
    response = app_client_instance.put(
        f"/categories/{category_id}/subcategory/{subcategory_id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "Test Description"
    assert data["active"] == True
    assert data["parent_id"] == None
    assert len(data["sub_categories"]) == 1
    assert data["sub_categories"][0]["name"] == "Test Subcategory"
    assert data["sub_categories"][0]["description"] == "Test Subcategory Description"
    assert data["sub_categories"][0]["active"] == True
    assert data["sub_categories"][0]["parent_id"] == category_id


@pytest.mark.asyncio
async def test_get_category_not_found(app_client):
    app_client_instance = await app_client
    response = app_client_instance.get("/categories/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


@pytest.mark.asyncio
async def test_get_category_with_subcategories(app_client):
    app_client_instance = await app_client
    response = app_client_instance.post(
        "/categories",
        json={
            "name": "Test Category",
            "description": "Test Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    category_id = data["id"]
    response = app_client_instance.post(
        f"/categories/{category_id}/subcategories",
        json={
            "name": "Test Subcategory",
            "description": "Test Subcategory Description",
            "active": True,
        },
    )
    assert response.status_code == 200
    response = app_client_instance.get(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "Test Description"
    assert data["active"] == True
    assert data["sub_categories"][0]["name"] == "Test Subcategory"
    assert data["sub_categories"][0]["description"] == "Test Subcategory Description"
    assert data["sub_categories"][0]["active"] == True
    assert data["sub_categories"][0]["parent_id"] == category_id
