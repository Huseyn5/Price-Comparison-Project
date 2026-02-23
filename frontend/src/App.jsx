import { useEffect, useState } from "react";
import axios from "axios";
import Header from "./components/Header";
import ProductCard from "./components/ProductCard";
import Footer from "./components/Footer";

function App() {
  const [products, setProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/products`)
         .then(res => setProducts(res.data))
         .catch(err => console.error("Backend Error:", err));
  }, []);

  const filteredProducts = products.filter(p =>
    p.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-gray-950 to-black flex flex-col"s>
      <Header searchQuery={searchQuery} setSearchQuery={setSearchQuery} />

      <main className="flex-grow max-w-7xl mx-auto w-full px-6 py-10">
        {filteredProducts.length > 0 ? (
          filteredProducts.map(p => <ProductCard key={p.id} product={p} />)
        ) : (
          <p className="col-span-full text-center text-gray-400 mt-20">
            No products found.
          </p>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;
