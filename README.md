# 🍞 BakeryBackend

A FastAPI-based backend service for managing a Favorites API — built for the Bakery app ecosystem.

## 🚀 Features

-  Built with FastAPI
-  Favorites API to manage user-preferred items
-  SQLite database (via `favorites.db`)
-  Modular design using routers
-  Pydantic models for data validation

## 📁 Project Structure
├── main.py # Entry point for the FastAPI app
├── database.py # DB connection and setup
├── models.py # SQLAlchemy models
├── schemas.py # Pydantic schemas
├── routers/ # API route definitions
├── favorites.db # SQLite database file
├── requirements.txt # Python dependencies


## ▶️ Getting Started

###  Requirements

- Python 3.9+
- pip

###  Installation

```bash
# Clone the repo
git clone 
cd 

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # on Linux/macOS
venv\Scripts\activate     # on Windows

# Install dependencies
pip install -r requirements.txt

###Running the Server

uvicorn main:app --reload

🛠 Technologies Used
FastAPI

SQLite

SQLAlchemy

Pydantic



