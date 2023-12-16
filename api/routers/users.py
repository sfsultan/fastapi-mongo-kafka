from fastapi import APIRouter, Body, HTTPException, status, Depends
from api.auth import create_access_token, create_refresh_token, get_hashed_password, verify_password
from api.models import UpdateRoleModel, UpdateUserModel, UserCollection, UserModel, LoginModel, UserResponseModel, TokenSchema, SystemUser, UserOut, TokenPayload
from api.dependencies import app
from api.auth import get_current_user
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["User"])



@router.post(
    "/signup/",
    summary="Register a new user",
    response_description="Register a new user",
    response_model=UserResponseModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def signup_user(user: UserModel = Body(...)):
    """
    Register a new user.
    A user will be created and provided in the response.
    """
    user_exists = await app.state.mongo_collection['users'].find_one(
        {"email": user.email}
    )
    if user_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    
    user.password = get_hashed_password(user.password)

    new_user = await app.state.mongo_collection['users'].insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await app.state.mongo_collection['users'].find_one(
        {"_id": new_user.inserted_id}
    )
    
    return created_user



@router.post(
    "/user/role/",
    summary="Set user role",
    response_description="Updated user",
    response_model=UserResponseModel,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def change_role(user: UpdateRoleModel = Body(...), current_user = Depends(get_current_user)):
    """
    Change or apply a user role.

    Only CEOs can perform this activity.
    """
    print("current_user >> ", current_user)

    if current_user.role != "CEO":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized action"
        )
    

    updated_user = await app.state.mongo_collection['users'].update_one(
        {"email": user.email},
        {"$set": {"role": user.role}}
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to update the user " + user.email
        )

    updated_user = await app.state.mongo_collection['users'].find_one(
        {"email": user.email}
    )
    
    return updated_user






@router.post(
    "/login/",
    summary="Create access and refresh token for user",
    response_description="Login a user",
    response_model=TokenSchema,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def login_user(user: OAuth2PasswordRequestForm  = Depends()):
    """
    Login a user.

    This will return an `access_token` and a `refresh_token`.
    """
    creds = user

    if creds is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    fetched_user = await app.state.mongo_collection['users'].find_one(
        {"email": creds.username}
    )

    hashed_pass = fetched_user['password']

    if not verify_password(user.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(fetched_user['email']),
        "refresh_token": create_refresh_token(fetched_user['email']),
    }






@router.get(
    "/users/",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def list_users():
    """
    List all of the user data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return UserCollection(users=await app.state.mongo_collection['users'].find().to_list(1000))




@router.get('/me', summary='Get details of currently logged in user', response_model=UserResponseModel, include_in_schema=False)
async def get_me(user: UserResponseModel = Depends(get_current_user)):
    print("user", user)
    return user


@router.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')