// src/components/ChatInterface.tsx
import React, { useState, useEffect, useRef,  } from 'react';
import type {KeyboardEvent} from 'react';
interface ChatInterfaceProps {
  /** 
   * Array of questions (strings) from the “bot.” 
   * Once the user starts typing, each question and answer appears as a chat bubble.
   */
  questions: string[];

  /**
   * Called once all questions have been answered, passing
   * an object mapping each question → user answer.
   */
  onSubmit: (prefs: { [key: string]: string }) => void;
}

type Message = {
  sender: 'bot' | 'user';
  text: string;
};

const ChatInterface: React.FC<ChatInterfaceProps> = ({ questions, onSubmit }) => {
  // Holds the chat history of message objects ({ sender, text })
  const [messages, setMessages] = useState<Message[]>([]);

  // Index of which question the bot is currently on
  const [currentIndex, setCurrentIndex] = useState<number>(0);

  // Collected answers so far (question → answer)
  const [answers, setAnswers] = useState<{ [key: string]: string }>({});

  // Controlled input value for the user’s current answer
  const [inputValue, setInputValue] = useState<string>('');

  // Ref to scroll the last message into view
  const bottomRef = useRef<HTMLDivElement | null>(null);

  // Whenever the `questions` prop changes, reset the chat
  useEffect(() => {
    if (questions.length > 0) {
      // Start with the first bot question
      setMessages([{ sender: 'bot', text: questions[0] }]);
      setCurrentIndex(0);
      setAnswers({});
      setInputValue('');
    } else {
      // No questions → clear the chat
      setMessages([]);
    }
  }, [questions]);

  // Auto-scroll to the bottom whenever messages update
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Called when user clicks “Send” or presses Enter
  const sendAnswer = () => {
    const trimmed = inputValue.trim();
    if (!trimmed) return; // Don't send empty answers

    const currentQuestion = questions[currentIndex];

    // 1) Add the user’s answer bubble
    setMessages((prev) => [...prev, { sender: 'user', text: trimmed }]);

    // 2) Store the answer in our map
    setAnswers((prev) => ({ ...prev, [currentQuestion]: trimmed }));

    // Clear the input field
    setInputValue('');

    const next = currentIndex + 1;
    if (next < questions.length) {
      // 3) Show the next bot question after a small delay (for UX)
      setTimeout(() => {
        setMessages((prev) => [...prev, { sender: 'bot', text: questions[next] }]);
      }, 200);
      setCurrentIndex(next);
    } else {
      // 4) All questions answered → call onSubmit after a slight delay
      setTimeout(() => {
        onSubmit({ ...answers, [currentQuestion]: trimmed });
      }, 200);
    }
  };

  // Allow pressing Enter key to send the answer
  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendAnswer();
    }
  };

  return (
    <div className="flex flex-col h-[450px] w-full shadow-lg rounded-xl overflow-hidden">

      {/* ============================================= */}
      {/*       Scrollable Chat Messages Area           */}
      {/* ============================================= */}
      <div className="flex-1 p-4 space-y-4 overflow-y-auto bg-white dark:bg-gray-800">
        {messages.map((msg, idx) => (
          <div key={idx} className="flex">
            {msg.sender === 'bot' ? (
              // ── Bot message (left-aligned) ─────────────────────────
              <div className="max-w-[70%] bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 
                              rounded-tr-xl rounded-br-xl rounded-tl-xl px-4 py-3 shadow-sm animate-fadeIn">
                <p className="whitespace-pre-wrap">{msg.text}</p>
              </div>
            ) : (
              // ── User message (right-aligned) ──────────────────────
              <div className="ml-auto max-w-[70%] bg-blue-600 text-white 
                              rounded-tl-xl rounded-bl-xl rounded-tr-xl px-4 py-3 shadow-md animate-fadeIn">
                <p className="whitespace-pre-wrap">{msg.text}</p>
              </div>
            )}
          </div>
        ))}
        {/* Dummy div to scroll into view */}
        <div ref={bottomRef} />
      </div>

      {/* ============================================= */}
      {/*            Input Area (Bottom)                */}
      {/* ============================================= */}
      <div className="border-t border-gray-300 dark:border-gray-700 px-4 py-3 bg-gray-50 dark:bg-gray-900 flex items-center">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your answer..."
          className="flex-1 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 
                     rounded-full px-4 py-2 text-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={sendAnswer}
          className="ml-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full transition-transform 
                     active:scale-95 focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
