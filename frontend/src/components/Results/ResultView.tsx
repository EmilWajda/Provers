import { ArrowLeft, FileText } from "lucide-react";
import { ResultSummary, type ResultCell } from "../../types";
import useWebSocket from "react-use-websocket";
import { useActiveWorkspace } from "../../hooks/useActiveWorkspace";
import { useEffect, useState } from "react";
import useProblems from "../../hooks/useProblems";
import useProblemTypes from "../../hooks/useProblemTypes";
import ResultCharts from "./ResultCharts";

const useWS = (useWebSocket as any).default as typeof useWebSocket; // A weird hack to fix import issues

type IncompleteSummary = {
  timestamp: string;
  provers: string[];
  problems: string[];
};

const resultStatusClassMap: { [key: string]: string } = {
  satisfiable: "bg-green-100 text-green-700",
  unsatisfiable: "bg-red-100 text-red-700",
  unknown: "bg-yellow-100 text-yellow-700",
  timeout: "bg-gray-100 text-gray-700",
  unconverted: "bg-yellow-100 text-yellow-700",
  ongoing: "bg-gray-50 text-gray-400",
};

const ResultView = ({ resultId, onBack }: { resultId: string; onBack: () => void }) => {
  const activeWorkspace = useActiveWorkspace().workspace;
  const [summary, setSummary] = useState<ResultSummary | null>(null);
  const [cells, setCells] = useState<ResultCell[]>([]);
  const { problems } = useProblems();
  const { problemTypes } = useProblemTypes();
  const { lastJsonMessage } = useWS<IncompleteSummary | ResultCell>(`/ws/workspaces/${activeWorkspace}/results`, {
    queryParams: { benchmark: resultId },
    shouldReconnect: (_event) => false,
  });

  const setOrUpdateCell = (newCell: ResultCell) => {
    setCells((prev) => {
      const existingIndex = prev.findIndex(
        (cell) => cell.problem === newCell.problem && cell.prover === newCell.prover,
      );
      if (existingIndex !== -1) {
        const updated = [...prev];
        updated[existingIndex] = newCell;
        return updated;
      } else {
        return [...prev, newCell];
      }
    });
  };

  useEffect(() => {
    if (!lastJsonMessage) return;
    if ("timestamp" in lastJsonMessage) {
      setSummary(new ResultSummary(lastJsonMessage.timestamp, lastJsonMessage.provers, lastJsonMessage.problems));
    } else {
      setOrUpdateCell(lastJsonMessage);
    }
  }, [lastJsonMessage]);

  if (!summary)
    return <div className="flex text-gray-400 items-center justify-center h-full text-lg">Loading result...</div>;

  return (
    <div className="h-full flex flex-col p-8 animate-in slide-in-from-right duration-300">
      <button
        onClick={onBack}
        className="self-start mb-6 flex items-center gap-2 text-gray-500 hover:text-gray-800 transition-colors"
      >
        <ArrowLeft size={20} /> Back to Results List
      </button>

      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
        <div className="flex items-center gap-4 mb-6 border-b pb-6">
          <div className="bg-blue-100 p-3 rounded-full">
            <FileText className="text-blue-600 w-8 h-8" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Benchmark Report</h2>
            <p className="text-gray-500">{summary.timestamp.toISOString()}</p>
          </div>
        </div>

        <div className="overflow-x-auto mb-8 border border-gray-200 rounded-lg shadow-sm max-h-[600px]">
          <table className="w-full text-left border-collapse">
            <thead className="bg-gray-50 text-gray-600 text-xs uppercase font-semibold sticky top-0 z-20 shadow-sm">
              <tr>
                <th className="p-4 border-b border-gray-200 sticky left-0 bg-gray-50 z-30 border-r">Problem</th>
                {summary.provers.map((prover) => (
                  <th
                    key={prover}
                    className="p-4 border-b border-gray-200 text-center min-w-[180px] border-r last:border-r-0"
                  >
                    {prover}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {summary.problems.map((problem) => (
                <tr key={problem} className="hover:bg-gray-50">
                  <td className="p-4 font-medium text-gray-800 sticky left-0 bg-white border-r border-gray-200 z-10 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]">
                    {problem}
                  </td>
                  {summary.provers.map((prover) => {
                    const cell = cells.find((c) => c.problem === problem && c.prover === prover);
                    if (!cell) {
                      return (
                        <td key={prover} className="p-3 text-sm border-r border-gray-100 last:border-r-0 align-top">
                          <span className="text-gray-300 italic">N/A</span>
                        </td>
                      );
                    }
                    const status = cell.result || "ongoing";
                    return (
                      <td
                        key={`${prover}-${problem}`}
                        className="p-3 text-sm border-r border-gray-100 last:border-r-0 align-top"
                      >
                        <div className="space-y-1">
                          <div className="flex justify-between items-center pt-1 border-t border-gray-50 mt-1">
                            <span className="text-gray-400 text-xs">Result:</span>
                            <span
                              className={`font-bold text-xs px-1.5 py-0.5 rounded-sm ${resultStatusClassMap[status]}`}
                            >
                              {status.toUpperCase()}
                            </span>
                          </div>
                          {cell.stats && (
                            <>
                              <div className="flex justify-between items-center">
                                <span className="text-gray-400 text-xs">Real Time:</span>
                                <span className="font-mono text-gray-700">{cell.stats.real_time.toFixed(2)} s</span>
                              </div>
                              <div className="flex justify-between items-center">
                                <span className="text-gray-400 text-xs">System Time:</span>
                                <span className="font-mono text-gray-700">{cell.stats.system_time.toFixed(2)} s</span>
                              </div>
                              <div className="flex justify-between items-center">
                                <span className="text-gray-400 text-xs">Memory:</span>
                                <span className="font-mono text-gray-700">{cell.stats.peak_memory} KB</span>
                              </div>
                            </>
                          )}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <ResultCharts cells={cells} provers={summary.provers} problems={problems} problemTypes={problemTypes} />
      </div>
    </div>
  );
};

export default ResultView;
