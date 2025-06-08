import { useState } from 'react';

export default function FeedbackForm() {
  const [feedback, setFeedback] = useState('');
  const [submitted, setSubmitted] = useState(false);
const API = import.meta.env.VITE_API_URL;

  const handleSubmit = async () => {
    await fetch(`${API}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feedback }),
    });
    setSubmitted(true);
  };

  return (
    <div className="bg-white dark:bg-gray-900 border rounded-lg shadow-sm p-6 mt-6">
      <h3 className="text-xl font-semibold mb-4 text-center">💬 Share Your Feedback</h3>
      <textarea
        className="w-full border p-2 rounded"
        rows={3}
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        placeholder="What did you think of the recommendations?"
      />
      <div className="text-center mt-4">
        <button
          onClick={handleSubmit}
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
          disabled={submitted}
        >
          {submitted ? '✅ Submitted!' : 'Submit Feedback'}
        </button>
      </div>
    </div>
  );
}
