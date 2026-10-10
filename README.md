# Dual-Client POS System

A production-oriented Point of Sale (POS) system built around a **single FastAPI backend**, **PostgreSQL database**, **PyQt6 desktop client**, and **responsive Web POS**.

The system is designed to support multiple POS clients while keeping authentication, business rules, pricing, inventory, checkout, and transaction integrity centralized in the backend.

It also supports using a **smartphone as a companion barcode scanner** for the Web POS, alongside traditional USB/Bluetooth barcode scanners and manual barcode entry.

---

## ✨ Key Features

### 🖥️ Dual POS Clients

* **PyQt6 Desktop POS**
* **Responsive Web POS**
* Both clients use the same FastAPI backend
* No client directly accesses the database
* Consistent business rules across both clients

### 📱 Multiple Barcode Scanning Methods

The POS supports three barcode input methods:

1. **USB/Bluetooth Barcode Scanner**
2. **Smartphone Camera Scanner**
3. **Manual Barcode Entry**

The scanner source can be selected directly from the POS.

### 📲 Smartphone Barcode Scanner

A smartphone can be paired with the Web POS using a temporary QR-based scanner session.

```text
Web POS
   ↓
Generate Scanner Session
   ↓
Display QR Code
   ↓
Phone Scans QR
   ↓
Phone Camera Scans Barcode
   ↓
FastAPI
   ↓
Web POS
   ↓
Cart
```

The smartphone acts only as a barcode scanner. It does not access PostgreSQL or perform sales calculations.

### 👨‍💼 Cashier / Self-Service Scanner Modes

When using the smartphone scanner, the POS can select between:

#### Cashier Present

* Phone remains paired after a completed sale
* Multiple transactions can be processed
* Cart resets after each sale
* Scanner remains ready for the next transaction

#### No Cashier / Self-Service

* Scanner session is intended for one transaction
* After a successful sale, the scanner session is revoked
* The phone cannot continue submitting barcodes
* A new transaction requires a new pairing

Scanner sessions are temporary, scoped, revocable, and isolated between POS sessions.

---

## 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │   PostgreSQL    │
                         └────────▲────────┘
                                  │
                         ┌────────┴────────┐
                         │     FastAPI     │
                         │                 │
                         │ Authentication  │
                         │ Authorization   │
                         │ Products        │
                         │ Inventory       │
                         │ Pricing         │
                         │ Payments        │
                         │ Sales           │
                         │ Reports         │
                         │ Scanner         │
                         └────▲───────▲────┘
                              │       │
                   ┌──────────┘       └──────────┐
                   │                             │
            ┌──────┴──────┐              ┌──────┴──────┐
            │  PyQt6 POS  │              │   Web POS   │
            └─────────────┘              └──────▲──────┘
                                               │
                                         ┌─────┴─────┐
                                         │ Smartphone │
                                         │  Scanner   │
                                         └────────────┘
```

### Core Principle

> **FastAPI is the single source of truth.**

Only the FastAPI backend communicates directly with PostgreSQL.

The clients are responsible primarily for:

* UI
* user interaction
* scanner input
* cart presentation
* displaying API responses
* receipt presentation

The backend is responsible for:

* authentication
* authorization
* pricing
* discounts
* tax
* payment validation
* inventory validation
* inventory deduction
* sale creation
* idempotency
* concurrency control
* reports
* audit logging
* scanner-session security

---

## 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy 2.x
* PostgreSQL
* Alembic
* JWT / secure session authentication
* Argon2 or bcrypt

### Desktop

* Python
* PyQt6

### Web

* Modern component-based frontend
* Responsive UI
* REST API integration
* WebSocket support where appropriate

### Mobile Scanner

* Mobile browser
* Device camera
* Browser-compatible barcode scanning APIs
* QR-based pairing

---

## 🔐 Authentication & Authorization

The system uses role-based access control.

### ADMIN

Administrators can manage:

* Products
* Inventory
* Users
* Reports
* Configuration
* Audit logs

### CASHIER

Cashiers can:

* Access the POS
* Search products
* Scan products
* Manage carts
* Process sales
* View permitted sales information

All authorization decisions are enforced by FastAPI.

Frontend role checks are used only for UI behavior and are **not considered security controls**.

---

## 🛒 POS Checkout Flow

Both the PyQt6 and Web POS use the same backend checkout process:

```text
Login
  ↓
Scan / Search Product
  ↓
Cart
  ↓
Discount
  ↓
Tax
  ↓
Payment
  ↓
Backend Validation
  ↓
Atomic Transaction
  ↓
Inventory Deduction
  ↓
Sale Creation
  ↓
Receipt
  ↓
