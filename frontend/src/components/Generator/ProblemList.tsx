import { Trash2 } from 'lucide-react';
import type { Problem } from '../../types';

interface ProblemListProps {
  problems: Problem[];
  onDeleteProblem: (id: string) => void;
}

const ProblemList = ({ problems, onDeleteProblem }: ProblemListProps) => {
  const groupedProblems: Record<string, Problem[]> = {
    'Problem 1': problems.filter(p => p.type === 'Problem 1'),
    'Problem 2': problems.filter(p => p.type === 'Problem 2'),
    'Problem 3': problems.filter(p => p.type === 'Problem 3'),
  };

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
                {typeProblems.map(problem => (
                  <li key={problem.id} className="flex justify-between items-center p-2 hover:bg-gray-50 rounded group">
                    <span className="text-gray-700 font-mono text-sm">{problem.name}</span>
                    <div className="flex items-center gap-4">
                      <span className="text-xs text-gray-400">Clauses: {problem.params.clauses}, Lengths: [{problem.params.lengths.join(', ')}]</span>
                      <button 
                        onClick={() => onDeleteProblem(problem.id)}
                        className="text-red-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-opacity"
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