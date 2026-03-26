import { FileText, Trash2, Pencil, CircleQuestionMark  } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { createPortal } from "react-dom";
import { ResultSummary } from "../../types";
import { useQuery } from "@tanstack/react-query";
import { useActiveWorkspace } from "../../hooks/useActiveWorkspace";
import axios from "axios";
import useMutationNotify from "../../hooks/useMutationNotify";

const ProblemTooltip = ({ problems }: { problems: string[] }) => {
  const [visible, setVisible] = useState(false);
  const [pos, setPos] = useState({ top: 0, left: 0 });
  const iconRef = useRef<HTMLDivElement | null>(null);
  const tooltipRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!visible || !iconRef.current) return;
    const rect = iconRef.current.getBoundingClientRect();
    // place the tooltip directly below the icon (align left to icon)
    let left = rect.left;
    let top = rect.bottom + 8;
    setPos({ top, left });

    // adjust after tooltip mounts so we can avoid viewport overflow
    const t = setTimeout(() => {
      const tt = tooltipRef.current?.getBoundingClientRect();
      if (!tt) return;
      // if bottom overflows, place above the icon
      if (top + tt.height > window.innerHeight - 8) {
        top = rect.top - tt.height - 8;
      }
      // if right edge overflows, shift left so it fits
      if (left + tt.width > window.innerWidth - 8) {
        left = Math.max(8, window.innerWidth - tt.width - 8);
      }
      // ensure tooltip doesn't start off-screen on the left
      if (left < 8) left = 8;
      setPos({ top, left });
    }, 0);

    const onResize = () => setVisible(false);
    window.addEventListener("resize", onResize);
    return () => {
      clearTimeout(t);
      window.removeEventListener("resize", onResize);
    };
  }, [visible]);

  return (
    <div
      ref={iconRef}
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
      className="inline-block p-1 cursor-help"
    >
      <CircleQuestionMark className="w-4 h-4 text-gray-400" />
      {visible &&
        createPortal(
          <div
            ref={tooltipRef}
            style={{ position: "fixed", top: pos.top, left: pos.left }}
            className="z-50 max-w-[60vw] bg-white border border-gray-200 rounded shadow-lg p-3 text-sm text-gray-700"
          >
            <div className="font-medium text-gray-800 mb-2">Problem Paths</div>
            <ul className="list-disc list-inside overflow-auto">
              {problems && problems.length > 0 ? (
                problems.map((p: string, idx: number) => (
                  <li key={idx} className="py-0.5">
                    {p}
                  </li>
                ))
              ) : (
                <li className="text-gray-500">No details available</li>
              )}
            </ul>
          </div>,
          document.body,
        )}
    </div>
  );
};

const ResultListView = ({ onSelectResult }: { onSelectResult: (id: string) => void }) => {
  const activeWorkspace = useActiveWorkspace().workspace;
  const { data } = useQuery({
    queryKey: ["results", activeWorkspace],
    queryFn: async (): Promise<ResultSummary[]> => {
      const response = await axios.get(`/api/workspaces/${activeWorkspace}/results`);
      const { done, ongoing } = response.data;
      const doneMapped = Object.entries(done).map(
        ([filePath, summary]: [string, any]) =>
          new ResultSummary(summary.timestamp, summary.provers, summary.problems, filePath),
      );
      const ongoingMapped = ongoing.map(
        (summary: any) => new ResultSummary(summary.timestamp, summary.provers, summary.problems, null),
      );
      return [...doneMapped, ...ongoingMapped].sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
    },
  });
  const deleteReport = useMutationNotify({
    mutationFn: async (id: string) => {
      if (!activeWorkspace) throw new Error("No active workspace");
      await axios.delete(`/api/workspaces/${activeWorkspace}/results`, { data: { id } });
    },
    queryKey: ["results", activeWorkspace],
    successMessage: "Report deleted successfully",
  });
  const renameReport = useMutationNotify({
    mutationFn: async ({ id, newName }: { id: string; newName: string }) => {
      if (!activeWorkspace) throw new Error("No active workspace");
      await axios.put(`/api/workspaces/${activeWorkspace}/results`, { id, newName });
    },
    queryKey: ["results", activeWorkspace],
    successMessage: "Report renamed successfully",
  });
  return (
    <div className="p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-8 flex items-center gap-3">
        <FileText className="text-blue-600 w-8 h-8" /> Results
      </h2>
      {!data || data.length === 0 ? (
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
                <th className="px-6 py-4 font-medium">Date / File Path</th>
                <th className="px-6 py-4 font-medium">Provers</th>
                <th className="px-6 py-4 font-medium">Problems</th>
                <th className="px-6 py-4 font-medium text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {data.map((result) => (
                <tr key={result.id} className="hover:bg-blue-50 transition-colors group">
                  <td className="px-6 py-4 font-medium text-gray-800">
                    <div className="flex flex-col gap-2">
                      <p>{result.timestamp.toLocaleString()}</p>
                      <p className={`text-sm ${result.filePath ? "text-gray-400" : "text-green-400"}`}>
                        {result.filePath ? `${result.filePath}.json` : "Ongoing..."}
                      </p>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-600">
                    <div className="flex gap-1">
                      {result.provers.map((p) => (
                        <span key={p} className="text-xs bg-gray-200 px-1.5 py-0.5 rounded">
                          {p}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-600 font-semibold">
                    <div className="flex gap-2 items-center">
                      <p>{result.problems.length}</p>
                      <ProblemTooltip problems={result.problems} />
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="inline-flex items-center justify-end">
                      <button
                        onClick={() => onSelectResult(result.id)}
                        className="text-blue-600 hover:text-blue-800 font-medium text-sm border border-blue-200 hover:border-blue-400 px-3 py-1.5 rounded transition-all bg-white hover:shadow-sm"
                      >
                        View Report
                      </button>
                      {result.filePath && (
                        <>
                          <button
                            onClick={() => {
                              const newName = prompt(`Enter new name for report ${result.id}:`, result.id);
                              if (newName !== null) {
                                const trimmed = newName.trim();
                                if (trimmed === "" || trimmed.replace(/\./g, "") === "") {
                                  alert("Invalid name.");
                                  return;
                                }
                                if (trimmed !== result.id) {
                                  renameReport({ id: result.id, newName: trimmed });
                                }
                              }
                            }}
                            title="Rename Report"
                            className="ml-3 text-blue-500 hover:text-blue-700 px-3 py-1.5 rounded text-sm border border-blue-100 hover:border-blue-200 transition-all bg-white hover:shadow-sm"
                          >
                            <Pencil size={16} />
                          </button>
                          <button
                            onClick={() => deleteReport(result.id)}
                            title="Delete Report"
                            className="ml-3 text-red-500 hover:text-red-700 px-3 py-1.5 rounded text-sm border border-red-100 hover:border-red-200 transition-all bg-white hover:shadow-sm"
                          >
                            <Trash2 size={16} />
                          </button>
                        </>
                      )}
                    </div>
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
