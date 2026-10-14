from app.core.database import SessionLocal
from app.agent.tools import get_order_details


db = SessionLocal()

try:
    print("Existing order:")
    print(get_order_details(1, db))

    print("\nNonexistent order:")
    print(get_order_details(99999, db))
finally:
    db.close()