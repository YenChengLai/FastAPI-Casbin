from fastapi import FastAPI, HTTPException, Depends, Request
from casbin import Enforcer

app = FastAPI()

# Initialize Casbin enforcer with a model and policy file
enforcer = Enforcer("rbac_model.conf", "policy.csv")


# Define a dependency to check permission using Casbin
def check_permission(sub: str, request: Request, path: str):
    """ trigger casbin validation """
    if not enforcer.enforce(sub, "update" if request.method == "POST" else "get", path):
        raise HTTPException(status_code=403, detail="Permission denied")


# Define routes with RBAC authorization
@app.get("/role-management")
def role_management(_ = Depends(check_permission)):

    return {"message": "role-management accessed!"}


@app.get("/remote-device-access")
def remote_device_access(_ = Depends(check_permission)):

    return {"message": "remote-device-access accessed!"}


@app.get("/email-communication")
def email_communication(_ = Depends(check_permission)):

    return {"message": "email-communication accessed!"}


@app.get("/organization-management")
def organization_management(_ = Depends(check_permission)):

    return {"message": "organization-management accessed!"}

@app.get("/firmware-update")
def firmware_update(_ = Depends(check_permission)):

    return {"message": "firmware-update accessed!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
