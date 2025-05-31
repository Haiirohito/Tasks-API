from bson import ObjectId


async def get_all_tasks(collection):
    return await collection.find().to_list(100)


async def get_task_by_id(collection, task_id: str):
    if not ObjectId.is_valid(task_id):
        return None
    return await collection.find_one({"_id": ObjectId(task_id)})


async def create_task(collection, task_data: dict):
    result = await collection.insert_one(task_data)
    return await collection.find_one({"_id": result.inserted_id})


async def update_task(collection, task_id: str, update_data: dict):
    if not ObjectId.is_valid(task_id):
        return False
    await collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})
    return await collection.find_one({"_id": ObjectId(task_id)})


async def delete_task(collection, task_id: str):
    if not ObjectId.is_valid(task_id):
        return False
    result = await collection.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count == 1
