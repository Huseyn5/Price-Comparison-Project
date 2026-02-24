import ProductCard from "./ProductCard";
import "./ProductGrid.css";

export default function ProductGrid({ products, onAddToComparison, comparisonIds }) {
  return (
    <div className="product-grid">
      {products.map(product => (
        <ProductCard
          key={product.id}
          product={product}
          onAddToComparison={onAddToComparison}
          isInComparison={comparisonIds.includes(product.id)}
        />
      ))}
    </div>
  );
}