Cart Reset
```

The backend recalculates:

* Subtotal
* Discount
* Tax
* Grand total
* Payment status
* Change

Client-provided totals are never treated as authoritative.

---

## 📦 Inventory Management

The inventory system is designed around transactional consistency.

It supports:

* Stock tracking
* Low-stock thresholds
* Stock adjustments
* Restocking
* Returns
* Corrections
* Inventory audit history

Inventory transactions can be associated with:

* Sales
* Restocks
* Manual adjustments
* Returns
* Corrections

### Concurrency Protection

The system is designed to prevent situations such as:

```text
Stock = 1

POS A → attempts to sell 1
POS B → attempts to sell 1
```

The backend uses PostgreSQL transactions and appropriate concurrency-control mechanisms so inventory cannot incorrectly become negative.

---

## 💳 Payments

The checkout system is designed to support payment methods such as:

* Cash
* Card
* UPI
* Other configured payment methods

For cash payments:

```text
Amount Due
Amount Received
Change
```

Payment validation is performed by FastAPI.

---

## 🧾 Historical Sales

Completed sales preserve historical product information.

Sale items can retain snapshots such as:

* Product name
* SKU
* Barcode
* Unit price
* Tax rate
* Quantity
* Discount

This ensures an old receipt remains accurate even if the product's current information changes later.

---

## 🔁 Duplicate Transaction Protection

The checkout system is designed to protect against duplicate sales caused by:

* Double-clicking the payment button
* Network retries
* API retries
* Frontend retries
* Mobile connection problems

Idempotency mechanisms are used so the same transaction cannot accidentally create multiple completed sales.

---

## 📊 Reports

The planned reporting system includes:

* Daily sales
* Weekly sales
* Monthly sales
* Transaction count
* Revenue
* Tax collected
* Discount totals
* Payment-method breakdown
* Top-selling products
* Low-stock products

Reports are generated from authoritative PostgreSQL data.

---

## 🗄️ Database Design

The system uses PostgreSQL as its primary database.

Core entities include:

```text
Users
Categories
Products
Inventory
Inventory Transactions

Sales
Sale Items
Payments

Scanner Sessions

Discounts
Tax Rules
Audit Logs
```

Database integrity is supported through:

* Foreign keys
* Unique constraints
* Check constraints
* Indexes
* Transactions
* Row-level locking where required
* Alembic migrations

---

## 📱 Scanner Session Security

Mobile scanner sessions are designed to be:

* Temporary
* Unpredictable
* Scoped to a POS session
* Revocable
* Expirable
* Protected against replay
* Isolated between POS terminals

For example:

```text
POS A
  └── Phone A
       └── Scanner Session A
