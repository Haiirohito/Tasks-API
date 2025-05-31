from fastapi import Request, Depends

def get_database(request: Request):
    return request.app.state.mongo_client["task_db"]

def get_collection(db=Depends(get_database)):
    return db["tasks"]
