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

  const PRESETS = {
    Default: { clauses: 50, lengths: [2, 3, 4, 6, 8, 10] },
    Short: { clauses: 30, lengths: [2,3,4] },
    Long: { clauses: 100, lengths: [6,8,10,12] },
    Custom: null as null | { clauses: number; lengths: number[] }
  };
  const [selectedPreset, setSelectedPreset] = useState<keyof typeof PRESETS>('Default');
  const [showPresets, setShowPresets] = useState<boolean>(false);

  const handleGenerate = () => {
    onGenerate(selectedType, { clauses, lengths });
  };

  const handleAddLength = () => {
    const val = Number.parseInt(newLength);
    if (!Number.isNaN(val) && val > 0 && !lengths.includes(val)) {
      setLengths([...lengths, val].sort((a, b) => a - b));
      setNewLength('');
      setSelectedPreset('Custom');
    }
  };

  const handleRemoveLength = (val: number) => {
    setLengths(lengths.filter(l => l !== val));
    setSelectedPreset('Custom');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddLength();
    }
  };

  const applyPreset = (key: keyof typeof PRESETS) => {
    setSelectedPreset(key);
    const p = PRESETS[key];
    if (p) {
      setClauses(p.clauses);
      setLengths([...p.lengths]);
    } else {
      // Custom
      setClauses(0);
      setLengths([]);
      setNewLength('');
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl w-96 p-6 animate-in fade-in zoom-in duration-200">
        <h3 className="text-xl font-bold mb-4 text-gray-800">Generate new problem</h3>
        <div className="space-y-4">
          <div>
            <label htmlFor="problem-type" className="block text-sm font-medium text-gray-700 mb-1">Problem type</label>
            <div className="flex items-center justify-between">
              <select 
                id="problem-type"
                className="w-56 border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-none"
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value as ProblemType)}
              >
                <option value="Problem 1">Problem 1</option>
                <option value="Problem 2">Problem 2</option>
                <option value="Problem 3">Problem 3</option>
              </select>
              <div className="ml-3 relative">
                <button
                  type="button"
                  onClick={() => setShowPresets(s => !s)}
                  className="text-sm px-3 h-10 flex items-center border rounded-md bg-gray-50 hover:bg-gray-100"
                >
                  Presets: {selectedPreset} ▾
                </button>
                {showPresets && (
                  <div className="absolute right-0 top-full mt-2 w-40 bg-white border border-gray-200 rounded-md shadow-lg z-20">
                    <div className="flex flex-col p-1">
                      <button type="button" onClick={() => { applyPreset('Default'); setShowPresets(false); }} className="text-left px-2 py-1 rounded hover:bg-gray-100">Default</button>
                      <button type="button" onClick={() => { applyPreset('Short'); setShowPresets(false); }} className="text-left px-2 py-1 rounded hover:bg-gray-100">Short</button>
                      <button type="button" onClick={() => { applyPreset('Long'); setShowPresets(false); }} className="text-left px-2 py-1 rounded hover:bg-gray-100">Long</button>
                      <button type="button" onClick={() => { applyPreset('Custom'); setShowPresets(false); }} className="text-left px-2 py-1 rounded hover:bg-gray-100">Custom</button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
          <div>
            <label htmlFor="problem-clauses" className="block text-sm font-medium text-gray-700 mb-1">Number of clauses</label>
            <input 
              id="problem-clauses"
              type="number" 
              placeholder="e.g. 100"
              className="w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-none"
              value={clauses}
              onChange={(e) => { setClauses(Number.parseInt(e.target.value) || 0); setSelectedPreset('Custom'); }}
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