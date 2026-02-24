import "./ProductCard.css";

export default function ProductCard({ product, onAddToComparison, isInComparison }) {
  const discountPercentage = product.discount_percentage || 0;
  const availability = product.availability === "in_stock";

  return (
    <div className={`product-card ${!availability ? "out-of-stock" : ""}`}>
      {/* Image Section */}
      <div className="product-image-container">
        <img
          src={product.image || "https://via.placeholder.com/300x300?text=No+Image"}
          alt={product.name}
          className="product-image"
          onError={(e) => {
            e.target.src = "https://via.placeholder.com/300x300?text=No+Image";
          }}
        />
        
        {discountPercentage > 0 && (
          <div className="discount-badge">
            -{discountPercentage.toFixed(0)}%
          </div>
        )}
        
        {!availability && (
          <div className="out-of-stock-overlay">
            Out of Stock
          </div>
        )}
      </div>

      {/* Content Section */}
      <div className="product-content">
        {/* Category Badge */}
        <div className="category-badge">{product.category}</div>

        {/* Product Name */}
        <h3 className="product-name" title={product.name}>
          {product.name}
        </h3>

        {/* Description */}
        {product.description && (
          <p className="product-description">
            {product.description.substring(0, 60)}...
          </p>
        )}

        {/* Store Name */}
        <p className="store-name">📍 {product.store}</p>

        {/* Rating */}
        <div className="product-rating">
          <span className="stars">⭐ {product.rating.toFixed(1)}</span>
        </div>

        {/* Price Section */}
        <div className="price-section">
          {product.original_price && product.original_price > product.price ? (
            <>
              <span className="original-price">
                ${product.original_price.toFixed(2)}
              </span>
              <span className="current-price">
                ${product.price.toFixed(2)}
              </span>
            </>
          ) : (
            <span className="current-price">
              ${product.price.toFixed(2)}
            </span>
          )}
        </div>

        {/* Availability Status */}
        <div className={`availability-status ${product.availability}`}>
          {availability ? "✓ In Stock" : "✗ Out of Stock"}
        </div>
      </div>

      {/* Actions Section */}
      <div className="product-actions">
        <a
          href={product.link}
          target="_blank"
          rel="noreferrer"
          className="btn-buy"
          disabled={!availability}
        >
          Buy Now →
        </a>
        
        <button
          className={`btn-compare ${isInComparison ? "active" : ""}`}
          onClick={() => onAddToComparison(product)}
          title={isInComparison ? "Remove from comparison" : "Add to comparison"}
        >
          {isInComparison ? "✓ Compare" : "⚖ Compare"}
        </button>
      </div>
    </div>
  );
}
