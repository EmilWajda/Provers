import { useState } from 'react';
import { BarChart, ChevronDown, ChevronRight, CheckSquare, Square, Play } from 'lucide-react';
import type { Problem } from '../../types';

interface BenchmarkViewProps {
  problems: Problem[];
  onSubmit: (ids: string[], provers: string[]) => void;
  onNotify: (message: string, type?: 'success' | 'error') => void;
}

const BenchmarkView = ({ problems, onSubmit, onNotify }: BenchmarkViewProps) => {
  const [selectedProblems, setSelectedProblems] = useState<Set<string>>(new Set());
  const [selectedProvers, setSelectedProvers] = useState<Set<string>>(new Set(['SPASS']));
  const [expandedTypes, setExpandedTypes] = useState<Set<string>>(new Set());

  const toggleProblem = (id: string) => {
    const newSet = new Set(selectedProblems);
    if (newSet.has(id)) newSet.delete(id);
    else newSet.add(id);
    setSelectedProblems(newSet);
  };

  const toggleProver = (prover: string) => {
    const newSet = new Set(selectedProvers);
    if (newSet.has(prover)) newSet.delete(prover);
    else newSet.add(prover);
    setSelectedProvers(newSet);
  };

  const toggleTypeExpand = (type: string) => {
    const newSet = new Set(expandedTypes);
    if (newSet.has(type)) newSet.delete(type);
    else newSet.add(type);
    setExpandedTypes(newSet);
  };

  const selectAllInType = (typeProblems: Problem[]) => {
    const newSet = new Set(selectedProblems);
    const allSelected = typeProblems.every(p => newSet.has(p.id));
    for (const p of typeProblems) {
      if (allSelected) newSet.delete(p.id);
      else newSet.add(p.id);
    }
    setSelectedProblems(newSet);
  };

  const handleSubmit = () => {
    if (selectedProblems.size === 0) return onNotify("Select at least one problem.", 'error');
    if (selectedProvers.size === 0) return onNotify("Select at least one prover.", 'error');
    onSubmit(Array.from(selectedProblems), Array.from(selectedProvers));
  };

  const groupedProblems: Record<string, Problem[]> = {
    'Problem 1': problems.filter(p => p.type === 'Problem 1'),
    'Problem 2': problems.filter(p => p.type === 'Problem 2'),
    'Problem 3': problems.filter(p => p.type === 'Problem 3'),
  };

  return (
    <div className="p-8 h-full flex flex-col relative">
      <div className="flex items-center gap-3 mb-6 border-b pb-4">
        <BarChart className="text-purple-600 w-8 h-8" />
        <h2 className="text-3xl font-bold text-gray-800">Benchmark</h2>
      </div>

      <div className="flex-1 overflow-y-auto mb-32 pr-2">
        {Object.entries(groupedProblems).map(([type, typeProblems]) => (
          <div key={type} className="mb-4 bg-white border border-gray-200 rounded-lg overflow-hidden">
            <div className="flex items-center justify-between p-3 bg-gray-50 cursor-pointer hover:bg-gray-100 transition-colors">
              <button 
                type="button"
                className="flex items-center gap-2 flex-1 text-left bg-transparent border-none p-0 cursor-pointer" 
                onClick={() => toggleTypeExpand(type)}
              >
                {expandedTypes.has(type) ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
                <span className="font-semibold text-gray-700">{type}</span>
                <span className="bg-gray-200 text-gray-600 text-xs px-2 py-0.5 rounded-full">{typeProblems.length}</span>
              </button>
              <button onClick={(e) => { e.stopPropagation(); selectAllInType(typeProblems); }} className="text-xs text-blue-600 hover:underline px-2">
                Select/Deselect All
              </button>
            </div>

            {expandedTypes.has(type) && (
              <div className="p-2 space-y-1 bg-white border-t border-gray-100">
                {typeProblems.length === 0 && <p className="text-sm text-gray-400 p-2">No problems.</p>}
                {typeProblems.map(problem => {
                  const isSelected = selectedProblems.has(problem.id);
                  return (
                    <button 
                      key={problem.id}
                      onClick={() => toggleProblem(problem.id)}
                      className={`w-full flex items-center gap-3 p-2 rounded cursor-pointer transition-colors text-left outline-none focus:ring-2 focus:ring-blue-500 ${
                        isSelected ? 'bg-blue-50 border border-blue-200' : 'hover:bg-gray-50 border border-transparent'
                      }`}
                    >
                      {isSelected ? <CheckSquare className="text-blue-600 w-5 h-5" /> : <Square className="text-gray-400 w-5 h-5" />}
                      <span className={`${isSelected ? 'text-blue-900 font-medium' : 'text-gray-700'}`}>{problem.name}</span>
                      <span className="text-xs text-gray-400 ml-auto">Clauses: {problem.params.clauses}, Lengths: [{problem.params.lengths.join(', ')}]</span>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-6 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)]">
        <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">Select Provers</h3>
        <div className="flex flex-wrap gap-4 mb-6">
          {['SPASS', 'CVC5', 'Vampire'].map(prover => {
            const isChecked = selectedProvers.has(prover);
            return (
              <label key={prover} className="flex items-center gap-2 cursor-pointer select-none">
                <input 
                  type="checkbox"
                  className="sr-only"
                  checked={isChecked}
                  onChange={() => toggleProver(prover)}
                />
                <div 
                  className={`w-5 h-5 rounded border flex items-center justify-center transition-colors ${
                    isChecked ? 'bg-purple-600 border-purple-600' : 'border-gray-300 bg-white'
                  }`}
                  aria-hidden="true"
                >
                  {isChecked && <CheckSquare size={14} className="text-white" />}
                </div>
                <span className="text-gray-700 font-medium">{prover}</span>
              </label>
            );
          })}
        </div>

        <button 
          onClick={handleSubmit}
          disabled={selectedProblems.size === 0 || selectedProvers.size === 0}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 rounded-lg font-bold text-lg shadow-lg flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <Play fill="currentColor" /> SUBMIT BENCHMARK ({selectedProblems.size})
        </button>
      </div>
    </div>
  );
};

export default BenchmarkView;