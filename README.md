# CampusCanteen — Cloud-Based Canteen Management System

A full-stack, database-backed canteen ordering system built with **Django**,
**PostgreSQL (hosted on Supabase)**, and **Bootstrap 5**. Students can browse
the menu, add items to a cart, place orders, submit custom food requests, and
track order status in real time. Admins get a dashboard to manage food items,
categories, orders, custom food requests, and registered users.

This is a genuinely functional application — every action (register, login,
add to cart, place an order, submit a custom request, change a status) is
backed by real database operations. Nothing is stored only in the browser.

---

## 1. Project Introduction

CampusCanteen digitizes a college canteen's ordering process. Instead of
queuing at a counter, students log in, browse the digital menu, place an
order, and watch it move through **Pending → Preparing → Ready → Completed**.

For food that isn't on the regular menu, students can also submit a
**Custom Food Request** specifying what they need and the time they need it
by. Canteen staff manage the whole operation — menu, categories, orders,
custom requests, and users — from one dashboard.

## 2. Features

**Student**
- Register / login / logout (Django auth, hashed passwords)
- Browse, search, and filter the food menu by category
- View food item details
- Add to cart, update quantity, remove items
- Checkout and place an order (unique order number, e.g. `ORD-2026-0001`)
- View order history and live order status tracking
- **Submit a Custom Food Request** for items not on the regular menu,
  specifying the food needed and the required/scheduled time
- Edit profile (name, email, phone, address)
- Pay securely online via Razorpay (cards, UPI, netbanking) at checkout

**Admin**
- Add / edit / delete food items, with image upload
- Set price and availability per item
- Manage categories
- View and update the status of every order
- **View and manage Custom Food Requests** from a dedicated dashboard section
- **Update Custom Food Request status** as preparation progresses
  (`Pending → Accepted → Preparing → Ready → Completed`, with `Rejected`
  available for requests that cannot be fulfilled)
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

## 4. Custom Food Request System

In addition to ordering from the regular menu, students can submit a
**custom food request** for items that aren't listed, along with the time
they need it by.

**How it works:**
1. A logged-in student opens **Custom Order** from the navbar and fills in
   the requested food item and the required/scheduled time.
2. The request is saved to the database and appears in the admin's
   **Food Requests** section.
3. The admin reviews the request and moves it through the status workflow
   below as preparation progresses.

**Status workflow**

| Status      | Meaning                                                    |
|-------------|-------------------------------------------------------------|
| Pending     | Request submitted by student, awaiting admin review          |
| Accepted    | Admin has approved the request                                |
| Preparing   | Food item is currently being prepared                         |
| Ready       | Food is ready for pickup                                      |
| Completed   | Request has been fulfilled and collected                      |
| Rejected    | Request could not be fulfilled                                |

> **Note — in progress:** letting students view their own submitted custom
> requests and track the status themselves (rather than only the admin
> seeing it) is planned as the next stage of this feature and is not fully
> implemented yet.

### Navigation for logged-in students

The navbar for authenticated students includes:

- **Custom Order** — submit a custom food request
- **My Orders**
- **Cart**
- **Profile**
- **Logout**

Admin/staff users see an **Admin Dashboard** link in place of the
student-specific navigation.

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

**Setup:** Add your Razorpay Test Mode keys to `.env`.

## 5. System Requirements

- Python 3.10+
- pip
- A free [Supabase](https://supabase.com) account (for the cloud Postgres DB)
- (Optional) Git, a cloud host such as Render / Railway / PythonAnywhere / Heroku-compatible platform

## 6. Installation Steps

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

## 7. Database Configuration

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

## 8. Supabase Configuration

1. Create a free project at [supabase.com](https://supabase.com).
2. Go to **Project Settings → Database**.
3. Copy the **connection string** (or the individual Host / Port / User /
   Password / Database name fields) into your `.env` file as shown above.
4. Supabase's default Postgres port is `5432` (direct connection) or `6543`
   (connection pooler, recommended for serverless/production). Either works
   with this project — just update `DB_PORT` / `DATABASE_URL` accordingly.
5. Make sure "Enforce SSL" is respected — `dj_database_url` / `psycopg2`
   will use SSL automatically when connecting to Supabase's hostname.

## 9. Running the Project Locally

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
- `http://127.0.0.1:8000/dashboard/` — admin dashboard (staff users only, includes Food Requests)
- `http://127.0.0.1:8000/django-admin/` — Django's built-in admin

## 10. Cloud Deployment Instructions

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

## 11. Admin Login Setup

Running `python manage.py seed_data` creates a default superuser:

```
username: admin
password: AdminPass123
```

**Change this password immediately** after first login, either via
`http://127.0.0.1:8000/django-admin/` or `python manage.py changepassword admin`.

Any user with `is_staff=True` can access `/dashboard/`, including the Food
Requests section. Regular students are blocked from every dashboard view
and URL by the `admin_required` decorator (`dashboard/decorators.py`),
which checks `request.user.is_staff` — not just hides the link in the UI.

## 12. Project Structure

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
├── orders/             # Order & OrderItem models, checkout, tracking,
│                       # plus the Custom Food Request model, submission
│                       # form, and status workflow
├── dashboard/          # Admin-only dashboard, food/category/order/request/user management
├── templates/          # All HTML templates (Bootstrap 5 based)
├── static/             # CSS/JS
└── media/              # Uploaded food images (created at runtime)
```

## 13. Future Scope

- Let students view their own submitted custom food requests and track
  status in real time *(in progress — planned next stage)*
- Real-time order/request status updates via WebSockets (Django Channels)
- SMS/email/push notifications when order or request status changes
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
