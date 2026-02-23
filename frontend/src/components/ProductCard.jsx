export default function ProductCard({ product }) {
  return (
    <div className="bg-gray-800 rounded-2xl shadow-xl overflow-hidden hover:scale-105 transform transition duration-300">
      <img src={product.image} alt={product.name} className="w-full h-48 object-cover" />
      <div className="p-5">
        <h2 className="text-lg font-semibold mb-1">{product.name}</h2>
        <p className="text-2xl font-bold text-blue-400 mb-2">${product.price}</p>
        <p className="text-sm text-gray-400 mb-4">{product.store}</p>
        <a href={product.link} target="_blank" rel="noreferrer"
           className="block w-full text-center bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 rounded-lg transition">
          Buy Now →
        </a>
      </div>
    </div>
  );
}
