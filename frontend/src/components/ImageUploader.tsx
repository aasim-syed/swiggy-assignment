// src/components/ImageUploader.tsx
import React, { useState, useRef, useCallback,  } from 'react';
import type { CSSProperties } from 'react';
import './ImageUploader.css';

interface ImageUploaderProps {
  setProductType: (cat: string) => void;
  setError: (err: string | null) => void;
  fetchQuestions: () => void;
}

const ImageUploader: React.FC<ImageUploaderProps> = ({
  setProductType,
  setError,
  fetchQuestions,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [manualInput, setManualInput] = useState('');
  const [modalError, setModalError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const API = import.meta.env.VITE_API_URL;

  const handleFile = useCallback(
    async (file: File) => {
      const objectUrl = URL.createObjectURL(file);
      setPreview(objectUrl);
      setError(null);

      const formData = new FormData();
      formData.append('file', file);

      try {
        const res = await fetch(`${API}/analyze-image`, {
          method: 'POST',
          body: formData,
        });
        if (!res.ok) throw new Error('Failed to analyze image.');

        const data = await res.json();

        if (!data.product_type) {
          setModalError(null);
          setShowModal(true);
          return;
        }

        setProductType(data.product_type);
        setError(null);
        fetchQuestions();
      } catch (err: unknown) {
        URL.revokeObjectURL(objectUrl);
        setPreview(null);
        if (err instanceof Error) setError(err.message);
        else setError('An unknown error occurred.');
      }
    },
    [API, fetchQuestions, setError, setProductType]
  );

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };

  const removePreview = () => {
    if (preview) URL.revokeObjectURL(preview);
    setPreview(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
    setError(null);
  };

  const submitManual = () => {
    if (manualInput.trim()) {
      setProductType(manualInput.trim().toLowerCase());
      setError(null);
      fetchQuestions();
      setManualInput('');
      setModalError(null);
      setShowModal(false);
    } else {
      setModalError('Please enter a category.');
    }
  };

  // Inline styles
  const overlayStyle: CSSProperties = {
    position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
    backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex',
    alignItems: 'center', justifyContent: 'center', zIndex: 1000,
  };

  const modalStyle: CSSProperties = {
    backgroundColor: '#fff', padding: '24px', borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)', maxWidth: '400px', width: '90%',
    display: 'flex', flexDirection: 'column', alignItems: 'center',
  };

  const inputStyle: CSSProperties = {
    width: '90%', padding: '12px', borderRadius: '8px', border: '1px solid #ccc',
    marginBottom: '8px', fontSize: '16px',
  };

  const errorTextStyle: CSSProperties = {
    color: '#dc2626', marginBottom: '12px', fontSize: '14px', textAlign: 'left', width: '90%',
  };

  const dropZoneStyle: CSSProperties = {
    display: 'flex', flexDirection: 'column', alignItems: 'center',
    justifyContent: 'center', padding: '40px', border: '2px dashed #ccc',
    borderRadius: '12px', cursor: 'pointer', transition: 'border-color 0.3s',
  };

  const cloudIconStyle: CSSProperties = {
    width: '48px', height: '48px', marginBottom: '16px', color: '#555',
  };

  return (
    <div className="uploader-container">
      <label className="uploader-label">Upload Product Image:</label>
      <div
        className={`drop-zone${isDragging ? ' drag-over' : ''}`}
        style={dropZoneStyle}
        onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={e => { e.preventDefault(); setIsDragging(false); }}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          type="file"
          accept="image/*"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        {/* Cloud upload icon */}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          strokeLinecap="round"
          strokeLinejoin="round"
          style={cloudIconStyle}
        >
          <path d="M3 15a4 4 0 014-4h1a5 5 0 0110 0h1a4 4 0 010 8H7a4 4 0 01-4-4z" />
          <polyline points="8 15 12 11 16 15" />
          <line x1="12" y1="11" x2="12" y2="21" />
        </svg>
        <div className="drop-zone-text" style={{ textAlign: 'center', fontSize: '16px', color: '#555' }}>
          {isDragging ? 'Drop image here' : 'Drag & drop an image, or click to select'}
        </div>
        <div className="drop-zone-subtext" style={{ marginTop: '8px', fontSize: '14px', color: '#777' }}>
          (Supports JPEG, PNG, GIF, etc.)
        </div>
      </div>

      {preview && (
        <div className="preview-wrapper" style={{ marginTop: '16px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <img src={preview} alt="Preview" className="image-preview" style={{ maxWidth: '100%', borderRadius: '8px' }} />
          <button
            type="button"
            onClick={removePreview}
            style={{
              marginTop: '12px', padding: '10px 20px', backgroundColor: '#fc8019',
              color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer',
            }}
          >
            Remove Image
          </button>
        </div>
      )}

      {showModal && (
        <div style={overlayStyle}>
          <div style={modalStyle}>
            <h2 style={{ margin: 0, marginBottom: '16px', fontSize: '20px', textAlign: 'center' }}>
              Enter Product Category
            </h2>
            <input
              type="text"
              value={manualInput}
              onChange={e => setManualInput(e.target.value)}
              placeholder="e.g., sneakers, electronics"
              style={inputStyle}
            />
            {modalError && <p style={errorTextStyle}>{modalError}</p>}
            <div style={{ textAlign: 'right', width: '90%' }}>
              <button
                onClick={submitManual}
                style={{ padding: '10px 20px', backgroundColor: '#4f46e5', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', marginRight: '8px' }}
              >
                Submit
              </button>
              <button
                onClick={() => { setShowModal(false); setModalError(null); }}
                style={{ padding: '10px 20px', backgroundColor: '#e5e7eb', color: '#374151', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
