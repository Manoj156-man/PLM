from sqlalchemy.orm import Session
from app import models
from app.core import security

def seed_db(db: Session):
    # Check if we already have users
    if db.query(models.User).first():
        return # Already seeded
        
    print("Seeding database with initial academic dummy data...")
    
    # 1. Create Users
    admin = models.User(
        username="admin",
        email="admin@plm.com",
        hashed_password=security.get_password_hash("adminpassword"),
        role=models.UserRole.ADMIN
    )
    manager = models.User(
        username="manager",
        email="manager@plm.com",
        hashed_password=security.get_password_hash("password"),
        role=models.UserRole.MANAGER
    )
    db.add(admin)
    db.add(manager)
    db.commit()
    
    # 2. Create Products
    products = [
        models.Product(
            name="Autonomous Delivery Drone",
            description="A quadcopter drone designed for last-mile delivery in urban environments. Focuses on AI obstacle avoidance and battery efficiency.",
            current_phase=models.ProductPhase.DESIGN,
            status=models.ProductStatus.ACTIVE
        ),
        models.Product(
            name="Smart Fitness Mirror",
            description="An interactive mirror that acts as a personal trainer, tracking form and reps using computer vision.",
            current_phase=models.ProductPhase.MANUFACTURING,
            status=models.ProductStatus.ALERT
        ),
        models.Product(
            name="Eco-Friendly Water Bottle",
            description="A smart water bottle that tracks hydration and is made from 100% biodegradable ocean plastics.",
            current_phase=models.ProductPhase.IDEATION,
            status=models.ProductStatus.ACTIVE
        ),
        models.Product(
            name="Quantum Computing Accelerator",
            description="A PCIe add-in card for standard workstations that simulates quantum algorithms locally.",
            current_phase=models.ProductPhase.END_OF_LIFE,
            status=models.ProductStatus.COMPLETED
        )
    ]
    
    for p in products:
        db.add(p)
    db.commit()
    
    # 3. Add Some Seed Events and Tasks for the Drone (Product 1)
    drone = db.query(models.Product).filter(models.Product.name == "Autonomous Delivery Drone").first()
    
    if drone:
        db.add(models.LifecycleEvent(
            product_id=drone.id, phase=models.ProductPhase.IDEATION, agent_id="IdeationAgent",
            event_type="analysis", description="Analyzed market need for urban drone delivery. High demand detected."
        ))
        db.add(models.LifecycleEvent(
            product_id=drone.id, phase=models.ProductPhase.IDEATION, agent_id="SupervisorAgent",
            event_type="transition", description="Transitioned product to design phase."
        ))
        db.add(models.Task(
            product_id=drone.id, title="Draft Rotor Schematics", description="Create CAD files for high-efficiency rotors.",
            assigned_to_agent="DesignAgent", status=models.TaskStatus.IN_PROGRESS
        ))
        
    # 4. Add alerts for the mirror (Product 2)
    mirror = db.query(models.Product).filter(models.Product.name == "Smart Fitness Mirror").first()
    if mirror:
        db.add(models.Alert(
            product_id=mirror.id, severity=models.AlertSeverity.CRITICAL,
            message="[ManufacturingAgent] Supply chain shortage for reflective smart glass panels."
        ))
        
    db.commit()
    print("Database seeding completed.")
