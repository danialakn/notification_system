# 📢 Real-Time Notification Microservices

A **scalable, event-driven, real-time notification system** built on a microservices architecture. This project provides a robust backend for applications requiring instant user notifications and messaging.

---

## ⚙️ Architecture Overview

This project is composed of two primary, decoupled microservices:

1. ![Django](https://img.shields.io/badge/Django-092E20?style=flat\&logo=django\&logoColor=white) **Auth Service (Django):**
   A fully RESTful service that acts as the central authority for user management, authentication, and authorization. It is the single source of truth for all user data.

2. ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat\&logo=fastapi\&logoColor=white) **Notification Service (FastAPI):**
   A high-performance asynchronous service responsible for managing persistent WebSocket connections and handling the real-time delivery of messages.

Communication between services is handled via **internal REST APIs** and coordinated asynchronously with a ![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=flat\&logo=rabbitmq\&logoColor=white) **RabbitMQ message broker**, ensuring resilience and horizontal scalability. User authentication for WebSocket connections is centralized through a ![JWT](https://img.shields.io/badge/JWT-black?style=flat\&logo=jsonwebtokens\&logoColor=white) **custom JWT validation** endpoint on the Auth Service.

```mermaid

```

---

## ✨ Key Features

* **Microservice Architecture** → Independent scaling and development of Auth (Django) and Notifications (FastAPI).
* **Real-Time Messaging** → Persistent, bidirectional communication using WebSockets.
* **Scalable Backend** → RabbitMQ with **direct** and **fanout** exchanges for private, group, and broadcast messaging.
* **Guaranteed Delivery** → Durable queues ensure messages for offline users are stored and delivered upon reconnection.
* **Secure Authentication** → Custom JWT tokens (with user roles) validated via Auth Service.
* **Multiple Databases** → SQLite for lightweight setups and PostgreSQL for production-ready environments.
* **Future-Ready** → Containerization (Docker) can be easily added.

---

## 🛠️ Technology Stack

* ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white) **Python** – Programming Language
* ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white) **FastAPI** – For the Notification Service
* ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge\&logo=django\&logoColor=white) **Django** – For the Authentication Service
* ![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge\&logo=rabbitmq\&logoColor=white) **RabbitMQ** – Message Broker
* ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white) **PostgreSQL** – Production Database
* ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge\&logo=sqlite\&logoColor=white) **SQLite** – Development/Test Database
* ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge\&logo=jsonwebtokens\&logoColor=white) **JWT** – Authentication & Authorization
* **Internal REST APIs** – For communication between services

---

## 📂 Project Structure

```
project-root/
├── authentication_service/     # Django REST API for authentication
│   ├── sample_dot_env.txt      # Example environment variables
│   └── ...
├── notification_service/       # FastAPI WebSocket notification service
│   ├── sample_dot_env.txt      # Example environment variables
│   ├── config.py               # Configuration (origins, broker, secrets)
│   ├── main.py                 # Service entry point
│   └── ...
└── README.md                   # Project documentation
```

---

## 📋 Prerequisites

* Python **3.10+**
* A running **PostgreSQL** instance *(for production)*
* **SQLite** supported out-of-the-box *(for development/testing)*
* A running **RabbitMQ** broker

---

## 🚀 Getting Started

### 1. Configure Environment Variables

Each service contains a `sample_dot_env.txt`. Create `.env` files:

```bash
cp authentication_service/sample_dot_env.txt authentication_service/.env
cp notification_service/sample_dot_env.txt notification_service/.env
```

Make sure `INTERNAL_SERVICE_KEY` is the same across both services.

### 2. Run the Auth Service (Django)

```bash
cd authentication_service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Default: `http://localhost:8000`

### 3. Run the Notification Service (FastAPI)

```bash
cd notification_service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run DB migrations (if Alembic configured)
alembic upgrade head

# Start the service
python main.py
# or
uvicorn config:app --reload --port 8001
```

Default: `http://localhost:8001`

### 4. Run the Celery Worker (Notifications)

```bash
cd notification_service
celery -A celery_app.celery_app worker --loglevel=info
```

### 5. Configure CORS & Origins

Update `config.py` inside the Notification Service with your frontend origins.

---

## 🔑 Workflow Summary

1. Client connects via WebSocket with a JWT.
2. Notification Service validates the token with Auth Service via API.
3. If valid, connection is established.
4. Messages (private, group, broadcast) are published to RabbitMQ.
5. RabbitMQ routes messages to queues.
6. Online users receive messages instantly; offline users receive messages after reconnect.

---

## 📖 Future Improvements

* Add **Docker Compose** for one-command multi-service deployment.
* Add **monitoring & observability** (Prometheus/Grafana).
* Add **retry & dead-letter queues** for failed messages.

---

## 🧑‍💻 Author

Built with ❤️ using **Django**, **FastAPI**, **RabbitMQ**, **SQLite**, **PostgreSQL**, **JWT**, and **Python**.

