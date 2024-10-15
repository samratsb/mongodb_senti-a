from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Use the connection string you got from MongoDB Atlas
MONGODB_URI = "mongodb+srv://mongodb:mongodb@cluster0.3shd3.mongodb.net/db1?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGODB_URI)
db = client.db1
collection = db.collec1

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = Field(default=None)

@app.post("/items/")
async def create_item(item: Item):
    new_item = await collection.insert_one(item.dict())
    created_item = await collection.find_one({"_id": new_item.inserted_id})

    # Convert ObjectId to string for JSON serialization
    created_item["_id"] = str(created_item["_id"])
    return {"id": created_item["_id"], **created_item}

@app.get("/items/")
async def get_items():
    items = []
    async for item in collection.find():
        item_dict = {**item}
        item_dict["_id"] = str(item_dict["_id"])
        items.append(item_dict)
    return items

@app.delete("/items/")
async def delete_all_items():
    result = await collection.delete_many({})
    return {"message": f"Deleted {result.deleted_count} items."}