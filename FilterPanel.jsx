import { useState } from "react";
import "./FilterPanel.css";

export default function FilterPanel({
  categories,
  stores,
  filters,
  setFilters,
  sortBy,
  setSortBy,
  onResetFilters
}) {
  const [expandedSections, setExpandedSections] = useState({
    category: true,
    price: true,
    store: true,
    rating: true,
    sort: true
  });

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const handlePriceChange = (type, value) => {
    setFilters(prev => ({
      ...prev,
      [type]: value
    }));
  };

  const handleCategoryChange = (category) => {
    setFilters(prev => ({
      ...prev,
      category: prev.category === category ? null : category
    }));
  };

  const handleStoreChange = (store) => {
    setFilters(prev => ({
      ...prev,
      store: prev.store === store ? null : store
    }));
  };

  const handleRatingChange = (rating) => {
    setFilters(prev => ({
      ...prev,
      minRating: prev.minRating === rating ? 0 : rating
    }));
  };

  const activeFiltersCount = [
    filters.category,
    filters.store,
    filters.minPrice > 0 || filters.maxPrice < 10000,
    filters.minRating > 0
  ].filter(Boolean).length;

  return (
    <div className="filter-panel">
      {/* Header */}
      <div className="filter-header">
        <h3>Filters</h3>
        {activeFiltersCount > 0 && (
          <button className="btn-reset-filters" onClick={onResetFilters}>
            Reset ({activeFiltersCount})
          </button>
        )}
      </div>

      {/* Sort Section */}
      <div className="filter-section">
        <button
          className="filter-section-header"
          onClick={() => toggleSection("sort")}
        >
          <span>Sort By</span>
          <span className={`arrow ${expandedSections.sort ? "expanded" : ""}`}>
            ▼
          </span>
        </button>
        {expandedSections.sort && (
          <div className="filter-options">
            {[
              { value: "newest", label: "Newest" },
              { value: "price-low", label: "Price: Low to High" },
              { value: "price-high", label: "Price: High to Low" },
              { value: "rating", label: "Highest Rated" }
            ].map(option => (
              <label key={option.value} className="filter-option">
                <input
                  type="radio"
                  name="sort"
                  value={option.value}
                  checked={sortBy === option.value}
                  onChange={(e) => setSortBy(e.target.value)}
                />
                <span>{option.label}</span>
              </label>
            ))}
          </div>
        )}
      </div>

      {/* Category Section */}
      {categories.length > 0 && (
        <div className="filter-section">
          <button
            className="filter-section-header"
            onClick={() => toggleSection("category")}
          >
            <span>Category</span>
            <span className={`arrow ${expandedSections.category ? "expanded" : ""}`}>
              ▼
            </span>
          </button>
          {expandedSections.category && (
            <div className="filter-options">
              {categories.map(category => (
                <label key={category} className="filter-option">
                  <input
                    type="checkbox"
                    checked={filters.category === category}
                    onChange={() => handleCategoryChange(category)}
                  />
                  <span>{category}</span>
                </label>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Price Range Section */}
      <div className="filter-section">
        <button
          className="filter-section-header"
          onClick={() => toggleSection("price")}
        >
          <span>Price Range</span>
          <span className={`arrow ${expandedSections.price ? "expanded" : ""}`}>
            ▼
          </span>
        </button>
        {expandedSections.price && (
          <div className="filter-price-range">
            <div className="price-input-group">
              <label>Min</label>
              <input
                type="number"
                min="0"
                max="10000"
                value={filters.minPrice}
                onChange={(e) => handlePriceChange("minPrice", parseFloat(e.target.value))}
                className="price-input"
              />
            </div>
            <div className="price-input-group">
              <label>Max</label>
              <input
                type="number"
                min="0"
                max="10000"
                value={filters.maxPrice}
                onChange={(e) => handlePriceChange("maxPrice", parseFloat(e.target.value))}
                className="price-input"
              />
            </div>
            <div className="price-range-display">
              ${filters.minPrice.toFixed(0)} - ${filters.maxPrice.toFixed(0)}
            </div>
          </div>
        )}
      </div>

      {/* Store Section */}
      {stores.length > 0 && (
        <div className="filter-section">
          <button
            className="filter-section-header"
            onClick={() => toggleSection("store")}
          >
            <span>Store</span>
            <span className={`arrow ${expandedSections.store ? "expanded" : ""}`}>
              ▼
            </span>
          </button>
          {expandedSections.store && (
            <div className="filter-options">
              {stores.map(store => (
                <label key={store} className="filter-option">
                  <input
                    type="checkbox"
                    checked={filters.store === store}
                    onChange={() => handleStoreChange(store)}
                  />
                  <span>{store}</span>
                </label>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Rating Section */}
      <div className="filter-section">
        <button
          className="filter-section-header"
          onClick={() => toggleSection("rating")}
        >
          <span>Minimum Rating</span>
          <span className={`arrow ${expandedSections.rating ? "expanded" : ""}`}>
            ▼
          </span>
        </button>
        {expandedSections.rating && (
          <div className="filter-options">
            {[
              { value: 0, label: "All Ratings" },
              { value: 3, label: "⭐⭐⭐ & Up" },
              { value: 3.5, label: "⭐⭐⭐.5 & Up" },
              { value: 4, label: "⭐⭐⭐⭐ & Up" },
              { value: 4.5, label: "⭐⭐⭐⭐.5 & Up" }
            ].map(option => (
              <label key={option.value} className="filter-option">
                <input
                  type="radio"
                  name="rating"
                  value={option.value}
                  checked={filters.minRating === option.value}
                  onChange={() => handleRatingChange(option.value)}
                />
                <span>{option.label}</span>
              </label>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
