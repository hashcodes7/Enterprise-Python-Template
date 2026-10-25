# Multi-Agent Business Operations Platform - Enterprise Backend

A production enterprise-grade **FastAPI** backend engineered for high-throughput multi-agent business operations. Built with strict layered separation of concerns, robust environment isolation, distributed tracing, and zero-downtime environment swapping.

---

## 🏛️ Enterprise Project Architecture

```
Multi agent Business Operations Platform/
├── .env.dev                  # 🛠️ Development environment variables
├── .env.prod                 # 🚀 Production environment variables
├── .env.example              # 📋 Reference environment configuration template
├── .gitignore                # 🔒 Enterprise git exclusions
├── requirements.txt          # 📦 Production and development dependencies
├── pyproject.toml            # ⚙️ Project configuration, linter & test settings
├── Dockerfile                # 🐳 Multi-stage production container build
├── docker-compose.yml        # 🚢 Dev & Prod container profiles
├── run.py                    # ⚡ Enterprise CLI server runner
│
├── app/                      # 🧱 Core Application Package
│   ├── __init__.py
│   ├── main.py               # 🚀 Application factory, CORS, middlewares & lifespan
│   │
│   ├── core/                 # ⚙️ Core System Services
│   │   ├── __init__.py
│   │   ├── environment.py    # 🔄 [SWAP FILE] Active environment switcher & resolution
│   │   ├── config.py         # 🛡️ Pydantic BaseSettings loading from .env.dev / .env.prod
│   │   ├── logging.py        # 📊 Structured logging & enterprise startup banner
│   │   ├── security.py       # 🔐 Security utilities & token masking
│   │   └── exceptions.py     # 🚨 Enterprise RFC 7807 exception hierarchy & handlers
│   │
│   ├── middlewares/          # 🌐 HTTP Middlewares
│   │   ├── __init__.py
│   │   ├── request_id.py     # 🆔 Distributed tracing (X-Request-ID)
│   │   └── process_time.py   # ⏱️ Execution latency benchmark (X-Process-Time-Ms)
│   │
│   ├── schemas/              # 📐 Pydantic Data Contracts & Schemas
│   │   ├── __init__.py
│   │   ├── base.py           # 📦 StandardResponse[T], ErrorDetail, Pagination
│   │   ├── health.py         # 💓 HealthResponse & ReadinessResponse
│   │   └── system.py         # 🔍 SystemConfigResponse & EnvSwitchResponse
│   │
│   ├── api/                  # 🔌 API Presentation Layer
│   │   ├── __init__.py
│   │   ├── deps.py           # 💉 Dependency injection providers
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py     # 🚏 API v1 router aggregator
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── health.py # 🩺 /health/live, /health/ready
│   │           └── system.py # ⚙️ /system/config, /system/env-switch
│   │
│   ├── services/             # 🧠 Business Logic & Multi-Agent Operations
│   │   └── __init__.py
│   │
│   └── models/               # 🗄️ Database & Domain Entity Models
│       └── __init__.py
│
└── tests/                    # 🧪 Enterprise Automated Test Suite
    ├── __init__.py
    ├── conftest.py           # 🧪 Shared fixtures & TestClient setup
    ├── test_env_swap.py      # 🧪 Dev <-> Prod environment swapping tests
    └── test_api.py           # 🧪 API endpoint integration tests
```

---

## 🔄 How to Swap Variables (Dev vs Prod)

The platform provides **three seamless ways** to swap between development (`.env.dev`) and production (`.env.prod`) variables:

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

### 1. Run the Backend
```bash
python run.py
```
* Interactive Swagger Docs: **http://127.0.0.1:8000/docs**
* ReDoc Specification: **http://127.0.0.1:8000/redoc**

### 2. Inspect Active Configuration & Loaded File
```bash
curl http://127.0.0.1:8000/api/v1/system/config
```
This returns the active environment variables with all credentials safely masked.

### 3. Check Liveness & Health
```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

---

## 🧪 Running Automated Tests

Run the complete test suite to verify configuration loading and variable swapping:

```bash
pytest
```
