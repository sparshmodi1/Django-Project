# Django REST Framework — Modular Entity & Mapping System

A modular Django REST Framework backend for managing **Vendors**, **Products**, **Courses**, **Certifications**, and their mappings.

Built using **APIView only** — no ViewSets, no GenericAPIView, no mixins, no routers.
API documentation powered by **drf-yasg** (Swagger + ReDoc).

---

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Programming language |
| Django | 4.2+ | Web framework |
| Django REST Framework | 3.14+ | API framework |
| drf-yasg | 1.21+ | Swagger / ReDoc docs |
| SQLite | built-in | Database (development) |

---

## Project Structure

```
django_project/
│
├── core/                               # Project config
│   ├── settings.py                     # All settings
│   ├── urls.py                         # Root URL config
│   └── wsgi.py                         # WSGI entry point
│
├── utils.py                            # Shared base model + helper functions
├── manage.py                           # Django management CLI
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
│
├── vendor/                             # Master app — Vendor
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── product/                            # Master app — Product
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── course/                             # Master app — Course
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── certification/                      # Master app — Certification
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── vendor_product_mapping/             # Mapping app — Vendor → Product
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── product_course_mapping/             # Mapping app — Product → Course
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── course_certification_mapping/       # Mapping app — Course → Certification
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
└── management/
    └── commands/
        └── seed_data.py                # Custom command to load sample data
```

---

## Setup & Installation

### Step 1 — Clone or extract the project

```bash
cd django_project
```

### Step 2 — Create a virtual environment

```bash
# Create
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Create migration files

```bash
python manage.py makemigrations vendor product course certification vendor_product_mapping product_course_mapping course_certification_mapping
```

### Step 5 — Apply migrations

```bash
python manage.py migrate
```

### Step 6 — Create superuser (for Django admin panel)

```bash
python manage.py createsuperuser
```

### Step 7 — Load sample data (optional)

```bash
python manage.py seed_data
```

This seeds the database with:
- 3 Vendors
- 4 Products
- 5 Courses
- 4 Certifications
- 5 Vendor-Product mappings
- 5 Product-Course mappings
- 5 Course-Certification mappings

### Step 8 — Run the development server

```bash
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000`

---

## API Documentation

Once the server is running, visit:

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/swagger/` | Swagger UI — interactive API explorer |
| `http://127.0.0.1:8000/redoc/` | ReDoc — clean reference documentation |
| `http://127.0.0.1:8000/admin/` | Django admin panel |

---

## API Endpoints

### Vendors

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/vendors/` | List all vendors |
| POST | `/api/vendors/` | Create a vendor |
| GET | `/api/vendors/<id>/` | Retrieve a vendor |
| PUT | `/api/vendors/<id>/` | Full update |
| PATCH | `/api/vendors/<id>/` | Partial update |
| DELETE | `/api/vendors/<id>/` | Soft delete |

### Products

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products/` | List all products |
| POST | `/api/products/` | Create a product |
| GET | `/api/products/<id>/` | Retrieve a product |
| PUT | `/api/products/<id>/` | Full update |
| PATCH | `/api/products/<id>/` | Partial update |
| DELETE | `/api/products/<id>/` | Soft delete |

### Courses

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/courses/` | List all courses |
| POST | `/api/courses/` | Create a course |
| GET | `/api/courses/<id>/` | Retrieve a course |
| PUT | `/api/courses/<id>/` | Full update |
| PATCH | `/api/courses/<id>/` | Partial update |
| DELETE | `/api/courses/<id>/` | Soft delete |

### Certifications

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/certifications/` | List all certifications |
| POST | `/api/certifications/` | Create a certification |
| GET | `/api/certifications/<id>/` | Retrieve a certification |
| PUT | `/api/certifications/<id>/` | Full update |
| PATCH | `/api/certifications/<id>/` | Partial update |
| DELETE | `/api/certifications/<id>/` | Soft delete |

### Vendor-Product Mappings

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/vendor-product-mappings/` | List all mappings |
| POST | `/api/vendor-product-mappings/` | Create a mapping |
| GET | `/api/vendor-product-mappings/<id>/` | Retrieve a mapping |
| PUT | `/api/vendor-product-mappings/<id>/` | Full update |
| PATCH | `/api/vendor-product-mappings/<id>/` | Partial update |
| DELETE | `/api/vendor-product-mappings/<id>/` | Soft delete |

### Product-Course Mappings

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/product-course-mappings/` | List all mappings |
| POST | `/api/product-course-mappings/` | Create a mapping |
| GET | `/api/product-course-mappings/<id>/` | Retrieve a mapping |
| PUT | `/api/product-course-mappings/<id>/` | Full update |
| PATCH | `/api/product-course-mappings/<id>/` | Partial update |
| DELETE | `/api/product-course-mappings/<id>/` | Soft delete |

