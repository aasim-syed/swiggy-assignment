type Props = {
  summary: string;
};

export default function SummaryView({ summary }: Props) {
  return (
    <div className="bg-yellow-50 dark:bg-yellow-900 border border-yellow-400 dark:border-yellow-300 p-4 mt-6 rounded">
      <h3 className="text-xl font-semibold mb-2 text-center">🧠 Session Summary</h3>
      <p className="text-gray-800 dark:text-white whitespace-pre-line">{summary}</p>
    </div>
  );
}
