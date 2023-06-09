from backend.schemas import Todo
from motor import motor_asyncio

client = motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client.Todo
collection = database.Item


async def get_item_by_title(title):
    item = await collection.find_one({'title': title})
    return item


async def get_all_todos():
    todos = []
    cursor = collection.find({})
    async for item in cursor:
        todos.append(Todo(**item))
    return todos


async def create_item(item):
    res = await collection.insert_one(item)
    return res


async def update_item(title, description):
    await collection.update_one({'title': title}, {'$set':
                                                       {'description':
                                                            description}})
    item = await collection.find_one({'title': title})
    return item


async def delete_item(title):
    collection.delete_one({'title': title})
    return True
