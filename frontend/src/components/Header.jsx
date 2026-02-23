export default function Header({ searchQuery, setSearchQuery }) {
  return (
    <header
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "1rem 2rem",
        background: "linear-gradient(90deg,#0f172a,#111827)",
        boxShadow: "0 6px 18px rgba(2,6,23,0.6)",
      }}
    >
      <h1
        style={{
          margin: 0,
          fontSize: "1.6rem",
          fontWeight: 800,
          color: "#ffffff",
          letterSpacing: "-0.02em",
        }}
      >
        Price
        <span style={{ color: "#3b82f6", marginLeft: 6 }}>Compare</span>
      </h1>

      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search products..."
        style={{
          background: "#2d52a225",
          border: "1px solid rgba(255,255,255,0.06)",
          borderRadius: 9999,
          padding: "0.5rem 0.9rem",
          width: "16rem",
          outline: "none",
          boxShadow: "0 1px 3px rgba(0,0,0,0.4)",
        }}
      />
    </header>
  );
}