```

Phone A cannot submit scans to POS B.

The smartphone never receives permissions to:

* Modify inventory
* Create arbitrary sales
* Access PostgreSQL
* Access administrative functionality

---

## 🧪 Testing

The project aims to include automated tests for:

### Authentication

* Login
* Invalid credentials
* Session expiry
* Authorization
* RBAC

### Products

* Product creation
* Barcode lookup
* Duplicate barcode protection
* Inactive products

### Inventory

* Stock validation
* Insufficient stock
* Concurrent sales
* Inventory transactions
* Negative-stock prevention

### Sales

* Successful checkout
* Duplicate requests
* Payment validation
* Inventory deduction
* Historical snapshots
* Transaction rollback

### Mobile Scanner

* Session creation
* QR pairing
* Invalid pairing
* Session expiration
* Session revocation
* Cashier-present reuse
* Self-service single-use behavior
* Session isolation
* Barcode submission

---

## 📁 Planned Project Structure

```text
project/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── models/
│   │   │
│   │   ├── schemas/
│   │   ├── api/
│   │   ├── services/
│   │   ├── security/
│   │   └── tests/
│   │
│   ├── alembic/
│   ├── alembic.ini
│   └── requirements.txt
│
├── desktop/
│   ├── app/
│   │   ├── api_client/
│   │   ├── ui/
│   │   └── services/
│   └── tests/
│
├── web/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── tests/
│
├── mobile-scanner/
│   └── src/
│
└── README.md
```

---

## 🚧 Development Status

This project is being developed incrementally.

### Work Completed So Far

The backend foundation has now been started under `backend/app/`:

* Added a FastAPI application entry point with a `/health` endpoint.
* Added environment-based settings using `pydantic-settings`.
* Added SQLAlchemy 2.x database base and PostgreSQL session setup.
* Added initial models for users, categories, products, inventory, sales, payments, scanner sessions, and audit logs.
* Added initial Pydantic schemas for authentication, products, users, and checkout requests.
* Added the backend dependency list in `backend/requirements.txt`.
* Added `backend/.env.example` for local configuration.
* Added temporary development scripts to create the database tables and an initial admin user.
* Added password hashing with Argon2 through `pwdlib`.
* Added JWT access-token creation and validation.
* Added authentication dependencies for loading the current user and enforcing roles.
* Added authentication and administration routers.
* Added the login endpoint at `POST /api/auth/login`.
* Added the protected admin profile endpoint at `GET /api/admin/profile`.
* Added product management endpoints for creation, listing, search, barcode lookup, updates, and deactivation.
* Added category management endpoints for creation, listing, lookup, updates, and deletion.
* Added Alembic configuration and an initial schema migration.
* Stamped the existing development database at revision `b4e5b39cfe88`.
* Verified health checks, login, JWT authentication, admin authorization, product APIs, and category APIs with Postman.

The models, schemas, authentication layer, initial migration, product management API, and category management API are complete foundation modules. Inventory APIs, business services, and automated tests are still pending.

### Current Prototype

The original repository contains early experiments for:

* Product creation
* Barcode lookup
* Basic sales
* Stock updates
* Camera-based barcode scanning

The original prototype used MongoDB and direct database access.

### Target Architecture

The project is being migrated toward:

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* PyQt6 POS
* Web POS
* Secure mobile scanner sessions
* Authentication
* RBAC
* Transaction-safe checkout
* Automated testing

The existing repository should therefore be considered a **prototype starting point rather than a production-ready POS**. The current repository still requires inventory APIs, atomic checkout, client applications, and automated tests.

---

## 🗺️ Roadmap

### Phase 1 — Backend Foundation

* [x] FastAPI setup
* [x] PostgreSQL setup
* [x] SQLAlchemy models
* [x] Alembic migrations
* [x] Authentication
* [x] RBAC
* [ ] Error handling
* [ ] Logging

### Phase 2 — POS Core

* [x] Product management
* [x] Category management
* [ ] Inventory management
* [x] Barcode lookup
* [ ] Pricing service
* [ ] Tax service
* [ ] Discount service
* [ ] Payment service
* [ ] Atomic checkout
* [ ] Idempotency
* [ ] Inventory audit trail

### Current Backend Verification

The following checks have passed against the development environment:

```bash
cd backend
python -m compileall -q app alembic
alembic current
alembic upgrade head
alembic check
```

The current database revision is:

```text
b4e5b39cfe88 (head)
```

The authentication flow has also been verified:

* `GET /health` returns `200 OK`.
* `POST /api/auth/login` returns a JWT for a valid admin user.
* `GET /api/admin/profile` returns `401 Unauthorized` without a token.
* `GET /api/admin/profile` returns `200 OK` with a valid admin token.

Product APIs have been verified with Postman:

* `POST /api/products` creates a product for an admin user.
* `GET /api/products` lists active products.
* `GET /api/products?search=<term>` searches by name, SKU, or barcode.
* `GET /api/products/{product_id}` returns an active product.
* `GET /api/products/barcode/{barcode}` performs barcode lookup.
* `PATCH /api/products/{product_id}` updates product details.
* `DELETE /api/products/{product_id}` deactivates a product.
* Product creation requires authentication and admin authorization.
* Duplicate SKU or barcode values return `409 Conflict`.

Category APIs have been verified with Postman:

* `POST /api/categories` creates a category for an admin user.
* `GET /api/categories` lists categories.
* `GET /api/categories/{category_id}` returns a category.
* `PATCH /api/categories/{category_id}` updates a category.
* `DELETE /api/categories/{category_id}` removes a category.
* Duplicate category names return `409 Conflict`.
* Category creation requires authentication and admin authorization.
* Products assigned to a deleted category remain available with a null category reference.

The category list endpoint uses SQLAlchemy's collection result method:

```python
db.scalars(statement).all()
```

This is required when retrieving multiple category records.

### Phase 3 — PyQt6 POS

* [ ] Login
* [ ] Dashboard
* [ ] Product search
* [ ] Barcode machine
* [ ] Manual barcode entry
* [ ] Cart
* [ ] Checkout
* [ ] Receipt
* [ ] Sales history

### Phase 4 — Web POS

* [ ] Login
* [ ] POS dashboard
* [ ] Product search
* [ ] Barcode machine support
* [ ] Manual barcode entry
* [ ] Cart
* [ ] Checkout
* [ ] Sales history
* [ ] Inventory
* [ ] Reports

### Phase 5 — Mobile Scanner

* [ ] Scanner sessions
* [ ] QR pairing
* [ ] Camera scanning
* [ ] WebSocket communication
* [ ] Cashier-present mode
* [ ] Self-service mode
* [ ] Session expiration
* [ ] Session revocation
* [ ] POS isolation

### Phase 6 — Production Hardening

* [ ] Automated tests
* [ ] Concurrency testing
* [ ] Security testing
* [ ] Rate limiting
* [ ] Secure CORS
* [ ] Health checks
* [ ] Structured logging
* [ ] Backups
* [ ] Recovery procedures
* [ ] Deployment configuration

---

## 🚀 Getting Started

> The exact commands below will be finalized as the backend, web client, and desktop client are implemented.

### Prerequisites

Install:

* Python 3.x
* PostgreSQL
* Node.js and npm/pnpm if required by the selected web stack
* Git

### Clone

```bash
git clone <repository-url>
cd <repository-directory>
```

### Backend

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Configure environment variables:

```env
APP_NAME=POS Backend
DEBUG=true
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/pos_database
SECRET_KEY=replace-this-with-a-long-random-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run migrations from the backend directory:

```bash
cd backend
alembic upgrade head
```

Start FastAPI:

```bash
python -m uvicorn app.main:app --reload
```

API documentation will be available through FastAPI's generated documentation when the backend is running.

The initial health endpoint is available at:

```text
http://127.0.0.1:8000/health
```

The current authentication checks can be tested with:

```bash
curl http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/api/admin/profile
curl -i -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
curl -i http://127.0.0.1:8000/api/admin/profile \
  -H "Authorization: Bearer $TOKEN"
```

The last request requires `TOKEN` to contain the access token returned by the login request. The protected endpoint should return `401 Not Authenticated` without a token and `200 OK` for a valid admin token.

### Product API Postman Checks

Use the bearer token returned by the login request in the Postman Authorization tab:

```text
Type: Bearer Token
Token: {{token}}
```

The product API base URL is:

```text
{{base_url}}/api/products
```

The verified product requests are:

```text
POST   {{base_url}}/api/products
GET    {{base_url}}/api/products
GET    {{base_url}}/api/products?search=milk
GET    {{base_url}}/api/products/{{product_id}}
GET    {{base_url}}/api/products/barcode/{{barcode}}
PATCH  {{base_url}}/api/products/{{product_id}}
DELETE {{base_url}}/api/products/{{product_id}}
```

Expected behavior:

* Product creation returns `201 Created`.
* Product listing and lookup return `200 OK`.
* Product deactivation returns `204 No Content`.
* Requests without a token return `401 Unauthorized`.
* Product creation by a non-admin user returns `403 Forbidden`.
* Duplicate SKU or barcode values return `409 Conflict`.

---

## 🔒 Environment Variables

Never commit secrets to Git.

Example:

```env
APP_NAME=POS Backend
DEBUG=true
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/pos_database
SECRET_KEY=replace-this-with-a-long-random-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use a `.env` file locally and keep it excluded through `.gitignore`. Do not commit database credentials.

---

## 🎯 Project Goals

The project is designed to demonstrate practical software-engineering concepts including:

* REST API architecture
* FastAPI
* PostgreSQL
* Relational database design
* SQLAlchemy
* Database migrations
* Authentication
* RBAC
* Transaction management
* Concurrency control
* Inventory consistency
* Idempotent APIs
* Desktop application development
* Responsive web development
* QR-based device pairing
* WebSockets
* Barcode scanning
* Automated testing
* Auditability

---

## 📌 Design Principles

### Single Source of Truth

All clients use the same FastAPI backend.

### Backend-First Validation

The client is never trusted for financial or inventory-critical calculations.

### Transaction Safety

Sales and inventory updates must remain consistent.

### Security by Design

Authentication, authorization, session expiry, and scanner isolation are part of the architecture.

### Reusable Business Logic

PyQt and Web POS must not implement separate versions of pricing, tax, inventory, or sales logic.

### Failure-Aware Design

The system must account for:

* Network failures
* Scanner disconnections
* Browser closure
* API timeouts
* Duplicate requests
* Concurrent sales
* Database failures

---

## 📈 Project Vision

The final goal is a POS platform where multiple clients can operate against the same reliable backend without duplicating business logic.

```text
                 ┌──────────────────┐
                 │    PostgreSQL    │
                 └────────▲─────────┘
                          │
                 ┌────────┴─────────┐
                 │      FastAPI     │
                 │   Single Truth   │
                 └────▲─────────▲───┘
                      │           │
               ┌──────┘           └──────┐
               │                         │
          ┌────┴─────┐              ┌────┴─────┐
          │  PyQt6   │              │  Web POS │
          │    POS   │              │          │
          └──────────┘              └────▲─────┘
                                        │
                                  ┌─────┴─────┐
                                  │ Smartphone│
                                  │  Scanner  │
                                  └───────────┘
```

The smartphone is a scanner, the PyQt application is a desktop POS client, the Web application is a web POS client, and **FastAPI remains the central authority for the entire system**.

---

## 📄 License

Add the project's chosen license here.

Example:

```text
MIT License
```

---

## 👨‍💻 Development

This project is under active development. Features described in the roadmap may not yet be implemented.

The README distinguishes between the **current prototype** and the **target architecture** to avoid presenting planned functionality as already implemented.
