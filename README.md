# Django Modular Entity & Mapping System

A Django REST Framework backend for managing Vendors, Products, Courses, Certifications, and their mappings. All APIs are built using `APIView` only. Documentation powered by `drf-yasg`.

---

## Project Structure

```
django_project/
├── core/                          # Project settings, root URLs, wsgi
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── utils.py                       # Shared: TimeStampedModel, helpers
├── manage.py
├── requirements.txt
│
├── vendor/                        # Master app
├── product/                       # Master app
├── course/                        # Master app
├── certification/                 # Master app
│
├── vendor_product_mapping/        # Mapping app
├── product_course_mapping/        # Mapping app
├── course_certification_mapping/  # Mapping app
│
└── management/
    └── commands/
        └── seed_data.py           # Seed command
```

Each app contains: `models.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`

---

## Setup Steps

### 1. Clone / extract the project

```bash
cd django_project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations vendor product course certification vendor_product_mapping product_course_mapping course_certification_mapping
python manage.py migrate
```

### 5. Create a superuser (optional, for Django admin)

```bash
python manage.py createsuperuser
```

### 6. Seed sample data

```bash
python manage.py seed_data
```

### 7. Start the development server

```bash
python manage.py runserver
```

---

## Installed Apps

```python
INSTALLED_APPS = [
    ...
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

## API Documentation

| URL | Description |
|-----|-------------|
| `/swagger/` | Swagger UI — interactive API explorer |
| `/redoc/` | ReDoc — clean reference documentation |
| `/admin/` | Django admin panel |

---

## API Endpoints

### Master Entities

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/vendors/` | List vendors |
| POST | `/api/vendors/` | Create vendor |
| GET | `/api/vendors/<id>/` | Retrieve vendor |
| PUT | `/api/vendors/<id>/` | Full update |
| PATCH | `/api/vendors/<id>/` | Partial update |
| DELETE | `/api/vendors/<id>/` | Soft delete (sets is_active=False) |

Same pattern applies for `/api/products/`, `/api/courses/`, `/api/certifications/`.

### Mapping APIs

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/vendor-product-mappings/` | List mappings |
| POST | `/api/vendor-product-mappings/` | Create mapping |
| GET | `/api/vendor-product-mappings/<id>/` | Retrieve |
| PUT | `/api/vendor-product-mappings/<id>/` | Full update |
| PATCH | `/api/vendor-product-mappings/<id>/` | Partial update |
| DELETE | `/api/vendor-product-mappings/<id>/` | Soft delete |

Same pattern for `/api/product-course-mappings/` and `/api/course-certification-mappings/`.

---

## Query Parameter Filtering

### Master entities

```
GET /api/products/?vendor_id=1          # Products mapped to vendor 1
GET /api/courses/?product_id=2          # Courses mapped to product 2
GET /api/certifications/?course_id=3    # Certifications mapped to course 3
GET /api/vendors/?is_active=true        # Active vendors only
GET /api/vendors/?name=tech             # Vendors with "tech" in name
```

### Mapping lists

```
GET /api/vendor-product-mappings/?vendor_id=1
GET /api/vendor-product-mappings/?primary_mapping=true
GET /api/product-course-mappings/?product_id=2
GET /api/course-certification-mappings/?course_id=1&is_active=true
```

---

## Validation Rules

- `code` is unique per master entity — duplicate codes are rejected
- Duplicate mappings (same parent + child pair) are rejected
- Only one `primary_mapping=True` allowed per parent at each mapping level
- Foreign keys must reference active records
- All required fields are enforced at serializer level

### Example validation errors

```json
// Duplicate mapping
{"non_field_errors": ["This vendor-product mapping already exists."]}

// Duplicate primary mapping
{"non_field_errors": ["This vendor already has a primary product mapping."]}

// Duplicate code
{"code": ["A vendor with this code already exists."]}
```

---

## Soft Delete

All DELETE endpoints perform a soft delete by setting `is_active = False`. Records are retained in the database and can be filtered using `?is_active=false`.

---

## API Usage Examples

### Create a vendor

```bash
curl -X POST http://127.0.0.1:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corp", "code": "ACME001", "description": "Sample vendor"}'
```

### Create a vendor-product mapping

```bash
curl -X POST http://127.0.0.1:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{"vendor": 1, "product": 1, "primary_mapping": true}'
```

### Filter products by vendor

```bash
curl http://127.0.0.1:8000/api/products/?vendor_id=1
```

### Partial update a course

```bash
curl -X PATCH http://127.0.0.1:8000/api/courses/1/ \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description"}'
```

---

## Technical Constraints Met

- Uses `APIView` only — no ViewSets, no GenericAPIView, no mixins, no routers
- All HTTP methods (`get`, `post`, `put`, `patch`, `delete`) written manually
- Swagger and ReDoc documentation at `/swagger/` and `/redoc/`
- Shared `TimeStampedModel` abstract base for all models
- Custom `get_object_or_404_custom` utility to handle `DoesNotExist` cleanly
- Soft delete via `is_active` flag on all entities and mappings
