from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr, SecretStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from typing_extensions import Literal



# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    """
    Container for a single user record.
    """

    # The primary key for the UserModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    password: str = Field(..., min_length=5, max_length=20, description="user password")
    email: EmailStr = Field(...)
    role: Literal['CEO', 'Floor Manager', 'Factory Worker'] = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "12345678",
                "role": "CEO | Floor Manager | Factory Worker",
            }
        },
    )

class UserResponseModel(BaseModel):
    """
    Container for a single user record.
    """

    # The primary key for the UserModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    role: Literal['CEO', 'Floor Manager', 'Factory Worker'] = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "role": "CEO | Floor Manager | Factory Worker",
            }
        },
    )

class LoginModel(BaseModel):
    password: str = Field(..., min_length=5, max_length=20, description="user password")
    email: EmailStr = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "jdoe@example.com",
                "password": "12345678",
            }
        },
    )

class TokenSchema(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class UpdateUserModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """
    name: Optional[str] = None
    password: Optional[str] = Field(..., min_length=5, max_length=20, description="user password")
    role: Optional[Literal['CEO', 'Floor Manager', 'Factory Worker']]
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "password": "12345678",
                "role": "CEO | Floor Manager | Factory Worker",
            }
        },
    )


class UpdateRoleModel(BaseModel):
    """
    Update the role of the user.
    """
    email: EmailStr = Field(...)
    role: Literal['CEO', 'Floor Manager', 'Factory Worker']
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "email": "jdoe@example.com",
                "role": "CEO | Floor Manager | Factory Worker",
            }
        },
    )


class UserCollection(BaseModel):
    """
    A container holding a list of `UserModel` instances.
    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
    users: List[UserResponseModel]



class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserOut(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str


class SystemUser(UserOut):
    password: str