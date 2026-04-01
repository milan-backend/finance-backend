from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Record
from app.schemas.record import RecordCreate, RecordUpdate, RecordResponse
from app.dependencies import get_current_user
from app.dependencies import require_role

router = APIRouter(prefix="/records", tags=["Records"])


@router.post("/", response_model=RecordResponse)
def create_record(
    data: RecordCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):
    record = Record(
        **data.dict(),
        user_id=current_user.id   
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.get("/", response_model=list[RecordResponse])
def get_records(
    db: Session = Depends(get_db),
     current_user = Depends(require_role(["viewer", "analyst", "admin"]))
):
    records = db.query(Record)\
        .filter(Record.user_id == current_user.id)\
        .all()

    return records


@router.put("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int,
    data: RecordUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):
    record = db.query(Record).filter(Record.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record


@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):
    record = db.query(Record).filter(Record.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(record)
    db.commit()

    return {"message": "Record deleted"}