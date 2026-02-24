# 🛒 PriceCompare — Product Price Comparison Website

A modern, full-stack web application that enables users to search, filter, and compare prices of electronic products across multiple online stores. Built with React, Flask, and SQLite, featuring an advanced filtering system, real-time search, and product comparison functionality.

## ✨ Features

### Frontend Features
- **🔍 Advanced Search**: Real-time search with debouncing
- **🎯 Smart Filtering**: Filter by category, store, price range, and rating
- **📊 Product Comparison**: Compare up to 5 products side-by-side
- **⭐ Rating System**: View product ratings from multiple sources
- **💰 Price Tracking**: See original prices, discounts, and current prices
- **📱 Responsive Design**: Mobile-first, works on all devices
- **🌙 Dark Mode**: Modern dark theme for comfortable browsing
- **⚡ Fast Performance**: Optimized with lazy loading and pagination
- **🎨 Beautiful UI**: Modern, clean interface with smooth animations

### Backend Features
- **🌐 RESTful API**: Comprehensive API with 15+ endpoints
- **🔐 Error Handling**: Robust error handling and validation
- **📦 Pagination**: Efficient data loading with pagination
- **🗄️ Database**: SQLite with optimized queries
- **🔄 CORS Support**: Cross-origin requests enabled
- **📊 Statistics**: Database statistics and analytics
- **🛡️ Data Validation**: Input validation and sanitization
- **🚀 Scalable**: Ready for production deployment

### Data Features
- **50+ Products**: Comprehensive dummy data for testing
- **5 Stores**: Amazon, Apple, BestBuy, Newegg, Target, etc.
- **4 Categories**: Phones, Laptops, Tablets, Smartwatches
- **Realistic Prices**: Real market prices with discounts
- **High Ratings**: 3.5-5.0 star ratings for authenticity

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Browser (React)                     │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Header | Search | Filters | Product Grid | Comparison │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓ API Requests
┌─────────────────────────────────────────────────────────────┐
│                   Flask REST API (Backend)                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  /products | /search | /filter | /compare | /statistics │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓ Database Queries
┌─────────────────────────────────────────────────────────────┐
│                    SQLite Database                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Products | Stores | Categories | Comparisons         │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
price-comparison-project/
│
├── backend/
│   ├── app.py                 # Flask API server with 15+ endpoints
│   ├── database.py            # Database initialization and queries
│   ├── scraper.py             # Web scraper with dummy data generator
│   ├── requirements.txt       # Python dependencies
│   └── products.db            # SQLite database
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   │
│   ├── src/
│   │   ├── App.jsx            # Main app component with state management
│   │   ├── App.css            # Global styles and layout
│   │   │
│   │   ├── components/
│   │   │   ├── Header.jsx          # Navigation header with search
│   │   │   ├── Header.css
│   │   │   ├── ProductGrid.jsx     # Responsive product grid
│   │   │   ├── ProductGrid.css
│   │   │   ├── ProductCard.jsx     # Individual product card
│   │   │   ├── ProductCard.css
│   │   │   ├── FilterPanel.jsx     # Advanced filter panel
│   │   │   ├── FilterPanel.css
│   │   │   ├── LoadingSpinner.jsx  # Loading indicator
│   │   │   ├── Footer.jsx          # Footer with links
│   │   │   └── Footer.css
│   │   │
│   │   ├── index.js
│   │   ├── index.css
│   │   └── setupTests.js
│   │
│   ├── package.json
│   └── .env.example
│
├── API_DOCUMENTATION.md       # Complete API reference
├── README.md                  # This file
└── .gitignore
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 16+ and npm
- **Python** 3.8+
- **Git**

### Backend Setup

#### 1. Navigate to Backend Directory
```bash
cd backend
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Initialize Database and Load Data
```bash
python scraper.py
```

This will:
- Create `products.db` with optimized schema
- Insert 50+ products across 4 categories
- Generate realistic pricing and ratings

#### 5. Run Backend Server
```bash
python app.py
```

Backend will be available at: `http://localhost:5000`

**Test API:**
```bash
curl http://localhost:5000/products
curl http://localhost:5000/categories
curl http://localhost:5000/stores
```

### Frontend Setup

#### 1. Navigate to Frontend Directory
```bash
cd frontend
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Configure Environment
Create `.env` file:
```
REACT_APP_API_URL=http://localhost:5000
```

#### 4. Run Frontend
```bash
npm start
```

Frontend will open at: `http://localhost:3000`

---

## 📚 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/products` | Get all products with pagination |
| GET | `/products/<id>` | Get single product |
| GET | `/products/search?q=query` | Search products |
| GET | `/products/filter` | Filter products by criteria |
| GET | `/products/compare?ids=1,2,3` | Compare products |
| GET | `/categories` | Get all categories |
| GET | `/categories/<name>/products` | Get products by category |
| GET | `/stores` | Get all stores |
| GET | `/stores/<name>/products` | Get products by store |
| GET | `/price-comparison?product=name` | Price comparison across stores |
| GET | `/statistics` | Database statistics |

### Admin Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/admin/products` | Create product |
| PUT | `/admin/products/<id>` | Update product |
| DELETE | `/admin/products/<id>` | Delete product |

For detailed API documentation, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## 🎯 Key Features Explained

