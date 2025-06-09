// src/components/FeedbackForm.tsx
import { useState,  } from 'react';
import type {CSSProperties} from 'react';
export default function FeedbackForm() {
  const [feedback, setFeedback] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const API = import.meta.env.VITE_API_URL;

  const handleSubmit = async () => {
    if (!feedback.trim()) return;
    try {
      await fetch(`${API}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feedback }),
      });
      setSubmitted(true);
    } catch {
      // optional: handle network/error feedback
    }
  };

  const containerStyle: CSSProperties = {
    maxWidth: '600px',
    margin: '0 auto',
    backgroundColor: '#fff',
    padding: '24px',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
  };

  const textareaStyle: CSSProperties = {
    width: '100%',
    minHeight: '100px',
    padding: '12px',
    borderRadius: '8px',
    border: '1px solid #D1D5DB',
    fontSize: '16px',
    resize: 'vertical',
  };

  const buttonBase: CSSProperties = {
    padding: '10px 24px',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: 500,
    cursor: submitted ? 'default' : 'pointer',
    transition: 'background-color 0.2s',
  };

  const submitBtn: CSSProperties = {
    ...buttonBase,
    backgroundColor: submitted ? '#10B981' : '#6B21A8',
    color: '#fff',
    border: 'none',
    marginRight: '12px',
  };

  const disabledStyle: CSSProperties = submitted
    ? { opacity: 0.7 }
    : {};

  return (
    <div style={containerStyle}>
      <h3
        style={{
          fontSize: '20px',
          fontWeight: 600,
          marginBottom: '16px',
          textAlign: 'center',
        }}
      >
        💬 Share Your Feedback
      </h3>
      <textarea
        style={textareaStyle}
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        placeholder="What did you think of the recommendations?"
        disabled={submitted}
      />
      <div style={{ textAlign: 'center', marginTop: '16px' }}>
        <button
          onClick={handleSubmit}
          style={{ ...submitBtn, ...disabledStyle }}
          disabled={submitted || feedback.trim() === ''}
        >
          {submitted ? '✅ Submitted!' : 'Submit Feedback'}
        </button>
      </div>
    </div>
  );
}
