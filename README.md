<div align="center">

# InvenGuardCO

*Inventory Management System for Manufacturing Environments*

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-SSR-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791)

</div>


## About

**InvenGuardCO** is a web-based inventory management system designed for manufacturing environments. It enables real-time tracking of raw materials, production feasibility validation, and low-stock alerts to support operational decision-making.

> [!NOTE]
> This is a personal project that models a fictional but realistic industrial scenario inspired by common challenges in manufacturing environments.

For detailed analysis and requirements, see the [Documentation](#documentation) section.

---

## Contact 
For questions, suggestions, or collaboration opportunities, feel free to reach out!
✉️ <a href="mailto:keylersanchez00@gmail.com">Here 👋🏽 (Email)</a>

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTMX + Jinja2 Templates (SSR) |
| **Backend** | FastAPI |
| **ORM** | SQLAlchemy + SQLModel |
| **Database** | PostgreSQL |
| **Task Queue** | Celery + Redis |
| **Containerization** | Docker + Docker Compose |

---

## Architecture

The backend follows a **Layered Architecture** pattern (img here !)

---

## Features

- **Inventory Management** — Track raw material entries, adjustments, and real-time stock levels
- **Bill of Materials (BOM)** — Define production recipes with required materials and quantities
- **Production Orders** — Create, validate, and execute production orders
- **Feasibility Validation** — Verify material availability before production execution
- **Low-Stock Alerts** — Automatic notifications when inventory falls below thresholds
- **User Management** — Role-based access control (Plant Manager, Supervisor, Clerk, Operator)

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/InvenGuardCO.git

cd InvenGuardCO

# Start with Docker Compose
docker compose -f docker/docker-compose.yml --env-file .env up -d

# Access the application
# http://localhost:8000
```

### Local Development

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start the application
uvicorn src.app.main:app --reload
```

## Project Structure

```
InvenGuardCO/
├── app/
│   ├── core/ # Configuration, security, and dependencies
│   ├── models/ # SQLModel models (ORM layer)
│   ├── db/ # Database session and initialization
│   ├── schemas/ # Pydantic models (DTOs)
│   ├── repositories/ # Data access layer
│   ├── services/ # Business logic layer
│   ├── templates/ # Jinja2 templates for SSR
│   ├── static/ # Static files (CSS, JS, images)
│   ├── docker/ # Dockerfile for fastapi app
│   ├── web/ # FastAPI routers (controllers)
│   └── main.py # FastAPI application entry point
├── tests/ # Unit and integration tests
├── docs/ # Project documentation
├── docker/ # Docker Compose files
├── requirements.txt # Python dependencies
└── README.md
```

## Documentation

| Document | Description |
|----------|-------------|
| [Analysis](docs/analysis.md) | Project context, problem statement, proposed solution, actors, and diagrams |
| [Requirements](docs/requirements.md) | Functional and non-functional requirements specification |

## Roadmap

User stories plan : 

- [✓] US-00 : User Authentication (Login/Logout)
- [✓] US-01 : Manage Users 
- [] US-02 : Record Material Entry
- [] US-03 : Adjust Inventory
- [] US-04 : Configure Alert Thresholds
- [] US-05 : Manage Bill of Materials (BOM)
- [] US-06 : Create Production Order
- [] US-07 : Execute Production Order
- [] US-08 : Monitor Production Progress
- [] US-09 : View Company Reports

<div align="center">

**InvenGuardCO** — Built with FastAPI and HTMX
</div>
