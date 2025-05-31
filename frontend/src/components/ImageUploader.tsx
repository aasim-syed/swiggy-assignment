// src/components/ImageUploader.tsx
import React from 'react';

interface ImageUploaderProps {
  setProductType: (cat: string) => void;
  setError: (err: string | null) => void;
  fetchQuestions: () => void; // Function to generate questions immediately after image analysis
}

const ImageUploader: React.FC<ImageUploaderProps> = ({
  setProductType,
  setError,
  fetchQuestions,
}) => {
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/analyze-image', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error('Failed to analyze image.');

      const data = await res.json();

      // If the backend could not infer a category, prompt for manual entry
      if (!data.product_type) {
        const manual = prompt(
          "❓ We couldn't infer the product category. Please enter it manually (e.g., sneakers, electronics, books):"
        );
        if (manual) {
          setProductType(manual.toLowerCase());
          setError(null);
          // Automatically fetch questions once manual category is provided
          fetchQuestions();
        } else {
          setError('No category selected. Please try again.');
        }
        return;
      }

      // If backend inferred successfully, set product type and clear any previous errors
      setProductType(data.product_type);
      alert(`🧠 Category inferred: ${data.product_type}`);
      setError(null);

      // Immediately trigger question generation (no extra button needed)
      fetchQuestions();
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred.');
      }
    }
  };

  return (
    <div>
      <label className="block mb-2 font-semibold">Upload Product Image:</label>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange} // Automatically analyze & generate questions on upload
        className="block w-full text-sm text-gray-500 border border-gray-300 rounded cursor-pointer"
      />
    </div>
  );
};

export default ImageUploader;
