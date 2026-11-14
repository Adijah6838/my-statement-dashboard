from app.db.database import SessionLocal
from app.schemas.user import UserCreate
from app.schemas.statement import StatementCreate
from app.crud import user as user_crud
from app.crud import statement as stmt_crud

db = SessionLocal()

# 1. Create a test user
print("--- Testing User CRUD ---")
# Using a different email in case you run it multiple times
user_in = UserCreate(email="crud_test2@email.com", password="password123", full_name="CRUD Tester")
db_user = user_crud.create_user(db, user_in)
print("User created:", db_user.email)

# 2. Create statements
print("\n--- Testing Statement CRUD ---")
stmt1 = StatementCreate(transaction_type="deposit", description="Salary", amount=5000.0, status="completed")
stmt2 = StatementCreate(transaction_type="withdrawal", description="Groceries", amount=200.0, status="completed")
stmt3 = StatementCreate(transaction_type="transfer", description="Sent to friend", amount=300.0, sender_name="CRUD Tester", receiver_name="Friend", status="completed")

stmt_crud.create_statement(db, stmt1, db_user.id)
stmt_crud.create_statement(db, stmt2, db_user.id)
stmt_crud.create_statement(db, stmt3, db_user.id)
print("3 statements created.")

# 3. Calculate balance
print("\n--- Testing Balance Calculation ---")
balance = stmt_crud.calculate_balance(db, db_user.id, db_user.full_name)
print(f"Calculated balance for {db_user.full_name}: ${balance}")

# 4. Test pagination
print("\n--- Testing Pagination ---")
paginated = stmt_crud.get_statements(db, db_user.id, skip=0, limit=2)
print(f"Retrieved {len(paginated)} statements (limit=2).")
print(f"Total count in DB: {stmt_crud.count_statements(db, db_user.id)}")