""" import fastapi and casbin """
from fastapi import FastAPI, HTTPException, Depends
from casbin import Enforcer

app = FastAPI()

# Initialize Casbin enforcer with a model and policy file
enforcer = Enforcer("rbac_model.conf", "policy.csv")


# Define a dependency to check permission using Casbin
def check_permission(role: str, path: str):
    """ trigger casbin validation """
    print(role)
    print(path)

    if not enforcer.enforce(role, path, "GET"):
        raise HTTPException(status_code=403, detail="Permission denied")


# Define routes with RBAC authorization
@app.get("/admin")
def admin_panel(_ = Depends(check_permission)):
    """ mock admin """
    return {"message": "Welcome to the admin panel!"}


@app.get("/developer")
def developer_panel(_ = Depends(check_permission)):
    """ mock developer """
    return {"message": "Welcome to the developer panel!"}


@app.get("/user")
def user_panel(_ = Depends(check_permission)):
    """ mock user """
    return {"message": "Welcome to the user panel!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
