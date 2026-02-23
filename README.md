# 🛒 PriceCompare — Product Price Comparison Website

A full-stack web application that allows users to compare prices of electronic products (phones, laptops, computers) across different online stores.

The system collects product information using web scraping, stores normalized product data in a database, and displays current prices through a modern web interface.

---

## ✨ Features

* 🔎 Search products across stores
* 💰 Compare prices in one place
* 🖥 Modern Apple/Wealthsimple-style UI
* 🤖 Backend ready for AI-based product categorization
* 🌐 REST API between frontend and backend
* 🗄 Database storage for products and prices

---

## 🏗 System Architecture

```
User Browser (React Frontend)
            ↓ API Requests
        Flask Backend API
            ↓
        SQLite Database
            ↑
     Selenium Scraper (Data Collector)
```

### Components

#### Frontend

* React (UI framework)
* TailwindCSS (styling)
* Axios (API communication)

#### Backend

* Python
* Flask (REST API)
* Selenium (web scraping)
* SQLite (database)

---

## 📁 Project Structure

```
price-compare-app/
│
├── backend/
│   ├── app.py            # Flask API server
│   ├── database.py       # Database logic
│   ├── scraper.py        # Scraper + data insertion
│   ├── products.db       # SQLite database
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── ProductCard.jsx
│   │   └── App.jsx
│   └── .env
│
└── README.md
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```
git clone <your-repo-url>
cd price-compare-app
```

---

## 🐍 Backend Setup (Python + Flask)

### Step 1 — Create Virtual Environment

```
cd backend
python -m venv venv
```

Activate environment:

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

---

### Step 2 — Install Dependencies

```
pip install flask flask-cors selenium
pip freeze > requirements.txt
```

---

### Step 3 — Initialize Database & Insert Sample Data

```
python scraper.py
```

This will:

* create `products.db`
* insert example products
* simulate scraping

---

### Step 4 — Run Backend Server

```
python app.py
```

Backend runs at:

```
http://localhost:5000
```

Test API:

```
http://localhost:5000/products
```

You should see JSON product data.

---

## ⚛️ Frontend Setup (React)

### Step 1 — Install Dependencies

```
cd frontend
npm install
```

---

### Step 2 — Configure Environment Variables

Create `.env` file inside `frontend/`:

```
REACT_APP_API_URL=http://localhost:5000
```

---

### Step 3 — Run Frontend

```
npm start
```

Open browser:

```
http://localhost:3000
```

---

## 🔄 Development Workflow

Typical workflow:

1. Run scraper → collects products
2. Store data in database
3. Backend exposes API endpoints
4. Frontend fetches and displays products

---

## 🤖 Scraper Overview

`scraper.py` is responsible for:

* Visiting store websites
* Extracting:

  * product name
  * price
  * store name
  * link
  * image
* Saving data into the database

Future scrapers can be added per store:

```
scrape_bestbuy()
scrape_amazon()
scrape_newegg()
```

---

## 📈 Scaling Plan

### Backend Scaling

* Replace Flask → FastAPI
* Add async scraping jobs
* Schedule scrapers using cron or Celery
* Move SQLite → PostgreSQL

### Frontend Scaling

* Add routing (React Router)
* Product detail pages
* Filters & sorting
* User accounts

### Infrastructure

* Frontend → Vercel / Netlify
* Backend → Render / AWS
* Database → Supabase / PostgreSQL

---

## 🧠 Future AI Features

Planned AI integrations:

* Product name normalization
* Feature extraction from descriptions
* Automatic product matching across stores
* Price trend prediction

---

## 🛠 Troubleshooting

### Products not showing

* Ensure backend is running on port 5000
* Restart React after editing `.env`
* Check browser console for Axios errors

### Database empty

Run:

```
python scraper.py
```

---

## 👨‍💻 Author

Built by **Huseyn Talibov**

---

## 📄 License

MIT License — free to modify and use.
