// src/App.tsx
import { useState, useEffect } from 'react';
import ImageUploader from './components/ImageUploader';
import ChatInterface from './components/ChatInterface';
import ProductConfirmation from './components/ProductConfirmation';
import FeedbackForm from './components/FeedbackFrom';
import type { Product } from './types/types';

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

  useEffect(() => {
    if (productType) {
      fetchQuestions();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [productType]);

  const fetchQuestions = async () => {
    try {
      const res = await fetch('http://localhost:8000/clarify-preferences', {
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
      const res = await fetch('http://localhost:8000/recommend', {
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
      const res = await fetch('http://localhost:8000/summarize', {
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

  const clearCart = () => {
    setCart([]);
    setSessionSummary('');
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
          <div style={{ margin: '0 auto', maxWidth: '576px' }} className="text-center mb-8">
            <p className="text-lg font-semibold text-green-600 mb-2">
              ✅ Confirmed: {confirmedProduct.name}
            </p>
            <button onClick={addToCart} className="px-4 py-2 bg-blue-600 text-white rounded-md mr-2">
              Add to Cart
            </button>
            <button onClick={() => setConfirmedProduct(null)} className="px-4 py-2 bg-gray-300 rounded-md">
              Refine
            </button>
          </div>
        )}

        {/* Cart Summary */}
        {cart.length > 0 && (
          <div style={{ margin: '0 auto', maxWidth: '576px' }} className="bg-white dark:bg-gray-900 p-6 rounded shadow mb-8">
            <h2 className="text-xl font-semibold mb-4 text-center">
              🛒 Cart
            </h2>
            <ul className="list-disc list-inside mb-4">
              {cart.map((item, idx) => (
                <li key={idx}>{item.name} — ₹{item.price}</li>
              ))}
            </ul>
            <div className="flex justify-center space-x-4">
              <button onClick={fetchSummary} className="px-4 py-2 bg-purple-600 text-white rounded-md">
                Summarize
              </button>
              <button onClick={clearCart} className="px-4 py-2 bg-red-500 text-white rounded-md">
                Clear Cart
              </button>
            </div>
          </div>
        )}

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
