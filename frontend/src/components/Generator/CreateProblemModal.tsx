import { useState } from 'react';
import { X, Plus } from 'lucide-react';
import type { ProblemType, ProblemParams } from '../../types';

interface CreateProblemModalProps {
  onClose: () => void;
  onGenerate: (type: ProblemType, params: ProblemParams) => void;
}

const CreateProblemModal = ({ onClose, onGenerate }: CreateProblemModalProps) => {
  const [selectedType, setSelectedType] = useState<ProblemType>('Problem 1');
  const [clauses, setClauses] = useState<number>(50);
  const [lengths, setLengths] = useState<number[]>([2, 3, 4, 6, 8, 10]);
  const [newLength, setNewLength] = useState<string>('');

  const handleGenerate = () => {
    onGenerate(selectedType, { clauses, lengths });
  };

  const handleAddLength = () => {
    const val = Number.parseInt(newLength);
    if (!Number.isNaN(val) && val > 0 && !lengths.includes(val)) {
      setLengths([...lengths, val].sort((a, b) => a - b));
      setNewLength('');
    }
  };

  const handleRemoveLength = (val: number) => {
    setLengths(lengths.filter(l => l !== val));
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddLength();
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl w-96 p-6 animate-in fade-in zoom-in duration-200">
        <h3 className="text-xl font-bold mb-4 text-gray-800">Generate new problem</h3>
        <div className="space-y-4">
          <div>
            <label htmlFor="problem-type" className="block text-sm font-medium text-gray-700 mb-1">Problem type</label>
            <select 
              id="problem-type"
              className="w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-none"
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value as ProblemType)}
            >
              <option value="Problem 1">Problem 1</option>
              <option value="Problem 2">Problem 2</option>
              <option value="Problem 3">Problem 3</option>
            </select>
          </div>
          <div>
            <label htmlFor="problem-clauses" className="block text-sm font-medium text-gray-700 mb-1">Number of clauses</label>
            <input 
              id="problem-clauses"
              type="number" 
              placeholder="e.g. 100"
              className="w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-none"
              value={clauses}
              onChange={(e) => setClauses(Number.parseInt(e.target.value) || 0)}
            />
          </div>
          <div>
            <label htmlFor="problem-lengths" className="block text-sm font-medium text-gray-700 mb-1">Clause lengths</label>
            <div className="flex gap-2 mb-2">
              <input 
                id="problem-lengths"
                type="number" 
                placeholder="Add length"
                className="flex-1 border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-none"
                value={newLength}
                onChange={(e) => setNewLength(e.target.value)}
                onKeyDown={handleKeyDown}
              />
              <button 
                onClick={handleAddLength}
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 p-2 rounded-md transition-colors"
                type="button"
              >
                <Plus size={20} />
              </button>
            </div>
            <div className="flex flex-wrap gap-2 min-h-[2rem]">
              {lengths.map(len => (
                <span key={len} className="bg-blue-100 text-blue-800 text-sm px-2 py-1 rounded-full flex items-center gap-1">
                  {len}
                  <button onClick={() => handleRemoveLength(len)} className="hover:text-blue-600 focus:outline-none">
                    <X size={14} />
                  </button>
                </span>
              ))}
              {lengths.length === 0 && <span className="text-gray-400 text-sm italic">No lengths added</span>}
            </div>
          </div>
        </div>
        <div className="mt-6 flex justify-end gap-3">
          <button onClick={onClose} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-md transition-colors">Cancel</button>
          <button onClick={handleGenerate} className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">Generate</button>
        </div>
      </div>
    </div>
  );
};

export default CreateProblemModal;