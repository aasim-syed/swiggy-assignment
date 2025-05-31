// src/components/ChatInterface.tsx
import { useState } from 'react';

const ChatInterface = ({
  questions,
  onSubmit
}: {
  questions: string[];
  onSubmit: (prefs: { [key: string]: string }) => void;
}) => {
  const [answers, setAnswers] = useState<{ [key: string]: string }>({});

  const handleChange = (q: string, val: string) => {
    setAnswers((prev) => ({ ...prev, [q]: val }));
  };

  const handleSubmit = () => {
    const unanswered = questions.find((q) => !answers[q]);
    if (unanswered) {
      alert(`Please answer: ${unanswered}`);
      return;
    }
    onSubmit(answers);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">💬 Please answer:</h2>
      {questions.map((q, idx) => (
        <div key={idx}>
          <label className="block font-medium mb-1">{q}</label>
          <input
            type="text"
            className="w-full border border-gray-300 rounded px-3 py-2"
            onChange={(e) => handleChange(q, e.target.value)}
          />
        </div>
      ))}
      <button
        onClick={handleSubmit}
        className="px-4 py-2 bg-purple-600 text-white rounded"
      >
        Submit Preferences
      </button>
    </div>
  );
};

export default ChatInterface;
