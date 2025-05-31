import type { Product } from "../types/types";
export const ProductCards = ({ products }: { products: Product[] }) => {
  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map((product, idx) => (
        <div
          key={idx}
          className="p-4 border rounded-lg shadow hover:shadow-md transition"
        >
          <h3 className="text-lg font-bold mb-1">{product.name}</h3>
          <p>Brand: {product.brand}</p>
          <p>Color: {product.color}</p>
          <p>Category: {product.category}</p>
          <p className="font-semibold">₹{product.price}</p>
        </div>
      ))}
    </div>
  );
};

export default ProductCards;
