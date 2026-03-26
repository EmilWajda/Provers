import { Trash2, Pencil } from "lucide-react";
import type { ProblemFileList } from "../../types";
import { groupProblems, PrettyPrintParams } from "../../utils";

interface ProblemListProps {
  problems: ProblemFileList;
  onDeleteProblem: (path: string) => void;
  onRenameProblem: (path: string, newName: string) => void;
}

const ProblemList = ({ problems, onDeleteProblem, onRenameProblem }: ProblemListProps) => {
  const groupedProblems = groupProblems(problems);

  if (Object.keys(groupedProblems).length === 0) {
    return (
      <div className="flex-1 overflow-y-auto flex items-center justify-center text-gray-400">
        No problems generated yet.
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto space-y-6">
      {Object.entries(groupedProblems).map(([type, typeProblems]) => (
        <div key={type} className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
          <div className="bg-gray-50 p-3 border-b border-gray-200 font-semibold text-gray-700">
            {type} <span className="text-gray-400 text-sm font-normal">({typeProblems.length})</span>
          </div>
          <div className="p-2">
            {typeProblems.length === 0 ? (
              <div className="text-gray-400 text-sm p-2 italic">No generated problems of this type.</div>
            ) : (
              <ul className="space-y-1">
                {typeProblems.map((problem) => (
                  <li
                    key={problem.fullPath}
                    className="flex justify-between items-center p-2 hover:bg-gray-50 rounded group"
                  >
                    <span className="text-gray-700 font-mono text-sm">{problem.fileName}</span>
                    <div className="flex items-center gap-4">
                      <span className="text-xs text-gray-400 ml-auto text-right">
                        <PrettyPrintParams problemData={problem.problem} />
                      </span>
                      <div className="flex items-center transition-opacity">
                        <button
                          onClick={() => {
                            const nameWithoutExt = problem.fileName.replace(/\.[^/.]+$/, "");
                            const newName = prompt(`Enter new name for problem ${problem.fileName}:`, nameWithoutExt);
                            if (newName !== null) {
                              const trimmed = newName.trim();
                              if (trimmed === "" || trimmed.replace(/\./g, "") === "") {
                                alert("Invalid name.");
                                return;
                              }
                              if (trimmed !== nameWithoutExt) {
                                onRenameProblem(problem.fullPath, trimmed);
                              }
                            }
                          }}
                          className="text-blue-500 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-md transition-colors p-1.5 mx-1"
                          title="Rename Problem"
                        >
                          <Pencil size={16} />
                        </button>
                        <button
                          onClick={() => onDeleteProblem(problem.fullPath)}
                          className="text-red-500 hover:text-red-700 bg-red-50 hover:bg-red-100 rounded-md transition-colors p-1.5 mr-1"
                          title="Delete Problem"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProblemList;
