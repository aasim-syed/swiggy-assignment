// src/components/ChatInterface.tsx
import React, { useState, useEffect, useRef } from 'react';
import type { KeyboardEvent } from 'react';

interface ChatInterfaceProps {
  questions: string[];
  onSubmit: (prefs: { [key: string]: string }) => void;
}

type Message = {
  sender: 'bot' | 'user';
  text: string;
};

const ChatInterface: React.FC<ChatInterfaceProps> = ({ questions, onSubmit }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [answers, setAnswers] = useState<{ [key: string]: string }>({});
  const [inputValue, setInputValue] = useState<string>('');
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (questions.length > 0) {
      setMessages([{ sender: 'bot', text: questions[0] }]);
      setCurrentIndex(0);
      setAnswers({});
      setInputValue('');
    } else {
      setMessages([]);
    }
  }, [questions]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendAnswer = () => {
    const trimmed = inputValue.trim();
    if (!trimmed) return;

    const currentQuestion = questions[currentIndex];
    setMessages(prev => [...prev, { sender: 'user', text: trimmed }]);
    setAnswers(prev => ({ ...prev, [currentQuestion]: trimmed }));
    setInputValue('');

    const next = currentIndex + 1;
    if (next < questions.length) {
      setTimeout(() => {
        setMessages(prev => [...prev, { sender: 'bot', text: questions[next] }]);
      }, 200);
      setCurrentIndex(next);
    } else {
      setTimeout(() => {
        onSubmit({ ...answers, [currentQuestion]: trimmed });
      }, 200);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendAnswer();
    }
  };

  // Inline styles for the two bubble types
  const botBubbleStyle: React.CSSProperties = {
    maxWidth: '70%',
    backgroundColor: '#F3F4F6',           // light gray
    color: '#1F2937',                     // dark text
    borderRadius: '16px 16px 16px 4px',   // rounded except bottom-left subtly
    padding: '12px 16px',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    marginBottom: '8px',
  };

  const userBubbleStyle: React.CSSProperties = {
    maxWidth: '70%',
    backgroundColor: '#f39044',           // blue-600
    color: '#FFFFFF',
    borderRadius: '16px 16px 4px 16px',   // rounded except top-left subtly
    padding: '12px 16px',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.15)',
    marginBottom: '8px',
    marginLeft: 'auto',
  };

  return (
    <div className="flex flex-col h-[450px] w-full max-w-xl mx-auto shadow-lg rounded-xl overflow-hidden">
      {/* Scrollable Chat Area */}
      <div className="flex-1 p-4 overflow-y-auto bg-white dark:bg-gray-800">
        {messages.map((msg, idx) => (
          <div key={idx} style={{ display: 'flex' }}>
            {msg.sender === 'bot' ? (
              <div style={botBubbleStyle}>
                <p style={{ margin: 0, whiteSpace: 'pre-wrap' }}>{msg.text}</p>
              </div>
            ) : (
              <div style={userBubbleStyle}>
                <p style={{ margin: 0, whiteSpace: 'pre-wrap' }}>{msg.text}</p>
              </div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div
        style={{
          borderTop: '1px solid #D1D5DB',
          backgroundColor: '#F9FAFB',
          padding: '12px 16px',
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <input
          type="text"
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your answer..."
          style={{
            flex: 1,
            padding: '10px 16px',
            borderRadius: '9999px',
            border: '1px solid #CCC',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
            backgroundColor: '#FFFFFF',
            fontSize: '1rem',
            color: '#1F2937',
            outline: 'none',
          }}
        />
        <button
          onClick={sendAnswer}
          style={{
            marginLeft: '12px',
            padding: '8px 20px',
            borderRadius: '9999px',
            backgroundColor: '#2563EB',
            color: '#FFFFFF',
            border: 'none',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.15)',
            fontSize: '1rem',
            cursor: 'pointer',
            transition: 'transform 0.1s ease-in-out, background-color 0.2s ease-in-out',
          }}
          onMouseEnter={e => {
            (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#f39044';
          }}
          onMouseLeave={e => {
            (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#f18010';
          }}
          onMouseDown={e => {
            (e.currentTarget as HTMLButtonElement).style.transform = 'scale(0.95)';
          }}
          onMouseUp={e => {
            (e.currentTarget as HTMLButtonElement).style.transform = 'scale(1)';
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
