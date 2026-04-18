from app.db.session import SessionLocal
from app.db.seed import seed_db
from app.db.base_class import Base
from app.db.session import engine
from app.api.endpoints.agents import trigger_agent_for_product

Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_db(db)

try:
    res = trigger_agent_for_product(1, db)
    print("SUCCESS:", res)
except Exception as e:
    import traceback
    traceback.print_exc()

