from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.agents.supervisor import SupervisorAgent

router = APIRouter()

@router.post("/trigger/{product_id}")
def trigger_agent_for_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    supervisor = SupervisorAgent(db, product_id)
    result = supervisor.process_current_phase()
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result
