from sqlalchemy.orm import Session
from app.models import statement as models
from app.schemas import statement as schemas
from typing import Optional

def create_statement(db: Session, statement: schemas.StatementCreate, user_id: int):
    """Create a new financial statement for a specific user."""
    db_statement = models.Statement(
        user_id=user_id,
        transaction_type=statement.transaction_type,
        description=statement.description,
        amount=statement.amount,
        sender_name=statement.sender_name,
        receiver_name=statement.receiver_name,
        status=statement.status
    )
    db.add(db_statement)
    db.commit()
    db.refresh(db_statement)
    return db_statement

def get_statements(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 10,
    transaction_type: Optional[str] = None,
    sort_by: str = "date",
    sort_desc: bool = True
):
    """Get a paginated list of statements for a user."""
    query = db.query(models.Statement).filter(models.Statement.user_id == user_id)
    
    if transaction_type:
        query = query.filter(models.Statement.transaction_type == transaction_type)
        
    if sort_by == "amount":
        order_col = models.Statement.amount
    elif sort_by == "description":
        order_col = models.Statement.description
    else:
        order_col = models.Statement.date
        
    if sort_desc:
        query = query.order_by(order_col.desc())
    else:
        query = query.order_by(order_col.asc())
        
    return query.offset(skip).limit(limit).all()

def count_statements(db: Session, user_id: int, transaction_type: Optional[str] = None):
    """Count total statements for pagination."""
    query = db.query(models.Statement).filter(models.Statement.user_id == user_id)
    if transaction_type:
        query = query.filter(models.Statement.transaction_type == transaction_type)
    return query.count()

def calculate_balance(db: Session, user_id: int, full_name: str) -> float:
    """
    Calculate the balance based on the official challenge rules:
    - Deposit: add
    - Withdrawal: subtract
    - Transfer (receiver): add
    - Transfer (sender): subtract
    """
    statements = db.query(models.Statement).filter(models.Statement.user_id == user_id).all()
    balance = 0.0
    for stmt in statements:
        if stmt.transaction_type == "deposit":
            balance += stmt.amount
        elif stmt.transaction_type == "withdrawal":
            balance -= stmt.amount
        elif stmt.transaction_type == "transfer":
            if stmt.receiver_name == full_name:
                balance += stmt.amount
            elif stmt.sender_name == full_name:
                balance -= stmt.amount
    return balance