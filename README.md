---

# 🛒 Django E-Commerce Store

A professional **Django + DRF based E-Commerce Store** with fully functional REST APIs, Swagger documentation, and a user-friendly frontend. This project is designed as an **intermediate level test project** to assess Django skills including models, serializers, views, authentication, and API documentation.

---

## 🚀 Features

### 🔑 Authentication & Users

* User registration & login with JWT authentication.
* Profile management (view & update profile).
* Admin & normal user roles.

### 🏬 Store (Products)

* Product listing with pagination, search & filters.
* Product details endpoint.
* Stock management (auto reduce on order).

### 🛒 Cart

* Add/remove products to cart.
* View current cart with items & total.
* Auto-clear cart after successful order.

### 📦 Orders

* Place order from cart.
* Track order status (**PENDING → PROCESSING → SHIPPED → DELIVERED → CANCELED**).
* Users can view their own orders.
* Admins can manage all orders (update status, cancel, delete).

### ⚡ Admin APIs

* Full CRUD on products.
* Manage orders (update status, view all orders).

### 📖 API Docs

* **Swagger UI** integration for interactive API documentation.
* Auth header support in Swagger.

### 🎨 Frontend

* Responsive & user-friendly interface (React or Bootstrap/Tailwind suggested).
* Product catalog with images.
* Add to cart & checkout flow.
* Login/Register UI.

---

## 🛠️ Tech Stack

* **Backend**: Django, Django REST Framework
* **Authentication**: JWT (SimpleJWT)
* **Database**: PostgreSQL (or MySQL/SQLite in dev)
* **API Docs**: drf-yasg (Swagger)
* **Frontend**: React.js with Bootstrap/Tailwind (Pending)

---

## 📂 Project Structure

```
EcommerceStore/
├── users/          # Authentication & user profile
├── store/          # Products, Cart, Orders
├── EcommerceStore/ # Project settings & urls
├── requirements.txt
└── README.md
```

---

## 📌 Models Overview

* **User** → custom user with roles.
* **Product** → name, description, price, stock, category.
* **Cart** → user cart with multiple items.
* **CartItem** → product, quantity, price.
* **Order** → user, shipping address, phone, total price, status.
* **OrderItem** → product, quantity, price, linked to Order.

---

## 🔗 API Endpoints (Sample)

### Auth

* `POST /api/auth/register/` → Register new user
* `POST /api/auth/login/` → Get JWT token

### Products

* `GET /api/store/products/` → List products
* `POST /api/store/products/` → Create product (Admin)

### Cart

* `GET /api/store/cart/` → View cart
* `POST /api/store/cart/add/` → Add product to cart

### Orders

* `GET /api/store/orders/` → List user orders
* `POST /api/store/orders/` → Place new order
* `GET /api/store/admin/orders/` → List all orders (Admin)
* `PATCH /api/store/admin/orders/{id}/` → Update order status

---

## 🔧 Setup & Installation

1. Clone repo:

   ```bash
   git clone https://github.com/yourusername/ecommerce-store.git
   cd ecommerce-store
   ```

2. Create virtual environment & install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run migrations:

   ```bash
   python manage.py migrate
   ```

4. Create superuser:

   ```bash
   python manage.py createsuperuser
   ```

5. Start server:

   ```bash
   python manage.py runserver
   ```

6. Access API Docs:

   * Swagger UI → [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---

## 🧪 Testing Checklist

✅ JWT authentication works (login & register)
✅ Products can be added, listed, updated, deleted
✅ Cart operations (add, view, clear) work correctly
✅ Orders create correctly & deduct stock
✅ Admin can update order status
✅ Swagger docs show all endpoints

---

## 📌 Next Steps (Optional Enhancements)

* Wishlist & product reviews.
* Payment gateway integration (Stripe/PayPal).
* Deployment on Docker & cloud hosting.

---

## 👨‍💻 Author

Designed by Kanik. 🚀

---

