from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api import deps
from app.models.user import User
from app.schemas import StatementPage
from app.crud import statement as stmt_crud

router = APIRouter()

@router.get("/", response_model=StatementPage)
def read_statements(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100), # Max limit of 100 as per requirements
    transaction_type: Optional[str] = None,
    sort_by: str = "date",
    sort_desc: bool = True
):
    """Get paginated statements for the current user."""
    statements = stmt_crud.get_statements(
        db, user_id=current_user.id, skip=skip, limit=limit,
        transaction_type=transaction_type, sort_by=sort_by, sort_desc=sort_desc
    )
    total = stmt_crud.count_statements(db, user_id=current_user.id, transaction_type=transaction_type)
    
    return {"items": statements, "total": total, "skip": skip, "limit": limit}

@router.get("/balance")
def read_balance(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """Get the calculated balance for the current user."""
    balance = stmt_crud.calculate_balance(db, user_id=current_user.id, full_name=current_user.full_name)
    return {"balance": balance, "full_name": current_user.full_name}