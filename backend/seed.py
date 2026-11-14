from app.db.database import SessionLocal, engine, Base
from app.models import User, Statement
from app.core.security import get_password_hash

def seed_data():
    print("Resetting database...")
    # Delete all existing data to ensure a clean seed
    db = SessionLocal()
    db.query(Statement).delete()
    db.query(User).delete()
    db.commit()

    print("Creating users...")
    # User 1: John Doe
    john = User(
        email="john.doe@email.com",
        hashed_password=get_password_hash("Challenge@123"),
        full_name="John Doe"
    )
    # User 2: Jane Roe
    jane = User(
        email="jane.roe@email.com",
        hashed_password=get_password_hash("Challenge@123"),
        full_name="Jane Roe"
    )
    # User 3: Alice Smith (For isolation testing)
    alice = User(
        email="alice.smith@email.com",
        hashed_password=get_password_hash("Challenge@123"),
        full_name="Alice Smith"
    )
    
    db.add(john)
    db.add(jane)
    db.add(alice)
    db.commit()
    db.refresh(john)
    db.refresh(jane)
    db.refresh(alice)

    print("Creating statements for John Doe...")
    john_statements = [
        Statement(user_id=john.id, transaction_type="deposit", description="Initial Deposit", amount=10000.00, sender_name="Bank", receiver_name="John Doe", status="completed"),
        Statement(user_id=john.id, transaction_type="deposit", description="Salary", amount=5000.00, sender_name="Employer", receiver_name="John Doe", status="completed"),
        Statement(user_id=john.id, transaction_type="withdrawal", description="ATM Withdrawal", amount=500.00, status="completed"),
        Statement(user_id=john.id, transaction_type="transfer", description="Sent to Mary", amount=1000.00, sender_name="John Doe", receiver_name="Mary Jane", status="completed"),
        Statement(user_id=john.id, transaction_type="transfer", description="Received from Bob", amount=1991.00, sender_name="Bob Smith", receiver_name="John Doe", status="completed"),
    ]
    # Balance calculation: 10000 + 5000 - 500 - 1000 + 1991 = 15491.00

    print("Creating statements for Jane Roe...")
    jane_statements = [
        Statement(user_id=jane.id, transaction_type="deposit", description="Freelance Payment", amount=4200.00, sender_name="Client", receiver_name="Jane Roe", status="completed"),
    ]
    # Balance calculation: 4200.00

    print("Creating statements for Alice Smith (Isolation Test)...")
    alice_statements = [
        Statement(user_id=alice.id, transaction_type="deposit", description="Bonus", amount=500.00, sender_name="Bank", receiver_name="Alice Smith", status="completed"),
    ]

    db.add_all(john_statements)
    db.add_all(jane_statements)
    db.add_all(alice_statements)
    db.commit()
    
    print("Database seeded successfully!")
    print("Users created:")
    print("1. john.doe@email.com / Challenge@123 (Balance: 15491.00)")
    print("2. jane.roe@email.com / Challenge@123 (Balance: 4200.00)")
    print("3. alice.smith@email.com / Challenge@123 (Isolation Test)")

if __name__ == "__main__":
    seed_data()