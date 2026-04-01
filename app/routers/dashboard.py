from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Record
from app.dependencies import get_current_user
from app.dependencies import require_role

from fastapi import Query
import datetime as dt

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["analyst", "admin"])),

    #  Filters
    start_date: dt.date | None = Query(None),
    end_date: dt.date | None = Query(None),
    category: str | None = Query(None),
    record_type: str | None = Query(None),

    # 📄 Pagination
    limit: int = Query(5, le=50),
    offset: int = Query(0)
):
    user_id = current_user.id

    #  Base Query
    query = db.query(Record).filter(Record.user_id == user_id)

    if start_date:
        query = query.filter(Record.date >= start_date)

    if end_date:
        query = query.filter(Record.date <= end_date)

    if category:
        query = query.filter(Record.category == category)

    if record_type:
        query = query.filter(Record.type == record_type)

    #  Aggregations
    total_income = query.filter(Record.type == "income")\
        .with_entities(func.sum(Record.amount)).scalar() or 0

    total_expense = query.filter(Record.type == "expense")\
        .with_entities(func.sum(Record.amount)).scalar() or 0

    net_balance = total_income - total_expense

    #  Category totals
    category_data = query.with_entities(
        Record.category,
        func.sum(Record.amount)
    ).group_by(Record.category).all()

    category_totals = [
        {"category": c, "total": float(t)}
        for c, t in category_data
    ]

    # Paginated recent transactions
    recent = query.order_by(Record.date.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()

    recent_transactions = [
        {
            "id": r.id,
            "amount": r.amount,
            "type": r.type,
            "category": r.category,
            "date": r.date
        }
        for r in recent
    ]

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "category_totals": category_totals,
        "recent_transactions": recent_transactions,
        "pagination": {
            "limit": limit,
            "offset": offset
        }
    }