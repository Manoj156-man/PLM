from sqlalchemy.orm import Session
from app import models
from app.agents.specialized import (
    IdeationAgent, DesignAgent, ManufacturingAgent,
    QualityControlAgent, InventoryAgent, SalesAgent,
    MaintenanceAgent, EndOfLifeAgent
)

AGENT_MAP = {
    models.ProductPhase.IDEATION: IdeationAgent,
    models.ProductPhase.DESIGN: DesignAgent,
    models.ProductPhase.MANUFACTURING: ManufacturingAgent,
    models.ProductPhase.QUALITY_CONTROL: QualityControlAgent,
    models.ProductPhase.INVENTORY: InventoryAgent,
    models.ProductPhase.SALES: SalesAgent,
    models.ProductPhase.MAINTENANCE: MaintenanceAgent,
    models.ProductPhase.END_OF_LIFE: EndOfLifeAgent,
}

class SupervisorAgent:
    def __init__(self, db: Session, product_id: int):
        self.db = db
        self.product_id = product_id
        self.product = self.db.query(models.Product).filter(models.Product.id == self.product_id).first()

    def process_current_phase(self):
        if not self.product:
            return {"error": "Product not found"}
            
        if self.product.status != models.ProductStatus.ACTIVE:
            return {"error": f"Cannot process product with status: {self.product.status}"}

        current_phase = self.product.current_phase
        agent_class = AGENT_MAP.get(current_phase)
        
        if not agent_class:
            return {"error": "No agent found for current phase"}
            
        agent = agent_class(self.db, self.product.id)
        
        # Add transition event for the supervisor
        event = models.LifecycleEvent(
            product_id=self.product.id,
            phase=current_phase,
            agent_id="SupervisorAgent",
            event_type="orchestration",
            description=f"Delegating processing to {agent.__class__.__name__}"
        )
        self.db.add(event)
        self.db.commit()

        # Run the specialized agent
        result = agent.run()
        
        if result.get("status") == "success" and result.get("recommended_next_phase"):
            next_phase = result["recommended_next_phase"]
            
            # Update product phase
            self.product.current_phase = next_phase
            self.db.commit()
            
            event = models.LifecycleEvent(
                product_id=self.product.id,
                phase=current_phase,
                agent_id="SupervisorAgent",
                event_type="transition",
                description=f"Transitioned product to {next_phase}"
            )
            self.db.add(event)
            self.db.commit()
            
            return {"message": f"Successfully completed {current_phase} and transitioned to {next_phase}", "agent_result": result}
            
        return {"message": f"Agent finished with status: {result.get('status')}", "agent_result": result}
