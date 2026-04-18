# Agentic AI Product Lifecycle Management (PLM) System

An advanced, full-stack demonstration of a Product Lifecycle Management (PLM) system driven by simulated Agentic Artificial Intelligence. This project is built to demonstrate how autonomous AI agents can act as a digital workforce to manage products from initial ideation through to manufacturing and end-of-life.

## 🚀 Project Overview

Traditional PLM systems require heavy manual data entry and human oversight at every phase transition. This project introduces an **Agentic AI Architecture** where:
- A **Supervisor Agent** oversees the global state of the product.
- **Specialized Agents** (Design, Manufacturing, Quality Control) execute tasks, generate insights, and report issues based on the current lifecycle phase.
- The system automatically triggers transitions, generates detailed audit logs, and creates dynamic pending tasks without human intervention.

## 💻 Tech Stack

**Frontend (Client)**
- **React 18 & TypeScript:** For a robust, type-safe component architecture.
- **Vite:** For ultra-fast hot module replacement and building.
- **Custom CSS / Glassmorphism:** A completely bespoke "Cyberpunk / Deep Space" aesthetic featuring complex keyframe animations, glowing neon accents, and heavy background blurring. (Tailwind CSS was intentionally bypassed to demonstrate advanced Vanilla CSS proficiency).

**Backend (Server)**
- **FastAPI (Python 3.11):** High-performance asynchronous API framework.
- **SQLAlchemy & PostgreSQL:** Relational database management with ORM mapping for handling complex Product, Event, Alert, and Task relationships.
- **Pydantic:** Strictest data validation and serialization.

**Infrastructure**
- **Docker & Docker Compose:** The entire stack (Frontend, Backend, and Database) is containerized for guaranteed reproducibility.

## 🧠 The Agentic AI Simulation

The core technical demonstration lies in the `/agents/trigger/{product_id}` endpoint. When a user triggers the AI:
1. **Context Retrieval:** The backend fetches the current state of the product from PostgreSQL.
2. **Phase Analysis:** The Supervisor Agent determines the current lifecycle phase (e.g., `design`, `manufacturing`).
3. **Delegation:** The Supervisor delegates responsibilities to a specialized agent. For instance, if the product is in `manufacturing`, the **Manufacturing Agent** is invoked.
4. **Action Execution:** The specialized agent simulates real-world AI processing by:
   - Creating an Event Log (e.g., "Analyzed supply chain constraints").
   - Generating new Tasks for human or sub-agent completion (e.g., "Source alternative silicon suppliers").
   - Potentially throwing Alerts based on probabilistic anomaly detection.
5. **State Mutation:** The product is autonomously advanced to the next logical phase.

## 🛠️ How to Run Locally

This project uses Docker to make setup completely painless.

### Prerequisites
- Docker
- Docker Compose

### Startup Instructions
1. Open a terminal in the root directory of this project.
2. Run the following command:
   ```bash
   docker compose up -d --build
   ```
3. Docker will automatically pull the necessary images, build the custom frontend/backend containers, and spin up the PostgreSQL database.
4. **The database automatically seeds itself** with dummy academic data upon the first successful startup!

### Accessing the Application
- **Frontend Dashboard:** [http://localhost:3000](http://localhost:3000)
- **Backend API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

## 🎨 Design & UX

The frontend was designed to visually represent the cutting-edge nature of Agentic AI. 
- **Dynamic Motion:** The application features a continuously orbiting deep-space background.
- **Staggered Animations:** Data grids and logs gracefully slide into view to prevent visual overwhelm.
- **Interactive States:** Interactive elements glow and pulse with neon accents to provide immediate visual feedback.

---
*Developed as an academic demonstration of applied Agentic AI in enterprise software architecture.*
