from typing import Dict, Any
import random
from app.agents.base import BaseAgent
from app import models

class IdeationAgent(BaseAgent):
    def run(self) -> Dict[str, Any]:
        self.log_event("analysis", "Analyzing market trends and product description.")
        
        # Mock logic
        if "fail" in (self.product.description or "").lower():
            self.raise_alert(models.AlertSeverity.WARNING, "Idea seems unfeasible based on description.")
            return {"status": "failed", "message": "Ideation rejected.", "recommended_next_phase": None}
            
        self.create_task("Draft Initial Concept", "Create detailed technical specs based on idea.")
        self.save_memory("market_viability", "High")
        self.log_event("completion", "Ideation phase completed successfully.")
        
        return {
            "status": "success",
            "message": "Market viability is high. Ready for design.",
            "recommended_next_phase": models.ProductPhase.DESIGN
        }

class DesignAgent(BaseAgent):
    def run(self) -> Dict[str, Any]:
        self.log_event("analysis", "Reviewing specifications and creating CAD models.")
        
        viability = self.load_memory("market_viability")
        if not viability:
            self.log_event("warning", "No market viability data found, proceeding anyway.")
            
        self.create_task("Review Design", "Peer review the initial design models.")
        self.log_event("completion", "Design blueprints finalized.")
        
        return {
            "status": "success",
            "message": "Design completed.",
            "recommended_next_phase": models.ProductPhase.MANUFACTURING
        }

class ManufacturingAgent(BaseAgent):
    def run(self) -> Dict[str, Any]:
        self.log_event("analysis", "Allocating resources and starting production.")
        
        # Simulate occasional manufacturing issues
        if random.random() < 0.2:
            self.raise_alert(models.AlertSeverity.CRITICAL, "Supply chain shortage for key components.")
            return {"status": "blocked", "message": "Shortage of components.", "recommended_next_phase": None}
            
        self.log_event("completion", "Batch production completed.")
        return {
            "status": "success",
            "message": "Manufacturing finished.",
            "recommended_next_phase": models.ProductPhase.QUALITY_CONTROL
        }

class QualityControlAgent(BaseAgent):
    def run(self) -> Dict[str, Any]:
        self.log_event("analysis", "Running automated QA tests.")
        
        if random.random() < 0.15:
            self.raise_alert(models.AlertSeverity.WARNING, "Defect detected in 5% of batch.")
            return {"status": "failed", "message": "Failed QA tests.", "recommended_next_phase": models.ProductPhase.MANUFACTURING}
            
        self.log_event("completion", "All QA tests passed.")
        return {
            "status": "success",
            "message": "QA passed.",
            "recommended_next_phase": models.ProductPhase.INVENTORY
        }

class InventoryAgent(BaseAgent):
    def run(self) -> Dict[str, Any]:
        self.log_event("analysis", "Logging items into warehouse management system.")
        self.log_event("completion", "Stock registered.")
        return {
            "status": "success",
            "message": "Inventory updated.",
            "recommended_next_phase": models.ProductPhase.SALES
        }

class SalesAgent(BaseAgent):
    def run(self) -> Dict[str, Any]:
        self.log_event("analysis", "Launching product to storefront and tracking sales.")
        self.log_event("completion", "Sales targets met, moving to maintenance mode.")
        return {
            "status": "success",
            "message": "Product deployed and selling.",
            "recommended_next_phase": models.ProductPhase.MAINTENANCE
        }

class MaintenanceAgent(BaseAgent):
    def run(self) -> Dict[str, Any]:
        self.log_event("analysis", "Monitoring customer feedback and warranty claims.")
        
        # Determine if EOL should happen
        if "old" in (self.product.name or "").lower():
            return {
                "status": "success",
                "message": "Product is obsolete, recommending End of Life.",
                "recommended_next_phase": models.ProductPhase.END_OF_LIFE
            }
            
        return {
            "status": "success",
            "message": "Product operating normally.",
            "recommended_next_phase": None # Stay in maintenance
        }

class EndOfLifeAgent(BaseAgent):
    def run(self) -> Dict[str, Any]:
        self.log_event("analysis", "Initiating recall, recycling, and discontinuation protocols.")
        self.product.status = models.ProductStatus.COMPLETED
        self.db.commit()
        
        self.log_event("completion", "Product lifecycle fully terminated.")
        return {
            "status": "success",
            "message": "Product successfully retired.",
            "recommended_next_phase": None
        }
