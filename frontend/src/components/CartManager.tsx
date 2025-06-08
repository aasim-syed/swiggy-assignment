// src/components/CartManager.tsx
import type { CSSProperties } from 'react';
import type { Product } from '../types/types';

interface Props {
  cart: Product[];
  onCheckout: () => void;
}

export default function CartManager({ cart, onCheckout }: Props) {
  if (cart.length === 0) return null;

  // Inline styles matching Swiggy theme
  const containerStyle: CSSProperties = {
    maxWidth: '530px',
    margin: '0 auto',
    padding: '24px',
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
  };

  const headerStyle: CSSProperties = {
    fontSize: '24px',
    fontWeight: 700,
    color: '#fb641b',
    textAlign: 'center' as const,
    marginBottom: '16px',
  };

  const listStyle: CSSProperties = {
    marginBottom: '16px',
    listStyleType: 'none',
    padding: 0,
  };

  const listItemStyle: CSSProperties = {
    fontSize: '16px',
    color: '#333333',
    marginBottom: '8px',
    display: 'flex',
    justifyContent: 'space-between',
  };

  const totalStyle: CSSProperties = {
    fontSize: '18px',
    fontWeight: 600,
    color: '#333333',
    textAlign: 'right' as const,
    marginBottom: '20px',
  };

  const buttonStyle: CSSProperties = {
    display: 'block',
    margin: '0 auto',
    padding: '12px 32px',
    backgroundColor: '#fb641b',
    color: '#ffffff',
    border: 'none',
    borderRadius: '24px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  };

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  return (
    <div style={containerStyle}>
      <h2 style={headerStyle}>🛒 Your Cart</h2>
      <ul style={listStyle}>
        {cart.map((item, idx) => (
          <li key={idx} style={listItemStyle}>
            <span>{item.name}</span>
            <span>₹{item.price.toLocaleString()}</span>
          </li>
        ))}
      </ul>
      <div style={totalStyle}>
        <strong>Total:</strong> ₹{total.toLocaleString()}
      </div>
      <button style={buttonStyle} onClick={onCheckout}>
        Proceed to Checkout
      </button>
    </div>
  );
}
