from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class StateUserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: int = Field(...)
    username: str = Field(...)
    state: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": 123456789,
                "username": "bob",
                "state": "reverse",
            }
        }

class UpdateUserModel(BaseModel):
    user_id: Optional[int] = Field(...)
    username: Optional[str] = Field(...)
    state: Optional[str] = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": 123456789,
                "username": "bob",
                "state": "reverse",
            }
        }

class UpdateUserStateModel(BaseModel):
    state: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "state": "reverse",
            }
        }