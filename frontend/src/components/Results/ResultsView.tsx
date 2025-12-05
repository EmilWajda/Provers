import { FileText, ArrowLeft } from 'lucide-react';
import type { Result } from '../../types';

interface ResultsViewProps {
  results: Result[];
  activeResultId: string | null;
  onSelectResult: (id: string) => void;
  onBack: () => void;
}

const ResultsView = ({ results, activeResultId, onSelectResult, onBack }: ResultsViewProps) => {
  if (activeResultId) {
    const result = results.find(r => r.id === activeResultId);
    if (!result) return <div>Result not found.</div>;

    return (
      <div className="h-full flex flex-col p-8 animate-in slide-in-from-right duration-300">
        <button onClick={onBack} className="self-start mb-6 flex items-center gap-2 text-gray-500 hover:text-gray-800 transition-colors">
          <ArrowLeft size={20} /> Back to Results List
        </button>

        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
          <div className="flex items-center gap-4 mb-6 border-b pb-6">
            <div className="bg-blue-100 p-3 rounded-full">
              <FileText className="text-blue-600 w-8 h-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-800">Benchmark Report</h2>
              <p className="text-gray-500">{result.timestamp}</p>
            </div>
          </div>

          <div className="overflow-x-auto mb-8 border border-gray-200 rounded-lg shadow-sm max-h-[600px]">
            <table className="w-full text-left border-collapse">
              <thead className="bg-gray-50 text-gray-600 text-xs uppercase font-semibold sticky top-0 z-20 shadow-sm">
                <tr>
                  <th className="p-4 border-b border-gray-200 sticky left-0 bg-gray-50 z-30 border-r">Problem</th>
                  {result.provers.map(prover => (
                    <th key={prover} className="p-4 border-b border-gray-200 text-center min-w-[180px] border-r last:border-r-0">{prover}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {result.detailedResults?.map((row, idx) => (
                  <tr key={`${row.problemName}-${idx}`} className="hover:bg-gray-50">
                    <td className="p-4 font-medium text-gray-800 sticky left-0 bg-white border-r border-gray-200 z-10 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]">
                      {row.problemName}
                    </td>
                    {result.provers.map(prover => {
                      const metric = row.proverResults[prover];
                      return (
                        <td key={prover} className="p-3 text-sm border-r border-gray-100 last:border-r-0 align-top">
                          {metric ? (
                            <div className="space-y-1">
                              <div className="flex justify-between items-center">
                                <span className="text-gray-400 text-xs">Time:</span>
                                <span className="font-mono text-gray-700">{metric.time.toFixed(3)}s</span>
                              </div>
                              <div className="flex justify-between items-center">
                                <span className="text-gray-400 text-xs">Memory:</span>
                                <span className="font-mono text-gray-700">{metric.memory} KB</span>
                              </div>
                              <div className="flex justify-between items-center pt-1 border-t border-gray-50 mt-1">
                                <span className="text-gray-400 text-xs">Result:</span>
                                <span className={`font-bold text-xs px-1.5 py-0.5 rounded ${
                                  metric.status === 'SAT' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                }`}>
                                  {metric.status}
                                </span>
                              </div>
                            </div>
                          ) : (
                            <span className="text-gray-300 italic">N/A</span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="h-64 bg-gray-50 rounded-lg border border-gray-200 flex items-center justify-center text-gray-400">
            [charts]
          </div>
        </div>
      </div>
    );
  }

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
              {results.map(result => (
                <tr key={result.id} className="hover:bg-blue-50 transition-colors group">
                  <td className="px-6 py-4 font-medium text-gray-800">{result.timestamp}</td>
                  <td className="px-6 py-4 text-gray-600">
                    <div className="flex gap-1">
                      {result.provers.map(p => (
                        <span key={p} className="text-xs bg-gray-200 px-1.5 py-0.5 rounded">{p}</span>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-600">{result.problemCount}</td>
                  <td className="px-6 py-4 text-right">
                    <button onClick={() => onSelectResult(result.id)} className="text-blue-600 hover:text-blue-800 font-medium text-sm border border-blue-200 hover:border-blue-400 px-3 py-1.5 rounded transition-all bg-white hover:shadow-sm">
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

export default ResultsView;