### Advanced Filtering
Filter products by multiple criteria simultaneously:
- **Category**: Phones, Laptops, Tablets, Smartwatches
- **Store**: Amazon, Apple, BestBuy, Newegg, Target
- **Price Range**: Custom min/max price
- **Rating**: Minimum rating threshold
- **Availability**: In stock or out of stock

### Real-Time Search
- Debounced search for performance
- Searches in product names and descriptions
- Instant results as you type
- Highlights matching results

### Product Comparison
- Compare up to 5 products side-by-side
- View all details in comparison table
- See price differences at a glance
- Quick access to product links

### Responsive Design
- Mobile-first approach
- Works on phones, tablets, and desktops
- Touch-friendly interface
- Optimized performance

---

## 🔧 Technology Stack

### Frontend
- **React 19** - UI framework
- **Axios** - HTTP client
- **TailwindCSS** - Utility-first CSS
- **CSS3** - Modern styling with animations

### Backend
- **Python 3.8+** - Programming language
- **Flask 3.0** - Web framework
- **SQLite** - Database
- **BeautifulSoup4** - Web scraping
- **Requests** - HTTP library

### Tools & Services
- **Git** - Version control
- **npm** - Package manager
- **pip** - Python package manager

---

## 📊 Database Schema

### Products Table
```sql
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  category TEXT NOT NULL,
  price REAL NOT NULL,
  original_price REAL,
  discount_percentage REAL,
  store TEXT NOT NULL,
  link TEXT NOT NULL,
  image TEXT,
  rating REAL,
  availability TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

### Additional Tables
- **stores**: Store information
- **categories**: Product categories
- **comparisons**: User comparison history

---

## 🧪 Testing

### Test Backend API
```bash
# Get all products
curl http://localhost:5000/products

# Search products
curl "http://localhost:5000/products/search?q=iPhone"

# Filter products
curl "http://localhost:5000/products/filter?category=Phones&min_price=500&max_price=1500"

# Compare products
curl "http://localhost:5000/products/compare?ids=1,2,3"

# Get statistics
curl http://localhost:5000/statistics
```

### Test Frontend
1. Open `http://localhost:3000`
2. Search for products
3. Apply filters
4. Add products to comparison
5. View comparison table

---

## 🚀 Deployment

### Frontend Deployment (Vercel/Netlify)
```bash
npm run build
# Deploy the 'build' folder to Vercel or Netlify
```

### Backend Deployment (Render/Railway)
```bash
# Push to GitHub
git push origin main

# Connect repository to Render/Railway
# Set environment variables
# Deploy
```

---

## 🔮 Future Enhancements

### Short Term
- [ ] User authentication and accounts
- [ ] Wishlist/favorites feature
- [ ] Price history tracking
- [ ] Email price alerts
- [ ] Product reviews and ratings

### Medium Term
- [ ] Real web scraping from actual stores
- [ ] Advanced analytics dashboard
- [ ] Machine learning for recommendations
- [ ] Mobile app (React Native)
- [ ] Payment integration

### Long Term
- [ ] Multi-language support
- [ ] AI-powered chatbot
- [ ] Browser extension
- [ ] Price prediction using ML
- [ ] Community features

---

## 🐛 Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```bash
# Change port in app.py
app.run(host="0.0.0.0", port=5001, debug=True)
```

**Database errors:**
```bash
# Reinitialize database
rm products.db
python scraper.py
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**API connection errors:**
- Check `.env` file has correct `REACT_APP_API_URL`
- Ensure backend is running on port 5000
- Check browser console for errors

**Products not loading:**
- Verify backend is running: `http://localhost:5000/health`
- Check network tab in browser DevTools
- Clear browser cache

**Build errors:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## 📝 Best Practices

### Code Quality
- ✅ Modular component structure
- ✅ Consistent naming conventions
- ✅ Error handling and validation
- ✅ Responsive design principles
- ✅ Performance optimization

### Security
- ✅ Input validation on backend
- ✅ CORS enabled for development
- ✅ SQL injection prevention with parameterized queries
- ✅ Error messages don't expose sensitive data

### Performance
- ✅ Pagination for large datasets
- ✅ Debounced search
- ✅ Lazy loading for images
- ✅ Optimized database queries
- ✅ CSS animations for smooth UX

---

## 📄 License

MIT License - Feel free to use this project for personal or commercial purposes.

---

## 👨‍💻 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support

For issues, questions, or suggestions:
1. Check the [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
2. Review troubleshooting section
3. Open an issue on GitHub

---

## 🙏 Acknowledgments

- Built with modern web technologies
- Inspired by popular price comparison websites
- Community feedback and contributions

---

## 📈 Project Stats

- **Total Products**: 50+
- **Categories**: 4
- **Stores**: 5+
- **API Endpoints**: 15+
- **Frontend Components**: 8
- **Database Tables**: 4

---

## 🎉 Getting Started Checklist

- [ ] Clone the repository
- [ ] Install backend dependencies
- [ ] Initialize database with dummy data
- [ ] Run backend server
- [ ] Install frontend dependencies
- [ ] Configure `.env` file
- [ ] Run frontend
- [ ] Test search and filtering
- [ ] Try product comparison
- [ ] Explore API endpoints

---

**Happy price comparing! 🛍️**

Last Updated: February 2026
