// src/App.tsx
import  { useState } from 'react';
import ImageUploader from './components/ImageUploader';
import ChatInterface from './components/ChatInterface';
import ProductCards from './components/ProductCards';

function App() {
  const [productType, setProductType] = useState<string>('');
  const [questions, setQuestions] = useState<string[]>([]);
  const [preferences, setPreferences] = useState<{ [key: string]: string }>({});
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchQuestions = async () => {
    try {
      const res = await fetch('http://localhost:8000/clarify-preferences', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_type: productType })
      });
      if (!res.ok) throw new Error('Failed to generate questions.');
      const data = await res.json();
      setQuestions(data.questions);
   } catch (err: unknown) {
  if (err instanceof Error) {
    setError(err.message);
  } else {
    setError('An unknown error occurred.');
  }
}

  };

  const fetchRecommendations = async () => {
    try {
      const res = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_type: productType, preferences })
      });
      if (!res.ok) throw new Error('Failed to fetch recommendations.');
      const data = await res.json();
      setRecommendations(data.recommendations);
    } catch (err: unknown){
  if (err instanceof Error) {
    setError(err.message);
  } else {
    setError('An unknown error occurred.');
  }
}

  };

  return (
    <div className="p-4 max-w-4xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-center">🛍️ AI Shopping Assistant</h1>

      {error && <div className="text-red-600 font-semibold">{error}</div>}

      <ImageUploader setProductType={setProductType} setError={setError} />

      {productType && !questions.length && (
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded"
          onClick={fetchQuestions}
        >
          Generate Questions
        </button>
      )}

      {questions.length > 0 && (
        <ChatInterface
          questions={questions}
          onSubmit={(prefs) => {
            setPreferences(prefs);
            setError(null);
          }}
        />
      )}

      {Object.keys(preferences).length > 0 && (
        <button
          className="px-4 py-2 bg-green-600 text-white rounded"
          onClick={fetchRecommendations}
        >
          Get Recommendations
        </button>
      )}

      {recommendations.length > 0 && (
        <ProductCards products={recommendations} />
      )}
    </div>
  );
}

export default App;
