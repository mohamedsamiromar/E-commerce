---
name: project-ecommerce
description: Django REST e-commerce project — architecture, known issues, and decisions
metadata:
  type: project
---

Django REST API e-commerce project (`django_ecommerce`). PostgreSQL backend. Token auth + allauth. Runs on Docker via docker-compose.

Key files: `project/models.py`, `project/views.py`, `project/services.py`, `project/serializers.py`, `project/payment_gateways.py`, `project/filters.py`, `project/urls.py`, `django_ecommerce/settings.py`.

**Architecture decisions:**
- Views are thin — business logic delegated to `CartService`, `PaymentService`, `CouponService` in `services.py`
- Payment gateways use an ABC pattern (`PaymentGateway`) + `PaymentGatewayFactory` in `payment_gateways.py`
- Supported payment methods: Stripe (token & PaymentIntent), PayPal, Apple Pay, Google Pay
- `Category` model added; `Item` has `in_stock`, `created_at`, `updated_at`
- `Coupon` has `active`, `valid_from`, `valid_to` with `is_valid` property
- `Order.get_total()` never returns negative (uses `max(..., 0)`)
- `Order.ref_code` auto-generated via `uuid4().hex[:12].upper()` on first save

**Migration chain:** 0001→0002→0003→0004 (original) → 0005 (rename OrderItem.items→item) → 0006 (Category, Item renames, Payment multi-method, Coupon validity fields)

**Why:** Originally the models.py had drifted far from the migrations — OneToOneField instead of ForeignKey on Order/Address/Payment, field name typos (titie vs title), missing `get_final_price` method that was called by `get_total`. All fixed in this session.

**How to apply:** When suggesting schema changes, respect the migration chain above. When adding features, follow the service-layer pattern (thin views, logic in services.py).
