# E-commerce Store FastAPI

This project is a demonstration of a simple e-commerce backend API built using FastAPI and SQLAlchemy. It provides essential features for user management, product management, authentication, and shopping cart functionality.

## Features

**User Registration & Authentication:**
* Users can register, log in, and securely authenticate using JWT tokens.

**Product Management:**
* Authenticated users can add new products, view products, like/dislike products, and manage their own product listings.

**Shopping Cart:**
* Users can add products to their shopping cart and manage quantities.

**Like System:**
* Users can like or dislike products, with like counts tracked per product.

**Database Integration:**
* Uses SQLAlchemy ORM with PostgreSQL for persistent data storage.

## Technologies Used

* FastAPI

* SQLAlchemy

* PostgreSQL

* Pydantic

* Passlib (for password hashing)

* JOSE (for JWT token handling)

## Project Structure


* main.py – FastAPI app initialization and router inclusion

* model.py – SQLAlchemy ORM models for users, products, likes, and shopping cart

* schemas.py – Pydantic models for request/response validation

* database.py – Database connection and session management

* authentication.py – User authentication and JWT token utilities

* user.py – User-related API endpoints

* product.py – Product and shopping cart API endpoints

* hashing.py – Password hashing and verification

* jwt_token.py – JWT token creation and verification

## Getting Started

1. **Install dependencies:**

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib[bcrypt] python-jose
```

2. **Configure your PostgreSQL database** in database.py.

3. **Run the application:**

```bash
uvicorn main:app --reload
```

## Usage

* Use the provided API endpoints to register users, authenticate, manage products, and interact with the shopping cart.

* All sensitive endpoints require JWT authentication.