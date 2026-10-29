# Enterprise FastAPI Backend - Production Starter

A modern, production-grade **FastAPI** backend engineered on **Python 3.12+**. Built with Clean Layered Architecture (N-Tier), Pydantic v2 fail-fast settings validation, zero-downtime environment swapping between Development and Production, distributed tracing, structured logging, async SQLAlchemy 2.0 database pooling, and comprehensive automated test suites.

---

## 🏛️ Project Architecture & Layout

```
Enterprise FastAPI Backend/
├── .env.dev                  # 🛠️ Development environment variables (SQLite, debug mode)
├── .env.prod                 # 🚀 Production environment variables (PostgreSQL, strict CORS)
├── .env.example              # 📋 Reference environment configuration template
├── .gitignore                # 🔒 Git exclusions (caches, DB files, local overrides)
├── requirements.txt          # 📦 Production and development dependencies
├── pyproject.toml            # ⚙️ Python 3.12+ project configuration, Ruff linter & pytest
├── Dockerfile                # 🐳 Multi-stage production container build (Python 3.12-slim)
├── docker-compose.yml        # 🚢 Dev & Prod container profiles
├── run.py                    # ⚡ Enterprise CLI server runner (Python 3.12+)
│
├── app/                      # 🧱 Core Application Package
│   ├── __init__.py
│   ├── main.py               # 🚀 Application factory, CORS, middlewares & lifespan
│   │
│   ├── core/                 # ⚙️ Core System Services
│   │   ├── __init__.py
│   │   ├── environment.py    # 🔄 [SWAP FILE] Active environment switcher & resolver
│   │   ├── config.py         # 🛡️ Pydantic v2 BaseSettings loading from .env.dev / .env.prod
│   │   ├── logging.py        # 📊 Structured logging & enterprise startup banner
│   │   ├── security.py       # 🔐 Security utilities, API key verification & token masking
│   │   └── exceptions.py     # 🚨 Enterprise RFC 7807 exception hierarchy & global handlers
│   │
│   ├── db/                   # 🗄️ Database & Connection Pooling
│   │   ├── __init__.py
│   │   ├── base.py           # 🏛️ Modern SQLAlchemy 2.0 DeclarativeBase & TimestampMixin
│   │   └── session.py        # 🔌 Async engine pooling, ping checks & session dependencies
│   │
│   ├── middlewares/          # 🌐 HTTP Middlewares
│   │   ├── __init__.py
│   │   ├── request_id.py     # 🆔 Distributed tracing (X-Request-ID)
│   │   └── process_time.py   # ⏱️ Execution latency benchmark (X-Process-Time-Ms)
│   │
│   ├── schemas/              # 📐 Pydantic Data Contracts & Schemas
│   │   ├── __init__.py
│   │   ├── base.py           # 📦 StandardResponse[DataT], ErrorDetail, PaginatedResponse
│   │   ├── health.py         # 💓 HealthResponse & ReadinessResponse
│   │   ├── system.py         # 🔍 SystemConfigResponse & EnvSwitchResponse
│   │   ├── auth.py           # 🔑 LoginRequest, TokenResponse, TokenPayload
│   │   └── user.py           # 👤 UserBase, UserCreate, UserUpdate, UserResponse
│   │
│   ├── repositories/         # 💾 Data Access & Repository Pattern
│   │   ├── __init__.py
│   │   ├── base.py           # 🧬 Generic Async BaseRepository (CRUD operations)
│   │   └── user_repository.py# 👤 UserRepository
│   │
│   ├── api/                  # 🔌 API Presentation Layer
│   │   ├── __init__.py
│   │   ├── deps.py           # 💉 Dependency injection providers & type aliases
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py     # 🚏 API v1 router aggregator
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── health.py # 🩺 /health/live, /health/ready
│   │           └── system.py # ⚙️ /system/config, /system/env-switch
│   │
│   ├── services/             # 🧠 Domain Business Logic Layer
│   │   └── __init__.py
│   │
│   └── models/               # 🗄️ Database ORM Entities
│       ├── __init__.py
│       └── user.py           # 👤 SQLAlchemy User Model
│
├── tests/                    # 🧪 Enterprise Automated Test Suite
│   ├── __init__.py
│   ├── conftest.py           # 🧪 Shared fixtures, TestClient & clean state reset
│   ├── test_env_swap.py      # 🧪 Dev <-> Prod environment swapping tests
│   └── test_api.py           # 🧪 API endpoint integration tests
│
└── docs/                     # 📚 Platform Architecture & Engineering Guides
    ├── v1.md                 # 📘 Architecture & file rationale blueprint
    └── production_enterprise_guide.md # 📕 Production engineering handbook & checklists
```

