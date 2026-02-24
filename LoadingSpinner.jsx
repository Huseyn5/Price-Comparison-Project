export default function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p style={{ marginTop: "1rem", color: "#cbd5e1" }}>
        Loading products...
      </p>
    </div>
  );
}
