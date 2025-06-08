type Props = {
  onFetchSimilar: () => void;
};

export default function SimilarPrompt({ onFetchSimilar }: Props) {
  return (
    <div className="text-center mt-6">
      <button
        onClick={onFetchSimilar}
        className="bg-orange-500 text-white px-4 py-2 rounded hover:bg-orange-600"
      >
        🔁 Show Similar Products
      </button>
    </div>
  );
}
