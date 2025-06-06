// src/App.tsx
import { useState, useEffect } from 'react';
import ImageUploader from './components/ImageUploader';
import ChatInterface from './components/ChatInterface';
import ProductCards from './components/ProductCards';
import type { Product } from './types/types';

function App() {
  const [productType, setProductType] = useState<string>('');
  const [questions, setQuestions] = useState<string[]>([]);
  const [preferences, setPreferences] = useState<{ [key: string]: string }>({});
  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState<boolean>(false);

  // Whenever productType updates, fetch new questions
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
      const data: { questions: string[] } = await res.json();
      setQuestions(data.questions);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred while generating questions.');
      }
    }
  };

  const fetchRecommendations = async () => {
    try {
      setHasSearched(true); // mark that we’ve attempted a search
      const res = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_type: productType, preferences }),
      });
      if (!res.ok) throw new Error('Failed to fetch recommendations.');
      const data: { recommendations: Product[] } = await res.json();
      setRecommendations(data.recommendations);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred while fetching recommendations.');
      }
    }
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

        {/* Image Uploader Card */}
        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm p-6 mb-8"
            style={{ margin: '0 auto', maxWidth: '576px' }}
        >
          <h2 className="text-2xl font-semibold text-gray-700 dark:text-gray-200 mb-4 text-center">
            Upload Product Image
          </h2>
          <ImageUploader
            setProductType={setProductType}
            setError={setError}
            fetchQuestions={fetchQuestions}
          />
        </div>

        {/* Chat Interface Card */}
        {questions.length > 0 && (
          <div
            className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm p-6 mb-8"
            style={{ margin: '0 auto', maxWidth: '576px' }}
          >
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
          <div className="text-center mb-8"
            style={{ margin: '0 auto', maxWidth: '576px' }}
          >
            <button
              onClick={fetchRecommendations}
              className="inline-flex items-center px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-md shadow-md transition-transform transform hover:-translate-y-1 active:translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              🎯 Get Recommendations
            </button>
          </div>
        )}

        {/* Recommendations Card */}
      {hasSearched && (
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)',
              margin: '0 auto',
              maxWidth: '576px',
              overflow: 'hidden',
            }}
          >
            {/* Header Bar */}
            <div
              style={{
                backgroundColor: '#FFA500',   // bold orange
                padding: '16px 20px',
              }}
            >
              <h2
                style={{
                  margin: 0,
                  color: 'black',          // white text
                  fontSize: '1.5rem',
                  fontWeight: 600,
                  textAlign: 'center',
                }}
              >
                Recommended Products
              </h2>
            </div>

            {/* Content Area */}
            <div style={{ padding: '20px', borderTop: '2px solid #FFD580' }}>
              {recommendations.length > 0 ? (
                <ProductCards products={recommendations} />
              ) : (
                <div style={{ textAlign: 'center', padding: '40px 0' }}>
                  <p style={{ color: '#555555', fontSize: '1rem' }}>
                    😕 No products found for the given preferences.
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
