from fastapi import HTTPException, Request


def require_admin(request: Request):
    if not request.session.get("admin"):
        raise HTTPException(
            status_code=303,
            headers={"Location": "/admin/login"}
        )

    return True