import { Trash2 } from 'lucide-react';
import type { Problem } from '../../types';
import { PrettyPrintParams } from '../../utils';

type ProblemWithId = Problem & { id: string };

interface ProblemListProps {
  problems: ProblemWithId[];
  onDeleteProblem: (id: string) => void;
}

const ProblemList = ({ problems, onDeleteProblem }: ProblemListProps) => {
  const groupedProblems = problems.reduce((acc, problem) => {
    const type = problem.problem;
    if (!acc[type]) acc[type] = [];
    acc[type].push(problem);
    return acc;
  }, {} as Record<string, ProblemWithId[]>);

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
              <ul className="space-y-1">
                {typeProblems.map(problem => (
                  <li key={problem.id} className="flex justify-between items-center p-2 hover:bg-gray-50 rounded group">
                    <span className="text-gray-700 font-mono text-sm whitespace-pre-wrap"><PrettyPrintParams problemData={problem} /></span>
                     <button 
                        onClick={() => onDeleteProblem(problem.id)}
                        className="text-red-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-opacity"
                        title="Delete Problem"
                      >
                        <Trash2 size={16} />
                      </button>
                  </li>
                ))}
              </ul>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProblemList;