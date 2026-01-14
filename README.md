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

| Layer | Technology | Logo |
|-------|------------|------|
| **Frontend** | HTMX + Jinja2 Templates (SSR) | <img src="https://img.shields.io/badge/HTMX-339AF0?logo=htmx&logoColor=white" height="20"> <img src="https://img.shields.io/badge/Jinja2-B41717?logo=jinja&logoColor=white" height="20"> |
| **Styling** | Pico CSS | <img src="https://img.shields.io/badge/Pico%20CSS-222?logo=pico&logoColor=white" height="20"> |
| **Backend** | FastAPI | <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" height="20"> |
| **ORM** | SQLAlchemy + SQLModel | <img src="https://img.shields.io/badge/SQLAlchemy-d71f00?logo=sqlalchemy&logoColor=white" height="20"> <img src="https://img.shields.io/badge/SQLModel-222?logo=python&logoColor=white" height="20"> |
| **Database** | PostgreSQL | <img src="https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white" height="20"> |
| **Task Queue** | Celery + Redis | <img src="https://img.shields.io/badge/Celery-37814A?logo=celery&logoColor=white" height="20"> <img src="https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white" height="20"> |
| **Containerization** | Docker + Docker Compose | <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" height="20"> <img src="https://img.shields.io/badge/Docker%20Compose-2496ED?logo=docker&logoColor=white" height="20"> |

---

## Architecture

The backend follows a **Layered Architecture** pattern
(soon more datails !!!)

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
git clone https://github.com/Jonkkeyler333/InvenGuardCO

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

<details>
<summary><b>Project Structure 🌳</b></summary>

<pre>
<img src="https://img.shields.io/badge/InvenGuardCO-222?logo=github&logoColor=white" height="20">/
├── <img src="https://img.shields.io/badge/app-222?logo=fastapi&logoColor=white" height="20">/
│   ├── <img src="https://img.shields.io/badge/core-222?logo=lock&logoColor=white" height="20">         # Config, security, dependencies
│   ├── <img src="https://img.shields.io/badge/models-222?logo=python&logoColor=white" height="20">       # SQLModel models (ORM)
│   ├── <img src="https://img.shields.io/badge/db-222?logo=postgresql&logoColor=white" height="20">           # DB session/init
│   ├── <img src="https://img.shields.io/badge/schemas-222?logo=pydantic&logoColor=white" height="20">      # Pydantic DTOs
│   ├── <img src="https://img.shields.io/badge/repositories-222?logo=database&logoColor=white" height="20"> # Data access
│   ├── <img src="https://img.shields.io/badge/services-222?logo=gear&logoColor=white" height="20">     # Business logic
│   ├── <img src="https://img.shields.io/badge/templates-222?logo=jinja&logoColor=white" height="20">    # Jinja2 SSR
│   ├── <img src="https://img.shields.io/badge/static-222?logo=css3&logoColor=white" height="20">       # CSS, JS, images
│   ├── <img src="https://img.shields.io/badge/docker-222?logo=docker&logoColor=white" height="20">       # FastAPI Dockerfile
│   ├── <img src="https://img.shields.io/badge/web-222?logo=fastapi&logoColor=white" height="20">          # FastAPI routers
│   └── <img src="https://img.shields.io/badge/main.py-222?logo=python&logoColor=white" height="20">       # App entrypoint
├── <img src="https://img.shields.io/badge/tests-222?logo=pytest&logoColor=white" height="20">            # Unit/integration tests
├── <img src="https://img.shields.io/badge/docs-222?logo=markdown&logoColor=white" height="20">             # Documentation
├── <img src="https://img.shields.io/badge/docker-222?logo=docker&logoColor=white" height="20">           # Docker Compose
├── <img src="https://img.shields.io/badge/requirements.txt-222?logo=pypi&logoColor=white" height="20">  # Python dependencies
└── <img src="https://img.shields.io/badge/README.md-222?logo=markdown&logoColor=white" height="20">
</pre>
</details>

## Documentation

| Document | Description |
|----------|-------------|
| [Analysis](docs/analysis.md) | Project context, problem statement, proposed solution, actors, and diagrams |
| [Requirements](docs/requirements.md) | Functional and non-functional requirements specification |

## Roadmap

User stories plan : 

- [✓] US-00 : User Authentication (Login/Logout)
- [✓] US-01 : Manage Users 
- […] US-02 : Record Material Entry
- […] US-03 : Adjust Inventory
- […] US-04 : Configure Alert Thresholds
- […] US-05 : Manage Bill of Materials (BOM)
- […] US-06 : Create Production Order
- […] US-07 : Execute Production Order
- […] US-08 : Monitor Production Progress
- […] US-09 : View Company Reports

<div align="center">

**InvenGuardCO** — Built with FastAPI and HTMX
</div>
