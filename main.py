from typing import Annotated, Union

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from casbin import Enforcer
from pydantic import BaseModel


tags = [{"name": "Features", "description": "Features provided by OPTools"}]

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI(title="OPTool RBAC API Tests", openapi_tags=tags)


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# Initialize Casbin enforcer with a model and policy file
enforcer = Enforcer("rbac_model.conf", "policy.csv")


# Define a dependency to check permission using Casbin
def check_permission(sub: str, request: Request):
    """trigger casbin validation"""
    if not enforcer.enforce(
        sub, request.scope["path"][1:], "update" if request.method == "POST" else "get"
    ):
        raise HTTPException(status_code=403, detail="Permission denied")


# Define routes with RBAC authorization
@app.post("/role-management", tags=["Features"])
def role_management(_=Depends(check_permission)):
    """Editing users' roles and permissions"""
    return {"message": "role-management accessed!"}


@app.post("/remote-device-access", tags=["Features"])
def remote_device_access(_=Depends(check_permission)):
    """SSH into remote devices"""
    return {"message": "remote-device-access accessed!"}


@app.post("/email-communication", tags=["Features"])
def email_communication(_=Depends(check_permission)):
    """Sending emails to customers' accounts"""
    return {"message": "email-communication accessed!"}


@app.get("/organization-management", tags=["Features"])
def organization_management(_=Depends(check_permission)):
    """Search organization, site, and device's information"""
    return {"message": "organization-management accessed!"}


@app.post("/firmware-update", tags=["Features"])
def firmware_update(_=Depends(check_permission)):
    """Update remote device's firmware"""
    return {"message": "firmware-update accessed!"}


@app.get("/firmware-integrity", tags=["Features"])
def firmware_integrity(_=Depends(check_permission)):
    """Checking if there's any violation of firmware setting"""
    return {"message": "firmware-integrity accessed!"}


@app.get("/auditing", tags=["Features"])
def auditing(_=Depends(check_permission)):
    """Access auditing page to check user behaviors"""
    return {"message": "auditing accessed!"}


@app.post("/announcement", tags=["Features"])
def announcement_management(_=Depends(check_permission)):
    """Sending announcement to user accounts"""
    return {"message": "announcement management accessed!"}


@app.post("/approval", tags=["Features"])
def approval(_=Depends(check_permission)):
    """Grant pending permissions"""
    return {"message": "approval pending page accessed!"}


@app.post("/org-owner", tags=["Features"])
def org_owner_management(_=Depends(check_permission)):
    """Editing organization management"""
    return {"message": "org owner management accessed!"}


@app.post("/extend-trial", tags=["Features"])
def license_extension(_=Depends(check_permission)):
    """Extend customer's trial"""
    return {"message": "license extension accessed!"}


@app.post("/api-key", tags=["Features"])
def generate_api_key(_=Depends(check_permission)):
    """Generate OpenAPI key for customers"""
    return {"message": "generate api key accessed!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
