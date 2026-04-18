from abc import ABC, abstractmethod
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app import models
import json

class BaseAgent(ABC):
    def __init__(self, db: Session, product_id: int):
        self.db = db
        self.product_id = product_id
        self.product = self.db.query(models.Product).filter(models.Product.id == self.product_id).first()
        self.agent_id = self.__class__.__name__

    def load_memory(self, key: str) -> Any:
        mem = self.db.query(models.AgentMemory).filter(
            models.AgentMemory.agent_id == self.agent_id,
            models.AgentMemory.product_id == self.product_id,
            models.AgentMemory.key == key
        ).first()
        if mem:
            try:
                return json.loads(mem.value)
            except:
                return mem.value
        return None

    def save_memory(self, key: str, value: Any):
        mem = self.db.query(models.AgentMemory).filter(
            models.AgentMemory.agent_id == self.agent_id,
            models.AgentMemory.product_id == self.product_id,
            models.AgentMemory.key == key
        ).first()
        str_value = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
        
        if mem:
            mem.value = str_value
        else:
            mem = models.AgentMemory(
                agent_id=self.agent_id,
                product_id=self.product_id,
                key=key,
                value=str_value
            )
            self.db.add(mem)
        self.db.commit()

    def log_event(self, event_type: str, description: str):
        event = models.LifecycleEvent(
            product_id=self.product_id,
            phase=self.product.current_phase,
            agent_id=self.agent_id,
            event_type=event_type,
            description=description
        )
        self.db.add(event)
        self.db.commit()

    def create_task(self, title: str, description: str):
        task = models.Task(
            product_id=self.product_id,
            title=title,
            description=description,
            assigned_to_agent=self.agent_id
        )
        self.db.add(task)
        self.db.commit()
        return task

    def raise_alert(self, severity: models.AlertSeverity, message: str):
        alert = models.Alert(
            product_id=self.product_id,
            severity=severity,
            message=f"[{self.agent_id}] {message}"
        )
        self.db.add(alert)
        self.db.commit()
        
        self.product.status = models.ProductStatus.ALERT
        self.db.commit()
        return alert

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Main execution logic for the agent.
        Returns a dictionary with status, message, and recommended_next_phase.
        """
        pass
