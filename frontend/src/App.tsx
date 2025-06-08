// src/App.tsx
import { useState, useEffect } from 'react';
import ImageUploader from './components/ImageUploader';
import ChatInterface from './components/ChatInterface';
import ProductConfirmation from './components/ProductConfirmation';
import FeedbackForm from './components/FeedbackFrom';
import type { Product } from './types/types';
import CartManager from './components/CartManager';
import type { CSSProperties } from 'react';
function App() {
  const [productType, setProductType] = useState<string>('');
  const [questions, setQuestions] = useState<string[]>([]);
  const [preferences, setPreferences] = useState<{ [key: string]: string }>({});
  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [confirmedProduct, setConfirmedProduct] = useState<Product | null>(null);
  const [cart, setCart] = useState<Product[]>([]);
  const [sessionSummary, setSessionSummary] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState<boolean>(false);
const API = import.meta.env.VITE_API_URL;
console.log("API")
console.log(API)
  useEffect(() => {
    if (productType) {
      fetchQuestions();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [productType]);

  const fetchQuestions = async () => {
    try {
      const res = await fetch( `${API}/clarify-preferences`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_type: productType }),
      });
      if (!res.ok) throw new Error('Failed to generate questions.');
      const data: { question_text: string; key: string }[] = await res.json();
      setQuestions(data.map(q => q.question_text));
    } catch (err) {
      setError('An unknown error occurred while generating questions.');
    }
  };

  const fetchRecommendations = async () => {
    try {
      setHasSearched(true);
      const res = await fetch(`${API}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_type: productType, preferences }),
      });
      if (!res.ok) throw new Error('Failed to fetch recommendations.');
      const data = await res.json();
      setRecommendations(data.recommendations || []);
      setConfirmedProduct(null);
    } catch (err) {
      setError('An unknown error occurred while fetching recommendations.');
    }
  };

  const fetchSummary = async () => {
    try {
      const res = await fetch(`${API}/summarize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_type: productType,
          preferences,
          recommendations,
          cart,
        }),
      });
      if (!res.ok) throw new Error('Failed to fetch summary.');
      const data = await res.json();
      setSessionSummary(data.summary || '');
    } catch {
      setError('An unknown error occurred while summarizing session.');
    }
  };

  const confirmProduct = (product: Product | null) => {
    setConfirmedProduct(product);
  };

  const addToCart = () => {
    if (confirmedProduct) {
      setCart(prev => [...prev, confirmedProduct]);
      setConfirmedProduct(null);
    }
  };


  // Inline styles for confirmed-product block
  const confirmedContainerStyle: CSSProperties = {
    maxWidth: '530px',
    margin: '0 auto',
    padding: '24px',
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
    textAlign: 'center' as const,
  };
  const confirmedTextStyle: CSSProperties = {
    fontSize: '20px',
    fontWeight: 600,
    color: '#333333',
    marginBottom: '16px',
  };
  const buttonGroupStyle: CSSProperties = {
    display: 'flex',
    justifyContent: 'center',
    gap: '16px',
  };
  const primaryButtonStyle: CSSProperties = {
    padding: '12px 32px',
    backgroundColor: '#fb641b',
    color: '#ffffff',
    border: 'none',
    borderRadius: '24px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
  };
  const secondaryButtonStyle: CSSProperties = {
    padding: '12px 32px',
    backgroundColor: '#e0e0e0',
    color: '#333333',
    border: 'none',
    borderRadius: '24px',
    fontSize: '16px',
    cursor: 'pointer',
  };


  return (
    <div className="min-h-screen flex justify-center bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-900 dark:to-gray-800 py-10">
      <div className="w-full max-w-3xl px-6">
        {/* Header */}
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-800 dark:text-gray-100">
            🛍️ AI Shopping Assistant
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-300">
            Upload an image, answer a few quick questions, and get tailored product recommendations!
          </p>
        </header>

        {/* Error Banner */}
        {error && (
          <div className="mb-6 bg-red-50 dark:bg-red-900 border-l-4 border-red-500 dark:border-red-300 p-4 rounded-md">
            <p className="text-red-700 dark:text-red-200">{error}</p>
          </div>
        )}

        {/* Image Uploader */}
        <div style={{ margin: '0 auto', maxWidth: '576px' }} className="bg-white dark:bg-gray-900 border rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-700 dark:text-gray-200 mb-4 text-center">
            Upload Product Image
          </h2>
          <ImageUploader setProductType={setProductType} setError={setError} fetchQuestions={fetchQuestions} />
        </div>

        {/* Clarification Questions */}
        {questions.length > 0 && (
          <div style={{ margin: '0 auto', maxWidth: '576px' }} className="bg-white dark:bg-gray-900 border rounded-lg shadow-sm p-6 mb-8">
            <h2 className="text-2xl font-semibold text-gray-700 dark:text-gray-200 mb-4 text-center">
              Answer a Few Questions
            </h2>
            <ChatInterface
              questions={questions}
              onSubmit={(prefs) => {
                setPreferences(prefs);
                setError(null);
                setRecommendations([]);
                setHasSearched(false);
              }}
            />
          </div>
        )}

        {/* Get Recommendations Button */}
        {Object.keys(preferences).length > 0 && (
          <div style={{ margin: '0 auto', maxWidth: '576px' }} className="text-center mb-8">
            <button
              onClick={fetchRecommendations}
              className="inline-flex items-center px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-md shadow-md"
            >
              🎯 Get Recommendations
            </button>
          </div>
        )}

        {/* Product Confirmation */}
        {hasSearched && recommendations.length > 0 && !confirmedProduct && (
          <div style={{ margin: '0 auto', maxWidth: '576px' }}>
            <ProductConfirmation products={recommendations} onConfirm={confirmProduct} />
          </div>
        )}

        {/* Confirmed Product Actions */}
{confirmedProduct && (
          <div style={confirmedContainerStyle}>
            <p style={confirmedTextStyle}>
              🛒 Added to Cart: {confirmedProduct.name}
            </p>
            <div style={buttonGroupStyle}>
              <button style={primaryButtonStyle} onClick={addToCart}>
                Proceed to Checkout
              </button>
              <button style={secondaryButtonStyle} onClick={() => setConfirmedProduct(null)}>
                Continue Shopping
              </button>
            </div>
          </div>
        )}

        {/* Cart Summary */}
 <CartManager cart={cart} onCheckout={fetchSummary} />

        {/* Session Summary */}
        {sessionSummary && (
          <div style={{ margin: '0 auto', maxWidth: '576px' }} className="bg-yellow-100 p-4 rounded-md mb-8">
            <h3 className="font-semibold mb-2">🧾 Summary</h3>
            <p>{sessionSummary}</p>
          </div>
        )}

        {/* Feedback Form */}
        {hasSearched && !sessionSummary && (
          <div style={{ margin: '0 auto', maxWidth: '576px' }}>
            <FeedbackForm />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
