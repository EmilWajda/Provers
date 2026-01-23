import { Trash2 } from "lucide-react";
import type { ProblemFileList } from "../../types";
import { groupProblems, PrettyPrintParams } from "../../utils";

interface ProblemListProps {
  problems: ProblemFileList;
  onDeleteProblem: (path: string) => void;
}

const ProblemList = ({ problems, onDeleteProblem }: ProblemListProps) => {
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
                      <button
                        onClick={() => onDeleteProblem(problem.fullPath)}
                        className="text-red-300 hover:text-red-600 transition-colors p-2 mr-2"
                        title="Delete Problem"
                      >
                        <Trash2 size={16} />
                      </button>
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
