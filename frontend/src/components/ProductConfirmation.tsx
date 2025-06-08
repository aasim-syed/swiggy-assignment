// src/components/ProductConfirmation.tsx
import { useState,  } from 'react';
import type {CSSProperties} from 'react';
import type { Product } from '../types/types';

type Props = {
  products: Product[];
  onConfirm: (selected: Product | null) => void;
};

export default function ProductConfirmation({ products, onConfirm }: Props) {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  // Inline styles
  const containerStyle: CSSProperties = {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '24px',
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
  };

  const cardStyle = (isSelected: boolean): CSSProperties => ({
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '16px',
    borderRadius: '8px',
    border: isSelected ? '2px solid #fb641b' : '1px solid #e0e0e0',
    backgroundColor: isSelected ? '#fff4f1' : '#ffffff',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
    boxShadow: isSelected ? 'inset 0 1px 3px rgba(0,0,0,0.1)' : '0 1px 3px rgba(0,0,0,0.08)',
    marginBottom: '12px',
  });

  const buttonStyle: CSSProperties = {
    padding: '12px 32px',
    backgroundColor: selectedIndex !== null ? '#fb641b' : '#cccccc',
    color: '#ffffff',
    border: 'none',
    borderRadius: '24px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: selectedIndex !== null ? 'pointer' : 'not-allowed',
    opacity: selectedIndex !== null ? 1 : 0.6,
    transition: 'background-color 0.2s',
  };

  return (
    <div style={containerStyle}>
      <h2 style={{ textAlign: 'center', fontSize: '24px', marginBottom: '16px', fontWeight: 700, color: '#fb641b' }}>
        🧐 Confirm Your Product
      </h2>
      <div>
        {products.map((p, idx) => {
          const isSelected = idx === selectedIndex;
          return (
            <div
              key={p.id ?? idx}
              style={cardStyle(isSelected)}
              onClick={() => setSelectedIndex(idx)}
              onMouseEnter={e => { (e.currentTarget.style.transform = 'scale(1.02)'); }}
              onMouseLeave={e => { (e.currentTarget.style.transform = 'scale(1)'); }}
            >
              <div>
                <div style={{ fontSize: '18px', fontWeight: 500, color: '#333' }}>{p.name}</div>
                <div style={{ fontSize: '14px', color: '#666', marginTop: '4px' }}>₹{p.price.toLocaleString()}</div>
              </div>
              <input
                type="checkbox"
                checked={isSelected}
                onChange={() => setSelectedIndex(idx)}
                style={{ width: '20px', height: '20px', accentColor: '#fb641b' }}
              />
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <button
          style={buttonStyle}
          disabled={selectedIndex === null}
          onClick={() => onConfirm(selectedIndex !== null ? products[selectedIndex] : null)}
        >
          Confirm Selection
        </button>
      </div>
    </div>
  );
}
