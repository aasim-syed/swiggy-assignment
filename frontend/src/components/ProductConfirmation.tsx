import { useState } from 'react';
import type { Product } from '../types/types';

type Props = {
  products: Product[];
  onConfirm: (selected: Product | null) => void;
};

export default function ProductConfirmation({ products, onConfirm }: Props) {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  return (
    <div className="bg-white dark:bg-gray-900 border rounded-lg shadow-sm p-6 mb-6">
      <h3 className="text-xl font-semibold mb-4 text-center">🧐 Confirm a Product</h3>
      <ul className="space-y-2">
        {products.map((p, idx) => (
          <li
            key={p.id || idx}
            className={`p-3 border rounded cursor-pointer ${
              selectedIndex === idx ? 'bg-green-100 border-green-600' : 'hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
            onClick={() => setSelectedIndex(idx)}
          >
            <strong>{p.name}</strong> – ₹{p.price}
          </li>
        ))}
      </ul>

      <div className="text-center mt-4">
        <button
          onClick={() => onConfirm(selectedIndex !== null ? products[selectedIndex] : null)}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          ✅ Confirm Selection
        </button>
      </div>
    </div>
  );
}