### Course-Certification Mappings

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/course-certification-mappings/` | List all mappings |
| POST | `/api/course-certification-mappings/` | Create a mapping |
| GET | `/api/course-certification-mappings/<id>/` | Retrieve a mapping |
| PUT | `/api/course-certification-mappings/<id>/` | Full update |
| PATCH | `/api/course-certification-mappings/<id>/` | Partial update |
| DELETE | `/api/course-certification-mappings/<id>/` | Soft delete |

---

## Query Parameter Filtering

All list endpoints support query parameter filtering.

### Master entity filters

```
GET /api/vendors/?is_active=true
GET /api/vendors/?name=tech
GET /api/products/?vendor_id=1
GET /api/products/?is_active=true
GET /api/courses/?product_id=2
GET /api/courses/?is_active=true
GET /api/certifications/?course_id=3
GET /api/certifications/?is_active=true
```

### Mapping filters

```
GET /api/vendor-product-mappings/?vendor_id=1
GET /api/vendor-product-mappings/?product_id=2
GET /api/vendor-product-mappings/?primary_mapping=true
GET /api/vendor-product-mappings/?is_active=true
GET /api/product-course-mappings/?product_id=1
GET /api/product-course-mappings/?course_id=2
GET /api/product-course-mappings/?primary_mapping=true
GET /api/course-certification-mappings/?course_id=1
GET /api/course-certification-mappings/?certification_id=2
GET /api/course-certification-mappings/?primary_mapping=true
```

---

## Request & Response Examples

### Create a Vendor

**Request**
```http
POST /api/vendors/
Content-Type: application/json

{
    "name": "Tech Corp",
    "code": "TECH001",
    "description": "A technology vendor"
}
```

**Response — 201 Created**
```json
{
    "id": 1,
    "name": "Tech Corp",
    "code": "TECH001",
    "description": "A technology vendor",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### Create a Vendor-Product Mapping

**Request**
```http
POST /api/vendor-product-mappings/
Content-Type: application/json

{
    "vendor": 1,
    "product": 1,
    "primary_mapping": true
}
```

**Response — 201 Created**
```json
{
    "id": 1,
    "vendor": 1,
    "vendor_name": "Tech Corp",
    "product": 1,
    "product_name": "Python Bootcamp",
    "primary_mapping": true,
    "is_active": true,
    "created_at": "2024-01-15T10:35:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
}
```

---

### Partial Update a Course

**Request**
```http
PATCH /api/courses/1/
Content-Type: application/json

{
    "description": "Updated course description"
}
```

**Response — 200 OK**
```json
{
    "id": 1,
    "name": "Python Basics",
    "code": "CRS001",
    "description": "Updated course description",
    "is_active": true,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
}
```

---

### Soft Delete a Vendor

**Request**
```http
DELETE /api/vendors/1/
```

**Response — 200 OK**
```json
{
    "message": "Vendor deactivated successfully."
}
```

---

## Validation Rules

### Master entities
- `name` — required
- `code` — required, must be unique across all records of that entity
- `description` — optional
- `is_active` — defaults to `true`

### Mapping entities
- Both foreign keys are required and must reference active records
- The same parent-child pair cannot be mapped twice
- Only one `primary_mapping = true` is allowed per parent at each level

---

## Validation Error Examples

**Duplicate code**
```json
{
    "code": ["A vendor with this code already exists."]
}
```

**Duplicate mapping**
```json
{
    "non_field_errors": ["This vendor-product mapping already exists."]
}
```

**Duplicate primary mapping**
```json
{
    "non_field_errors": ["This vendor already has a primary product mapping. Only one primary mapping is allowed per vendor."]
}
```

**Inactive foreign key**
```json
{
    "vendor": ["Vendor does not exist or is inactive."]
}
```

---

## Soft Delete Behaviour

All `DELETE` endpoints perform a **soft delete** — the record is not removed from the database. Instead `is_active` is set to `False`.

To retrieve soft-deleted records:
```
GET /api/vendors/?is_active=false
```

To retrieve only active records:
```
GET /api/vendors/?is_active=true
```

---

## Design Decisions

**APIView only** — All views are written using `APIView` with manually defined `get`, `post`, `put`, `patch`, `delete` methods. No ViewSets, GenericAPIView, mixins, or routers are used anywhere.

**Shared TimeStampedModel** — A single abstract base model in `utils.py` provides `created_at` and `updated_at` to all 7 models without repeating the fields.

**Custom object fetcher** — `get_object_or_404_custom()` in `utils.py` handles `DoesNotExist` gracefully and returns `None` instead of raising an exception, keeping view logic clean.

**Database-level uniqueness** — Mapping models use `UniqueConstraint` for an extra layer of protection beyond serializer validation.

**Modular structure** — Each entity and each mapping lives in its own Django app with its own `models.py`, `serializers.py`, `views.py`, `urls.py`, and `admin.py`.

---

## Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'vendor',
    'product',
    'course',
    'certification',
    'vendor_product_mapping',
    'product_course_mapping',
    'course_certification_mapping',
]
```

---

## Requirements

```
Django==4.2.7
djangorestframework==3.14.0
drf-yasg==1.21.7
```

Install with:
```bash
pip install -r requirements.txt
```
