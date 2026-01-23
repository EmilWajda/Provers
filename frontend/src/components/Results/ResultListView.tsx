import { FileText } from "lucide-react";
import type { Result } from "../../types";

const ResultListView = ({ onSelectResult }: { onSelectResult: (id: string) => void }) => {
  const results: Result[] = []; // TODO: fetch
  return (
    <div className="p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-8 flex items-center gap-3">
        <FileText className="text-blue-600 w-8 h-8" /> Results
      </h2>
      {results.length === 0 ? (
        <div className="text-center text-gray-400 mt-20">
          <div className="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <FileText size={32} />
          </div>
          <p>No benchmark results in this workspace.</p>
          <p className="text-sm">Go to the Benchmark tab and run tests.</p>
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-50 border-b border-gray-200 text-gray-500 uppercase text-xs">
              <tr>
                <th className="px-6 py-4 font-medium">Date / ID</th>
                <th className="px-6 py-4 font-medium">Provers</th>
                <th className="px-6 py-4 font-medium">Problems</th>
                <th className="px-6 py-4 font-medium text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {results.map((result) => (
                <tr key={result.id} className="hover:bg-blue-50 transition-colors group">
                  <td className="px-6 py-4 font-medium text-gray-800">{result.timestamp}</td>
                  <td className="px-6 py-4 text-gray-600">
                    <div className="flex gap-1">
                      {result.provers.map((p) => (
                        <span key={p} className="text-xs bg-gray-200 px-1.5 py-0.5 rounded">
                          {p}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-600">{result.problemCount}</td>
                  <td className="px-6 py-4 text-right">
                    <button
                      onClick={() => onSelectResult(result.id)}
                      className="text-blue-600 hover:text-blue-800 font-medium text-sm border border-blue-200 hover:border-blue-400 px-3 py-1.5 rounded transition-all bg-white hover:shadow-sm"
                    >
                      View Report
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ResultListView;
