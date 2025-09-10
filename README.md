# 🔐 Django Auth API (JWT + Swagger)

A simple authentication system built with Django REST Framework, JWT (SimpleJWT), and Swagger (drf-yasg).
This project includes Register, Login (with username/email), Profile API and supports Bearer Token Authentication.

---

## 🚀 Features

* User Registration (username, email, phone number, password)
* User Login with username or email
* JWT Authentication (Access & Refresh Tokens)
* Login response includes full user details
* Profile API (protected with Bearer token)
* Swagger UI for API documentation

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kanik-snippet/ecommerce_webapp.git
cd ecommerce_webapp
```

### 2. Create Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Mac**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt drf-yasg pillow
```

### 4. Apply Migrations

```bash
python manage.py makemigrations core store
python manage.py migrate
```

### 5. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Server: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📑 API Documentation

* Swagger UI → [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
* Redoc → [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

## 🔑 Authentication

Protected endpoints require Bearer Token.

Steps:

1. Login and copy the Access Token
2. In Swagger, click Authorize
3. Enter:

   ```
   Bearer <your-access-token>
   ```

Example:

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI...
```

---

## ✅ Example Login Response

```json
{
  "refresh": "eyJhbGciOiJIUzI1...",
  "access": "eyJhbGciOiJIUzI1...",
  "user": {
    "id": 1,
    "username": "kanik",
    "email": "kanik@example.com",
    "phone_number": "9876543210",
    "name": "Kanik Gupta",
    "is_superuser": true,
    "is_staff": true,
    "is_active": true
  }
}
```

---

## 📂 Project Structure

```
project-root/
│── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
│── store/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
│── config/
│   ├── settings.py
│   ├── urls.py
│
│── manage.py
```

---

## 🛠 Tech Stack

* Python 3.x
* Django
* Django REST Framework
* SimpleJWT (for authentication)
* drf-yasg (Swagger API docs)

---

## 👨‍💻 Author

Developed by Kanik 🚀
