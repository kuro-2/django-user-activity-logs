🤝 Author
👤 Rohan Sharma
📝 Submitted as part of the Junior Django Developer Assignment
📧 rohan.sharma6004@gmail.com
https://github.com/kuro-2/django-user-activity-logs.git

# 🛠️ User Activity Log – Junior Django Assignment

A Django + DRF mini project that tracks user activity logs, implements filtering, caching with Redis, and a simple workflow transition system.  
Fully aligned with the assignment requirements, with test cases and admin interface included.

---

## 🚀 Features

✅ User Activity Log Model  
✅ PostgreSQL-backed data storage  
✅ DRF-powered CRUD API  
✅ Filter logs by action and date  
✅ Redis cache on list API (1-min timeout)  
✅ PATCH endpoint for status transitions  
✅ Secure configuration via `.env`  
✅ Admin dashboard  
✅ Pytest test suite

---

## 📂 Tech Stack

| Component   | Tech Used                        |
|-------------|----------------------------------|
| Backend     | Django 5.0.4, DRF 3.15.1         |
| Database    | PostgreSQL                       |
| Cache       | Redis via `django-redis`         |
| Tests       | Pytest, pytest-django            |
| Auth        | Django admin + DRF session auth  |

---

## 📸 Screenshots

See `/screenshots/` folder for visuals of:

- Admin login + model
- DRF API login & usage
- Filters & status transitions
- Redis caching demo
- Pytest test results

---

## 🔐 Environment Config (`.env`)

```env
DEBUG=True
SECRET_KEY=my-secret-key

POSTGRES_DB=activity_db
POSTGRES_USER=activity_user
POSTGRES_PASSWORD=your_paasword_here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/1
