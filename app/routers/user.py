from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.dependencies import require_role
from app.schemas.user import UpdateUserRole

router = APIRouter(prefix="/users", tags=["Users"])

@router.put("/{user_id}/role")
def update_user_role(
    user_id: int,
    data: UpdateUserRole,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    if data.role not in ["viewer", "analyst", "admin"]:
        raise HTTPException(400, "Invalid role")

    user.role = data.role
    db.commit()

    return {"message": f"Role updated to {data.role}"}