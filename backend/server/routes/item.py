from fastapi import APIRouter, Body

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from server.database import (fetch_all_items, fetch_one_item, create_item, delete_one_item, update_item)
from server.models.item import (ResponseModel, ErrorResponseModel, ItemSchema, UpdateItemModel,)

router = APIRouter()

@router.get("/items", response_description="Items retrieved")
async def get_items():
    items = await fetch_all_items()
    if items:
        return ResponseModel(items, "Items retrieved successfully")
    return ResponseModel(items, "Empty list returned")
    # raise HTTPException(404, "DB empty or Something went wrong}")

@router.get("/items/{id}", response_description="Item retrieved")
async def get_item(id):
    item = await fetch_one_item(id)
    if item:
        return ResponseModel(item, "Item retrieved successfully")
    return ErrorResponseModel("An error occured",404, "Item does not exist")

@router.post("/items", response_description="Item added to database")
async def post_item(item: ItemSchema = Body(...)):
    item = jsonable_encoder(item)
    new_item = await create_item(item)
    return ResponseModel(new_item, "Item added successfully")

@router.delete("/items/{id}", response_description="Item deleted from the database")
async def delete_item(id: str):
    deleted_item = await delete_one_item(id)
    if (deleted_item.deleted_count == 1):
        return ResponseModel(id, f"item with {id} deleted successfully")
    return ErrorResponseModel("An error occured", 404, f"item {id} does not exist")

@router.put("/items/{id}")
async def edit_item(id, input: UpdateItemModel = Body(...)):
    item = jsonable_encoder(input)
    response = await update_item(id, item)
    if response:
        return ResponseModel("Item with ID: {} update is successful".format(id), "item with id: {id} was successfully updated")
    return ErrorResponseModel("An error occurred", 404, "There was an error updating the item data.")


# @router.put("/items/{id}")
# async def edit_item(id: str, req: UpdateItemModel = Body(...)):
#     req = {k: v for k, v in req.dict().items() if v is not None}
#     updated_item = await update_item(id, req)
#     if updated_item:
#         return ResponseModel(
#             "Item with ID: {} update is successful".format(id),
#             "Updated successfully",
#         )
#     return ErrorResponseModel(
#         "An error occurred",
#         404,
#         "There was an error updating the item data.",
#     )