import "./Header.css";

export default function Header({
  searchQuery,
  setSearchQuery,
  comparisonCount,
  onShowComparison
}) {
  return (
    <header className="header">
      <div className="header-container">
        {/* Logo */}
        <div className="logo">
          <h1>
            Price<span>Compare</span>
          </h1>
          <p className="tagline">Find the best deals instantly</p>
        </div>

        {/* Search Bar */}
        <div className="search-container">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search products..."
            className="search-input"
          />
          <span className="search-icon">🔍</span>
        </div>

        {/* Comparison Button */}
        {comparisonCount > 0 && (
          <button className="btn-comparison-header" onClick={onShowComparison}>
            <span className="comparison-icon">⚖</span>
            <span className="comparison-count">{comparisonCount}</span>
          </button>
        )}
      </div>
    </header>
  );
}
