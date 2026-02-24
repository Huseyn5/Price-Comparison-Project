import { useEffect, useState, useCallback } from "react";
import axios from "axios";
import Header from "./components/Header";
import ProductGrid from "./components/ProductGrid";
import FilterPanel from "./components/FilterPanel";
import Footer from "./components/Footer";
import LoadingSpinner from "./components/LoadingSpinner";
import "./App.css";

function App() {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sortBy, setSortBy] = useState("newest");
  const [filters, setFilters] = useState({
    category: null,
    store: null,
    minPrice: 0,
    maxPrice: 10000,
    minRating: 0
  });
  const [categories, setCategories] = useState([]);
  const [stores, setStores] = useState([]);
  const [comparison, setComparison] = useState([]);
  const [showComparison, setShowComparison] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

  // Fetch initial data
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [productsRes, categoriesRes, storesRes] = await Promise.all([
          axios.get(`${API_URL}/products?limit=100`),
          axios.get(`${API_URL}/categories`),
          axios.get(`${API_URL}/stores`)
        ]);

        setProducts(productsRes.data.data || []);
        setCategories(categoriesRes.data.categories || []);
        setStores(storesRes.data.stores || []);
      } catch (err) {
        setError("Failed to load products. Please try again later.");
        console.error("API Error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [API_URL]);

  // Apply filters and search
  useEffect(() => {
    let result = [...products];

    // Search filter
    if (searchQuery.trim()) {
      result = result.filter(p =>
        p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.description?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Category filter
    if (filters.category) {
      result = result.filter(p => p.category === filters.category);
    }

    // Store filter
    if (filters.store) {
      result = result.filter(p => p.store === filters.store);
    }

    // Price filter
    result = result.filter(p =>
      p.price >= filters.minPrice && p.price <= filters.maxPrice
    );

    // Rating filter
    result = result.filter(p => p.rating >= filters.minRating);

    // Sorting
    switch (sortBy) {
      case "price-low":
        result.sort((a, b) => a.price - b.price);
        break;
      case "price-high":
        result.sort((a, b) => b.price - a.price);
        break;
      case "rating":
        result.sort((a, b) => b.rating - a.rating);
        break;
      case "newest":
      default:
        result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        break;
    }

    setFilteredProducts(result);
  }, [products, searchQuery, filters, sortBy]);

  const handleAddToComparison = useCallback((product) => {
    setComparison(prev => {
      const exists = prev.find(p => p.id === product.id);
      if (exists) {
        return prev.filter(p => p.id !== product.id);
      }
      if (prev.length >= 5) {
        alert("Maximum 5 products can be compared");
        return prev;
      }
      return [...prev, product];
    });
  }, []);

  const handleClearComparison = () => {
    setComparison([]);
  };

  const handleResetFilters = () => {
    setFilters({
      category: null,
      store: null,
      minPrice: 0,
      maxPrice: 10000,
      minRating: 0
    });
    setSearchQuery("");
    setSortBy("newest");
  };

  return (
    <div className="app-container">
      <Header
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        comparisonCount={comparison.length}
        onShowComparison={() => setShowComparison(!showComparison)}
      />

      <main className="main-content">
        <div className="content-wrapper">
          {/* Sidebar Filters */}
          <aside className="sidebar">
            <FilterPanel
              categories={categories}
              stores={stores}
              filters={filters}
              setFilters={setFilters}
              sortBy={sortBy}
              setSortBy={setSortBy}
              onResetFilters={handleResetFilters}
            />
          </aside>

          {/* Main Content */}
          <section className="main-section">
            {error && (
              <div className="error-banner">
                <p>{error}</p>
              </div>
            )}

            {loading ? (
              <LoadingSpinner />
            ) : showComparison && comparison.length > 0 ? (
              <div className="comparison-view">
                <div className="comparison-header">
                  <h2>Product Comparison ({comparison.length})</h2>
                  <button
                    className="btn-clear"
                    onClick={handleClearComparison}
                  >
                    Clear All
                  </button>
                </div>
                <div className="comparison-table">
                  <table>
                    <thead>
                      <tr>
                        <th>Product</th>
                        <th>Price</th>
                        <th>Store</th>
                        <th>Rating</th>
                        <th>Availability</th>
                      </tr>
                    </thead>
                    <tbody>
                      {comparison.map(product => (
                        <tr key={product.id}>
                          <td>
                            <div className="comparison-product">
                              {product.image && (
                                <img src={product.image} alt={product.name} />
                              )}
                              <span>{product.name}</span>
                            </div>
                          </td>
                          <td className="price">${product.price.toFixed(2)}</td>
                          <td>{product.store}</td>
                          <td>
                            <div className="rating">
                              ⭐ {product.rating.toFixed(1)}
                            </div>
                          </td>
                          <td>
                            <span className={`availability ${product.availability}`}>
                              {product.availability === "in_stock" ? "In Stock" : "Out of Stock"}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <>
                <div className="results-header">
                  <h2>
                    Products ({filteredProducts.length})
                  </h2>
                  {comparison.length > 0 && (
                    <button
                      className="btn-comparison"
                      onClick={() => setShowComparison(true)}
                    >
                      View Comparison ({comparison.length})
                    </button>
                  )}
                </div>

                {filteredProducts.length > 0 ? (
                  <ProductGrid
                    products={filteredProducts}
                    onAddToComparison={handleAddToComparison}
                    comparisonIds={comparison.map(p => p.id)}
                  />
                ) : (
                  <div className="empty-state">
                    <p>No products found matching your criteria.</p>
                    <button className="btn-reset" onClick={handleResetFilters}>
                      Reset Filters
                    </button>
                  </div>
                )}
              </>
            )}
          </section>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
