from pydantic import BaseModel, Field
from typing import Optional, Any
from bson import ObjectId
from pydantic import GetCoreSchemaHandler, field_serializer
from pydantic_core import core_schema


# Compatible with Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.no_info_after_validator_function(
                cls.validate, core_schema.str_schema()
            ),
            json_schema=core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: Any
    ) -> dict:
        return {"type": "string"}


class TaskBase(BaseModel):
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, Eggs, Bread")
    completed: bool = Field(default=False)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskInDB(TaskBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    @field_serializer("id")
    def serialize_id(self, v):
        return str(v)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "64a9a15b0b5d3c7b456e7e29",
                "title": "Buy groceries",
                "description": "Milk, Eggs, Bread",
                "completed": False,
            }
        }
