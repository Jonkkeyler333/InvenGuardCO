<div align="center">

# InvenGuardCO

*Inventory Management System for Manufacturing Environments*

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-SSR-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)

</div>


## About

**InvenGuardCO** is a web-based inventory management system designed for manufacturing environments. It enables real-time tracking of raw materials, production feasibility validation, and low-stock alerts to support operational decision-making.

> [!NOTE]
> This is a personal project that models a fictional but realistic industrial scenario inspired by common challenges in manufacturing environments.

For detailed analysis and requirements, see the [Documentation](#documentation) section.

---

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
docker compose up -d

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

# Run database migrations
alembic upgrade head

# Start the application
uvicorn src.app.main:app --reload
```


## Project Structure

```
InvenGuardCO/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── templates/
│   ├── static/
│   └── main.py
├── tests/
├── docs/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Documentation

| Document | Description |
|----------|-------------|
| [Analysis](docs/analysis.md) | Project context, problem statement, proposed solution, actors, and diagrams |
| [Requirements](docs/requirements.md) | Functional and non-functional requirements specification |

## Roadmap

- [ ] Project setup and Docker configuration
- [ ] Database schema and migrations
- [ ] User authentication and authorization
- [ ] Inventory management module
- [ ] BOM management module
- [ ] Production orders module
- [ ] Low-stock alerts (Celery tasks)
- [ ] Reporting dashboard

<div align="center">

**InvenGuardCO** — Built with FastAPI and HTMX

</div>
