// src/types.ts
export interface Product {
  id: string;
  name: string;
  price: number;
  brand: string;
  color: string;
  // Add any other fields the backend returns, e.g.:
  // imageUrl?: string;
  category?: string;
}