---

## 🔄 How to Swap Variables (Dev vs Prod)

The backend provides **four flexible ways** to swap between development (`.env.dev`) and production (`.env.prod`) configurations:

### Method 1: The Swapper File (Primary Code Toggle)
Open **`app/core/environment.py`** and modify the designated constant:

```python
# app/core/environment.py

# To use Development variables (.env.dev):
ACTIVE_ENVIRONMENT = EnvironmentType.DEV

# To use Production variables (.env.prod):
ACTIVE_ENVIRONMENT = EnvironmentType.PROD
```

### Method 2: Enterprise CLI Runner Flags
Use the included `run.py` launcher to explicitly select the target environment on launch:

```bash
# Run with DEV variables (.env.dev) and auto-reload:
python run.py --env dev --reload

# Run with PROD variables (.env.prod):
python run.py --env prod
```

### Method 3: System Environment Variable (`APP_ENV`)
Set `APP_ENV` in your shell, Docker container, or CI/CD deployment pipeline:

```bash
# Windows PowerShell
$env:APP_ENV="prod"
python run.py

# Linux / MacOS
export APP_ENV=prod
python run.py
```

### Method 4: Runtime Dynamic Swap via API
Without restarting the server or container:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/system/env-switch \
     -H "Content-Type: application/json" \
     -d '{"environment": "prod"}'
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Backend
```bash
python run.py
```
* **Interactive Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Specification**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 3. Check Liveness & Readiness
```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

### 4. Inspect Active Configuration & Loaded File
```bash
curl http://127.0.0.1:8000/api/v1/system/config
```
Returns active environment variables with passwords, secret keys, and tokens masked.

---

## 🧪 Running Automated Tests

Run the complete test suite:

```bash
pytest
```

---

## 🐳 Docker Deployment

### Run Development Container
```bash
docker compose --profile dev up --build
```

### Run Production Container
```bash
docker compose --profile prod up --build
```

---

## 📚 Platform Documentation & Architecture Guides

Comprehensive architectural blueprints and engineering guides are located in the [`docs/`](file:///c:/Users/Harsh/HiHarsh/Coding/Python/Multi%20agent%20Business%20Operations%20Platform/docs) directory:

1. **[Enterprise Architecture vs. Single-File Scripts](file:///c:/Users/Harsh/HiHarsh/Coding/Python/Multi%20agent%20Business%20Operations%20Platform/docs/enterprise_architecture_vs_script.md)**: Detailed breakdown of the top 10 deployment issues encountered when scaling an enterprise app versus naive scripts, and how this architecture intelligently solves each.
2. **[Enterprise Architecture & System Blueprint (v1)](file:///c:/Users/Harsh/HiHarsh/Coding/Python/Multi%20agent%20Business%20Operations%20Platform/docs/v1.md)**: Exhaustive directory and file manifest, dataflow boundaries, and technical justifications.
3. **[Enterprise Python Production Engineering Handbook](file:///c:/Users/Harsh/HiHarsh/Coding/Python/Multi%20agent%20Business%20Operations%20Platform/docs/production_enterprise_guide.md)**: Deep dive into async event-loop safety, database connection pooling, circuit breakers, security threat models, and a 25-point production readiness checklist.
