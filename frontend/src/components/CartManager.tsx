// src/components/CartManager.tsx
import React from 'react';
import type { Product } from '../types/types';

interface Props {
  cart: Product[];
  onCheckout: () => void;
}

const CartManager: React.FC<Props> = ({ cart, onCheckout }) => {
  if (cart.length === 0) return null;

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  return (
    <div className="bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm p-6 mt-8 max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-4 text-center text-green-700 dark:text-green-300">🛒 Your Cart</h2>
      <ul className="space-y-2">
        {cart.map((item, index) => (
          <li key={index} className="text-gray-700 dark:text-gray-300">
            ✅ {item.name} - ₹{item.price}
          </li>
        ))}
      </ul>
      <div className="mt-4 text-right text-lg text-green-800 dark:text-green-200">
        <strong>Total:</strong> ₹{total}
      </div>
      <div className="mt-4 text-center">
        <button
          onClick={onCheckout}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-md shadow-md"
        >
          ✅ Proceed to Checkout
        </button>
      </div>
    </div>
  );
};

export default CartManager;
