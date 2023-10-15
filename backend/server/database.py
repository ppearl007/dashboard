from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder


MONGODB_URL = "mongodb+srv://pelu:WH7VVxYUCxs4riiB@cluster0.ga23agj.mongodb.net/"
client = AsyncIOMotorClient(MONGODB_URL)

db = client.CTB
collection = db.items

# helpers

def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "uid": str(item["uid"]),
        "PN": item["PN"],
        "Desc": item["Desc"],
        "QtyStock": item["QtyStock"],
        "MOQ": item["MOQ"],
        "Price": item["Price"],
    }

async def fetch_all_items():
    items=[]
    async for item in collection.find():
        items.append(item_helper(item))
    return items

async def create_item(item: dict) -> dict:
    # document = jsonable_encoder(item)
    item = await collection.insert_one(item)
    new_item = await collection.find_one({"_id": item.inserted_id})
    return item_helper(new_item)

async def fetch_one_item(id: str) -> dict:
    item = await collection.find_one({"_id": ObjectId(id)})
    if item:
        return item_helper(item)
    
async def delete_one_item(id: str):
    result = await collection.find_one({"_id": ObjectId(id)}) 
    if result:
        result = await collection.delete_one({"_id": ObjectId(id)}) 
        return result
    
# Update an item with a matching ID
async def update_item(id, data: dict):
    document = jsonable_encoder(data)
    # if len(data) < 1:
    #     return data
    
    if len(document) >= 1:
        updated_result = await collection.update_one({"_id": ObjectId(id)}, {"$set": document})
        # print(updated_result.matched_count)
        # return updated_result

        if updated_result.modified_count == 1:
            if (updated_result := await collection.find_one({"_id": ObjectId(id)})) is not None:
                return updated_result
            
# async def update_item(id: str, data: dict):
#     # Return false if an empty request body is sent.
#     if len(data) < 1:
#         return False
#     item = await collection.find_one({"_id": ObjectId(id)})
#     if item:
#         updated_item = await collection.update_one(
#             {"_id": ObjectId(id)}, {"$set": data}
#         )
#         if updated_item:
#             return True
#         return False

