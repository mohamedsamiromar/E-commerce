# Django E-Commerce API

A production-ready REST API for an e-commerce platform built with **Django 4.2** and **Django REST Framework**. The project follows a modular multi-app architecture — each domain is a self-contained Django app with its own models, serializers, services, views, and tests.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Docker (Recommended)](#docker-recommended)
  - [Local Setup](#local-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
  - [Authentication](#authentication)
  - [Catalog](#catalog)
  - [Cart & Orders](#cart--orders)
  - [Payments](#payments)
  - [Coupons](#coupons)
  - [Addresses](#addresses)
  - [Merchant Dashboard](#merchant-dashboard)
- [Payment Integration](#payment-integration)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)

---

## Features

- **Product Catalog** — Browse, search, filter by price / category / discount, paginate
- **Shopping Cart** — Add/remove items, quantity management, persistent per-user cart
- **Order Lifecycle** — Tracks ordered → being delivered → received → refund states
- **Coupon System** — Discount codes with expiry dates and active/inactive toggle
- **Multi-Gateway Payments** — Stripe, PayPal, Apple Pay, Google Pay via a gateway factory pattern
- **Address Management** — Multiple shipping/billing addresses per user
- **Merchant Dashboard** — Approved merchants manage their own products, orders, coupons, and analytics via isolated APIs
- **Token Authentication** — DRF token auth + django-allauth session auth
- **Dockerised** — Runs with a single `docker compose up`
- **CI/CD** — GitHub Actions pipeline with a real PostgreSQL service

---

## Architecture

The codebase is split into six focused Django apps. Each app owns its domain end-to-end.

```text
catalog/    →  Category, Item                                  (product catalogue)
accounts/   →  UserProfile, Address                            (users & addresses)
coupons/    →  Coupon, CouponService                           (discount codes)
payments/   →  Payment, PaymentService, gateways               (payment processing)
orders/     →  OrderItem, Order, CartService                   (cart & order lifecycle)
merchants/  →  MerchantProfile, MerchantOrderFulfillment       (merchant dashboard)
```

**Dependency flow** (no circular imports):

```text
catalog   ──────────────────────────────────────┐
accounts  ──────────────────────────────────────┤
payments  ──────────────────────────────────────┼──▶  orders
coupons   ──────────────────────────────────────┘
                                                 ▲
catalog / coupons / orders ─────────────────────▶  merchants
```

`orders` models reference the other four apps via Django string labels (`'catalog.Item'`, `'accounts.Address'`, etc.) — no Python-level circular imports. `merchants` similarly references `catalog`, `coupons`, and `orders` by string label.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Framework | Django 4.2, Django REST Framework 3.14 |
| Database | PostgreSQL 13 |
| Payments | Stripe SDK, PayPal REST SDK |
| Auth | DRF Token Auth, django-allauth |
| Filtering | django-filter |
| CORS | django-cors-headers |
| Static files | Whitenoise |
| Container | Docker, Docker Compose |
| Server | Gunicorn |
| CI | GitHub Actions |

---

## Getting Started

### Docker (Recommended)

**Requirements:** Docker Desktop

```bash
# 1. Clone
git clone https://github.com/mohamedsamiromar/E-commerce.git
cd E-commerce

# 2. Configure environment
cp .env.example .env
# Open .env and fill in STRIPE_SECRET_KEY, PAYPAL_CLIENT_ID, etc.

# 3. Start
docker compose up --build
```

The API will be available at `http://localhost:8000`.

On first run the container automatically:

1. Runs all database migrations
2. Collects static files
3. Starts Gunicorn with 2 workers

### Local Setup

**Requirements:** Python 3.10+, PostgreSQL

```bash
# 1. Clone & create virtual environment
git clone https://github.com/mohamedsamiromar/E-commerce.git
cd E-commerce
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env — set DB_* and payment keys

# 4. Migrate & run
make migrate
make run
```

Common `make` commands:

| Command | Description |
|---|---|
| `make install` | Install Python dependencies |
| `make migrate` | Apply database migrations |
| `make run` | Start development server |
| `make test` | Run test suite |
| `make shell` | Open Django shell |
| `make superuser` | Create admin superuser |

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (PostgreSQL)
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost          # use "db" inside Docker
DB_PORT=5432

# Stripe
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# PayPal
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
PAYPAL_MODE=sandbox        # "live" for production

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## API Reference

### Authentication

All endpoints except `GET /api/catalog/items/` require a token in the `Authorization` header:

```http
Authorization: Token <your-token>
```

**Obtain a token:**

```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "john",
  "password": "secret"
}
```

Response:
```json
{ "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" }
```

---

### Catalog

#### List / Create Products

```http
GET  /api/catalog/items/
POST /api/catalog/items/
Authorization: Token <token>
```

**Query parameters (GET):**

| Parameter | Type | Description |
|---|---|---|
| `min_price` | number | Minimum price |
| `max_price` | number | Maximum price |
| `has_discount` | boolean | Only discounted items |
| `category` | string | Filter by category slug |
| `search` | string | Search title and description |
| `ordering` | string | `price`, `-price`, `title`, `id` |
| `limit` / `offset` | number | Pagination |

**Example response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "title": "Wireless Headphones",
      "price": 99.99,
      "discount_price": 79.99,
      "final_price": 79.99,
      "has_discount": true,
      "slug": "wireless-headphones",
      "description": "Premium noise-cancelling headphones",
      "image": null,
      "category": { "id": 1, "name": "Electronics", "slug": "electronics" },
      "in_stock": true,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

---

### Cart & Orders

#### View Cart

```http
GET /api/orders/cart/
Authorization: Token <token>
```

```json
{
  "id": 3,
  "ref_code": "A1B2C3D4E5F6",
  "order_items": [
    {
      "id": 5,
      "item": { "id": 1, "title": "Wireless Headphones", "final_price": 79.99, ... },
      "quantity": 2,
      "final_price": 159.98
    }
  ],
  "total": 149.98,
  "coupon": { "id": 1, "code": "SAVE10", "amount": 10.00 },
  "being_delivered": false,
  "received": false,
  "ordered_date": "2024-01-15T12:00:00Z"
}
```

#### Add Item to Cart

```http
POST /api/orders/cart/add/
Authorization: Token <token>
Content-Type: application/json

{ "slug": "wireless-headphones" }
```

#### Remove / Decrease Item from Cart

```http
POST /api/orders/cart/remove/
Authorization: Token <token>
Content-Type: application/json

{ "slug": "wireless-headphones" }
```

Decreases quantity by 1. Removes the item entirely when quantity reaches 0.

---

### Payments

```http
POST /api/payments/checkout/
Authorization: Token <token>
Content-Type: application/json
```

#### Stripe

```json
{
  "method": "stripe",
  "stripeToken": "tok_visa",
  "billing_address_id": 1,
  "shipping_address_id": 2
}
```

#### Apple Pay / Google Pay

```json
{
  "method": "apple_pay",
  "payment_method_id": "pm_1234567890",
  "billing_address_id": 1,
  "shipping_address_id": 2
}
```

#### PayPal

```json
{
  "method": "paypal",
  "paypal_payment_id": "PAY-XXXXXXXXXXXXXXXXXXXXXXXX",
  "payer_id": "XXXXXXXX",
  "billing_address_id": 1,
  "shipping_address_id": 2
}
```

**Success response:**
```json
{ "message": "Payment successful", "payment_id": 7 }
```

---

### Coupons

```http
POST /api/coupons/apply/
Authorization: Token <token>
Content-Type: application/json

{ "code": "SAVE10" }
```

Coupon codes are validated against `active`, `valid_from`, and `valid_to` fields. Returns `400` if expired or inactive.

---

### Addresses

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/accounts/addresses/` | List user's addresses |
| `POST` | `/api/accounts/addresses/create/` | Create an address |
| `PUT/PATCH` | `/api/accounts/addresses/<id>/update/` | Update an address |
| `DELETE` | `/api/accounts/addresses/<id>/delete/` | Delete an address |

**Query params (GET):** `?address_type=S` (Shipping) or `?address_type=B` (Billing)

**Create body:**
```json
{
  "street_address": "123 Main St",
  "apartment_address": "Apt 4B",
  "country": "US",
  "zip": "10001",
  "address_type": "S",
  "default": true
}
```

---

### Merchant Dashboard

All merchant endpoints are under `/api/merchant/` and require an approved merchant account. Every request must include an auth token. Non-merchant users receive `403 Forbidden`.

**Becoming a merchant:** A Django admin sets `is_approved = True` on the user's `MerchantProfile` via the admin panel. There is no self-approval endpoint by design.

#### Profile

```http
GET   /api/merchant/profile/
PATCH /api/merchant/profile/
Authorization: Token <token>
```

```json
{
  "id": 1,
  "store_name": "Tech Haven",
  "store_slug": "tech-haven",
  "description": "Premium electronics and gadgets.",
  "logo": null,
  "is_approved": true,
  "created_at": "2024-01-10T09:00:00Z"
}
```

#### Products

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/merchant/products/` | List own products |
| `POST` | `/api/merchant/products/` | Create a product |
| `GET` | `/api/merchant/products/<slug>/` | Retrieve a product |
| `PATCH` | `/api/merchant/products/<slug>/` | Update a product |
| `DELETE` | `/api/merchant/products/<slug>/` | Delete a product |
| `GET` | `/api/merchant/categories/` | List all categories (read-only) |

**Create / update body:**
```json
{
  "title": "Wireless Headphones Pro",
  "slug": "wireless-headphones-pro",
  "description": "40-hour battery, ANC",
  "price": 129.99,
  "discount_price": 99.99,
  "category_id": 1,
  "in_stock": true,
  "stock_qty": 50
}
```

#### Orders

Merchants see only the orders that contain at least one of their products. The response shows only their items within each order, not other merchants' items.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/merchant/orders/` | List relevant orders |
| `GET` | `/api/merchant/orders/<ref_code>/` | Order detail (merchant's items only) |
| `PATCH` | `/api/merchant/orders/<ref_code>/fulfill/` | Update fulfillment status |

**Fulfill body:**
```json
{
  "status": "shipped",
  "tracking_number": "1Z999AA10123456784"
}
```

`status` values: `pending` → `processing` → `shipped` → `delivered` → `cancelled`

**Order detail response:**
```json
{
  "id": 12,
  "ref_code": "A1B2C3D4E5F6",
  "customer": "john_doe",
  "my_items": [
    { "id": 5, "title": "Wireless Headphones Pro", "quantity": 2, "unit_price": 99.99, "final_price": 199.98 }
  ],
  "my_subtotal": 199.98,
  "fulfillment": { "status": "shipped", "tracking_number": "1Z999AA10123456784", "updated_at": "2024-01-16T08:00:00Z" },
  "ordered_date": "2024-01-15T12:00:00Z"
}
```

#### Merchant Coupons

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/merchant/coupons/` | List own coupons |
| `POST` | `/api/merchant/coupons/` | Create a coupon |
| `GET` | `/api/merchant/coupons/<id>/` | Retrieve a coupon |
| `PATCH` | `/api/merchant/coupons/<id>/` | Update a coupon |
| `DELETE` | `/api/merchant/coupons/<id>/` | Delete a coupon |

**Create body:**
```json
{
  "code": "TECHSAVE20",
  "amount": 20.00,
  "active": true,
  "valid_from": "2024-02-01T00:00:00Z",
  "valid_to": "2024-02-28T23:59:59Z"
}
```

#### Analytics

```http
GET /api/merchant/analytics/
Authorization: Token <token>
```

```json
{
  "total_revenue": 4250.00,
  "orders_count": 38,
  "pending_orders": 5,
  "products_count": 12,
  "low_stock_products": [
    { "id": 3, "title": "USB-C Hub", "slug": "usb-c-hub", "stock_qty": 2 }
  ],
  "top_products": [
    { "id": 1, "title": "Wireless Headphones Pro", "slug": "wireless-headphones-pro", "units_sold": 47 }
  ]
}
```

---

## Payment Integration

### Adding a new payment gateway

1. Create a class in [payments/gateways.py](payments/gateways.py) that extends `PaymentGateway` and implements `create_charge` and `create_customer`.
2. Register it in `PaymentGatewayFactory._registry`.
3. Add the method name to `Payment.METHOD_CHOICES` in [payments/models.py](payments/models.py).
4. Create a migration: `python manage.py makemigrations payments`.

```python
# payments/gateways.py
class CashOnDeliveryGateway(PaymentGateway):
    def create_charge(self, user, order, billing_address, shipping_address, **kwargs):
        payment = Payment.objects.create(method='cod', user=user, amount=order.get_total())
        # ... finalize order
        return payment, None

    def create_customer(self, user):
        pass

# Register it
class PaymentGatewayFactory:
    _registry = {
        ...
        'cod': CashOnDeliveryGateway,
    }
```

---

## Running Tests

```bash
# All tests
make test

# Single app
python manage.py test catalog
python manage.py test orders
python manage.py test payments
python manage.py test coupons
python manage.py test accounts
python manage.py test merchants

# With verbosity
python manage.py test --verbosity=2
```

Tests cover models, service layer logic, payment gateway behaviour (Stripe/PayPal mocked), and edge cases (empty cart, invalid coupon, unsupported gateway).

---

## Project Structure

```text
E-commerce/
├── catalog/                # Product catalogue
│   ├── models.py           #   Category, Item
│   ├── serializers.py
│   ├── filters.py          #   Price, category, discount, search filters
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
│
├── accounts/               # Users & addresses
│   ├── models.py           #   UserProfile, Address
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
│
├── coupons/                # Discount codes
│   ├── models.py           #   Coupon (with is_valid property)
│   ├── serializers.py
│   ├── services.py         #   CouponService
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
│
├── payments/               # Payment processing
│   ├── models.py           #   Payment (multi-method)
│   ├── serializers.py
│   ├── gateways.py         #   StripeGateway, PayPalGateway, StripeWalletGateway, Factory
│   ├── services.py         #   PaymentService
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
│
├── orders/                 # Cart & order lifecycle
│   ├── models.py           #   OrderItem, Order
│   ├── serializers.py
│   ├── services.py         #   CartService
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
│
├── merchants/              # Merchant dashboard
│   ├── models.py           #   MerchantProfile, MerchantOrderFulfillment
│   ├── permissions.py      #   IsMerchant
│   ├── admin.py
│   ├── urls.py
│   ├── serializers/
│   │   ├── profile.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   └── coupons.py
│   ├── views/
│   │   ├── profile.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── coupons.py
│   │   └── analytics.py
│   └── migrations/
│
├── django_ecommerce/       # Project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── Makefile
└── .env.example
```
