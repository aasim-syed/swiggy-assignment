// src/components/ImageUploader.tsx
import React, { useState, useRef, useCallback } from 'react';
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
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // Shared logic for handling a File (dropped or selected)
  const handleFile = useCallback(
    async (file: File) => {
      // Create a preview URL immediately
      const objectUrl = URL.createObjectURL(file);
      setPreview(objectUrl);
      setError(null);

      const formData = new FormData();
      formData.append('file', file);

      try {
        const res = await fetch('http://localhost:8000/analyze-image', {
          method: 'POST',
          body: formData,
        });
        if (!res.ok) throw new Error('Failed to analyze image.');

        const data = await res.json();

        // If no category inferred, prompt manually
        if (!data.product_type) {
          const manual = prompt(
            "❓ We couldn't infer the product category. Please enter it manually (e.g., sneakers, electronics, books):"
          );
          if (manual) {
            setProductType(manual.toLowerCase());
            setError(null);
            fetchQuestions();
          } else {
            setError('No category selected. Please try again.');
          }
          return;
        }

        // Otherwise, use inferred category
        setProductType(data.product_type);
        alert(`🧠 Category inferred: ${data.product_type}`);
        setError(null);
        fetchQuestions();
      } catch (err: unknown) {
        // On error, revoke preview and clear state
        URL.revokeObjectURL(objectUrl);
        setPreview(null);

        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('An unknown error occurred.');
        }
      }
    },
    [fetchQuestions, setError, setProductType]
  );

  // Called when the hidden file input changes
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  // Called on drop
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  // Remove the preview, allowing a new selection
  const removePreview = () => {
    if (preview) {
      URL.revokeObjectURL(preview);
      setPreview(null);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    setError(null);
  };

  return (
    <div className="uploader-container">
      <label className="uploader-label">Upload Product Image:</label>

      <div
        className={`drop-zone${isDragging ? ' drag-over' : ''}`}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={(e) => {
          e.preventDefault();
          setIsDragging(false);
        }}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          type="file"
          accept="image/*"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="file-input"
        />
        <div className="drop-zone-text">
          {isDragging ? 'Drop image here' : 'Drag & drop an image, or click to select'}
        </div>
        <div className="drop-zone-subtext">
          (Supports JPEG, PNG, GIF, etc.)
        </div>
      </div>

      {preview && (
        <div className="preview-wrapper">
          <div className="image-preview-container">
            <img src={preview} alt="Preview" className="image-preview" />
          </div>
          <button type="button" onClick={removePreview} className="remove-button">
            Remove Image
          </button>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;