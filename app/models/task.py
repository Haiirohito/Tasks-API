from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, V):
        if not ObjectId.is_valid(V):
            raise ValueError("Invalid ObjectID")
        return ObjectId(V)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema):
        from pydantic import core_schema
        
        string_schema = core_schema.str_schema()
        return string_schema


class TaskBase(BaseModel):
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, Eggs, Bread")
    completed: bool = Field(default=False)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    completed: Optional[bool]


class TaskInDB(TaskBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "64a9a15b0b5d3c7b456e7e29",
                "title": "Buy groceries",
                "description": "Milk, Eggs, Bread",
                "completed": False,
            }
        }
