# CampusCanteen — Cloud-Based Canteen Management System

A full-stack, database-backed canteen ordering system built with **Django**,
**PostgreSQL (hosted on Supabase)**, and **Bootstrap 5**. Students can browse
the menu, add items to a cart, place orders, and track their status in real
time. Admins get a dashboard to manage food items, categories, orders, and
registered users.

This is a genuinely functional application — every action (register, login,
add to cart, place an order, change an order's status) is backed by real
database operations. Nothing is stored only in the browser.

---

## 1. Project Introduction

CampusCanteen digitizes a college canteen's ordering process. Instead of
queuing at a counter, students log in, browse the digital menu, place an
order, and watch it move through **Pending → Preparing → Ready → Completed**.
Canteen staff manage the whole
 operation — menu, categories, orders, and
users — from one dashboard.

## 2. Features

**Student**
- Register / login / logout (Django auth, hashed passwords)
- Browse, search, and filter the food menu by category
- View food item details
- Add to cart, update quantity, remove items
- Checkout and place an order (unique order number, e.g. `ORD-2026-0001`)
- View order history and live order status tracking
- Edit profile (name, email, phone, address)
- Pay securely online via Razorpay (cards, UPI, netbanking) at checkout


**Admin**
- Add / edit / delete food items, with image upload
- Set price and availability per item
- Manage categories
- View and update the status of every order
- View registered users
- Dashboard with live stats: total users, food items, orders, pending /
  completed orders, today's orders, today's revenue, plus charts for
  daily orders, revenue, and the most popular food items
- See payment status (Paid / Unpaid) for every order

## 3. Technology Used

| Layer          | Technology                                   |
|----------------|-----------------------------------------------|
| Frontend       | HTML5, CSS3, Bootstrap 5, vanilla JavaScript, Chart.js |
| Backend        | Python 3, Django 5                            |
| Database       | PostgreSQL, hosted on **Supabase**            |
| Auth           | Django's built-in authentication system       |
| Static/Media   | WhiteNoise (static), Django FileField (media) |
| Config         | python-decouple (`.env` environment variables)|
| Payments       | Razorpay (Test Mode) — card, UPI, netbanking          |

## Payment Gateway (Razorpay)

Payments are handled through **Razorpay** in Test Mode:

- When a student places an order, a Razorpay order is created and a
  payment popup opens (Card / UPI / Netbanking).
- On successful payment, the payment is **verified server-side** using
  Razorpay's signature verification (`razorpay_client.utility.verify_payment_signature`)
  before the order is marked as paid — this prevents fake/tampered payment
  confirmations from the browser.
- The `Order` model tracks `razorpay_order_id`, `razorpay_payment_id`,
  and `is_paid`.
- Admins can see the payment status (Paid / Unpaid) for every order in
  the Order Management dashboard.

**Setup:** Add your Razorpay Test Mode keys to `.env`:

## 4. System Requirements

- Python 3.10+
- pip
- A free [Supabase](https://supabase.com) account (for the cloud Postgres DB)
- (Optional) Git, a cloud host such as Render / Railway / PythonAnywhere / Heroku-compatible platform

## 5. Installation Steps

```bash
# 1. Clone / unzip the project, then enter the folder
cd canteen_management

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the environment template and fill in real values
cp .env.example .env
```

## 6. Database Configuration

The app reads all DB credentials from environment variables — **nothing is
hard-coded**. You can configure it two ways in `.env`:

**Option A — individual fields**
```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-db-password
DB_HOST=db.your-project-ref.supabase.co
DB_PORT=5432
```

**Option B — a single connection string**
```
DATABASE_URL=postgresql://postgres:password@db.your-project-ref.supabase.co:5432/postgres
```

If neither `DATABASE_URL` nor `DB_PASSWORD` is set, the app automatically
falls back to a local SQLite database (`db.sqlite3`) so you can try it out
immediately before setting up Supabase.

## 7. Supabase Configuration

1. Create a free project at [supabase.com](https://supabase.com).
2. Go to **Project Settings → Database**.
3. Copy the **connection string** (or the individual Host / Port / User /
   Password / Database name fields) into your `.env` file as shown above.
4. Supabase's default Postgres port is `5432` (direct connection) or `6543`
   (connection pooler, recommended for serverless/production). Either works
   with this project — just update `DB_PORT` / `DATABASE_URL` accordingly.
5. Make sure "Enforce SSL" is respected — `dj_database_url` / `psycopg2`
   will use SSL automatically when connecting to Supabase's hostname.

## 8. Running the Project Locally

```bash
# Apply database migrations (creates all tables in Supabase/SQLite)
python manage.py migrate

# Load sample categories, food items, and an admin superuser
python manage.py seed_data

# (Optional) create your own superuser instead of/in addition to seed_data
python manage.py createsuperuser

# Collect static files (only needed once, or after CSS/JS changes)
python manage.py collectstatic --noinput

# Run the development server
python manage.py runserver
```

Visit:
- `http://127.0.0.1:8000/` — student-facing site
- `http://127.0.0.1:8000/dashboard/` — admin dashboard (staff users only)
- `http://127.0.0.1:8000/django-admin/` — Django's built-in admin

## 9. Cloud Deployment Instructions

The project is deployment-ready for any platform that runs Python (Render,
Railway, Heroku-style platforms, PythonAnywhere, a VPS, etc.). General steps:

1. Push the project to a Git repository.
2. On your hosting platform, set the following environment variables
   (mirroring `.env.example`): `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`,
   `DATABASE_URL` (or the `DB_*` fields), `CSRF_TRUSTED_ORIGINS`.
3. Set the build command to `pip install -r requirements.txt` and the
   release/pre-start command to:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
4. Set the start command to:
   ```bash
   gunicorn config.wsgi:application
   ```
5. Static files are served via **WhiteNoise** in production, so no separate
   static file host is required. Uploaded media (food images) is served
   from the `media/` folder — on platforms with an ephemeral filesystem
   (e.g. Heroku-style dynos), point `MEDIA_ROOT` at a persistent volume or
   swap in a cloud storage backend (e.g. `django-storages` + S3/Supabase
   Storage) for production use.
6. With `DEBUG=False`, Django automatically enforces HTTPS redirects,
   secure cookies, and HSTS (see `config/settings.py`).

## 10. Admin Login Setup

Running `python manage.py seed_data` creates a default superuser:

```
username: admin
password: AdminPass123
```

**Change this password immediately** after first login, either via
`http://127.0.0.1:8000/django-admin/` or `python manage.py changepassword admin`.

Any user with `is_staff=True` can access `/dashboard/`. Regular students are
blocked from every dashboard view and URL by the `admin_required` decorator
(`dashboard/decorators.py`), which checks `request.user.is_staff` — not
just hides the link in the UI.

## 11. Project Structure

```
canteen_management/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── config/            # Django project settings, root URLs, WSGI/ASGI
├── accounts/          # Registration, login/logout, profile, Profile model
├── menu/              # Category & FoodItem models, menu browsing, seed_data command
├── cart/               # Cart & CartItem models, add/update/remove
├── orders/             # Order & OrderItem models, checkout, tracking
├── dashboard/          # Admin-only dashboard, food/category/order/user management
├── templates/          # All HTML templates (Bootstrap 5 based)
├── static/             # CSS/JS
└── media/              # Uploaded food images (created at runtime)
```

## 12. Future Scope

- Online payment gateway integration (Razorpay / Stripe)
- Real-time order status updates via WebSockets (Django Channels)
- SMS/email/push notifications when order status changes
- QR-code based order pickup verification
- Multi-canteen / multi-branch support
- Ratings and reviews for food items
- Loyalty points / wallet system
- Native mobile app using the same Django backend as an API

---

### Security notes
- Passwords are hashed by Django's auth system (PBKDF2 by default).
- CSRF protection is enabled globally; every POST form includes `{% csrf_token %}`.
- Admin-only views are protected server-side (`is_staff` check), not just
  hidden in the UI.
- `SECRET_KEY` and database credentials are never hard-coded — only read
  from environment variables via `python-decouple`.
- `DEBUG` is `True` only for local development and must be set to `False`
  in production (`.env`).
