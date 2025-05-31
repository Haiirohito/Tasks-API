async def get_all_tasks(collection):
    return await collection.find().to_list(100)


async def create_task(collection, task_data):
    result = await collection.insert_one(task_data)
    new_task = await collection.find_one({"_id": result.inserted_id})
    return new_task

# ... add update, delete, get by id, etc.