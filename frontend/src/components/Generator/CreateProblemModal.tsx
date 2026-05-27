import { useState, useEffect } from "react";
import { X, Plus } from "lucide-react";
import type { ProblemParams } from "../../types";
import useProblemTypes from "../../hooks/useProblemTypes";

type IntegerListInputProps = {
  value: number[];
  onChange: (v: number[]) => void;
  name: string;
  description?: string;
};

interface CreateProblemModalProps {
  onClose: () => void;
  onGenerate: (type: string, params: ProblemParams) => void;
}

const ParamLabel = ({ name, description }: { name: string; description?: string }) => (
  <div className="group relative w-fit mb-1">
    <label className="block text-sm font-medium text-gray-700 cursor-help underline decoration-dotted decoration-gray-400">
      {name}
    </label>
    {description && (
      <div className="pointer-events-none absolute bottom-full left-0 mb-2 w-max max-w-xs rounded-sm bg-gray-900 px-2 py-1 text-xs text-white opacity-0 transition-opacity group-hover:opacity-100 z-10 shadow-lg">
        {description}
        <div className="absolute top-full left-4 -mt-[1px] border-4 border-transparent border-t-gray-900"></div>
      </div>
    )}
  </div>
);

const IntegerListInput = ({ value, onChange, name, description }: IntegerListInputProps) => {
  const [newVal, setNewVal] = useState("");
  const add = () => {
    const v = parseInt(newVal);
    const current = value || [];
    if (!isNaN(v) && !current.includes(v)) {
      onChange([...current, v].sort((a, b) => a - b));
      setNewVal("");
    }
  };
  return (
    <div className="mb-4">
      <ParamLabel name={name} description={description} />
      <div className="flex gap-2 mb-2">
        <input
          type="number"
          value={newVal}
          onChange={(e) => setNewVal(e.target.value)}
          className="flex-1 border rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-hidden"
          placeholder="Add value"
          onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), add())}
        />
        <button
          type="button"
          onClick={add}
          className="bg-gray-100 hover:bg-gray-200 text-gray-700 p-2 rounded-md transition-colors"
        >
          <Plus size={20} />
        </button>
      </div>
      <div className="flex flex-wrap gap-2">
        {(value || []).map((v) => (
          <span key={v} className="bg-blue-100 text-blue-800 text-sm px-2 py-1 rounded-full flex items-center gap-1">
            {v}
            <button onClick={() => onChange(value.filter((x) => x !== v))}>
              <X size={14} />
            </button>
          </span>
        ))}
      </div>
    </div>
  );
};

const CreateProblemModal = ({ onClose, onGenerate }: CreateProblemModalProps) => {
  const { problemTypes, isLoading } = useProblemTypes();
  const [selectedType, setSelectedType] = useState<string>("");
  const [currentParams, setCurrentParams] = useState<ProblemParams>({});

  useEffect(() => {
    if (!isLoading && problemTypes && Object.keys(problemTypes).length > 0 && !selectedType) {
      const keys = Object.keys(problemTypes).sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }));
      setSelectedType(keys[0]);
    }
  }, [problemTypes, isLoading, selectedType]);

  const applyPreset = (presetName: string) => {
    if (selectedType && problemTypes[selectedType] && problemTypes[selectedType].presets[presetName]) {
      setCurrentParams({ ...problemTypes[selectedType].presets[presetName] });
    }
  };

  useEffect(() => {
    if (selectedType && problemTypes[selectedType]) {
      const presets = problemTypes[selectedType].presets;
      const presetKeys = Object.keys(presets);
      if (presetKeys.includes("Default")) {
        applyPreset("Default");
      } else if (presetKeys.length > 0) {
        applyPreset(presetKeys[0]);
      } else {
        setCurrentParams({});
      }
    }
  }, [selectedType]);

  const handleGenerate = () => {
    onGenerate(selectedType, currentParams);
  };

  if (isLoading)
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-black bg-black/50 z-50">
        <div className="bg-white p-4 rounded">Loading...</div>
      </div>
    );

  const currentTypeSpec = problemTypes[selectedType];

  return (
    <div className="fixed inset-0 bg-black bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl w-96 p-6 animate-in fade-in zoom-in duration-200 max-h-[90vh] overflow-y-auto">
        <h3 className="text-xl font-bold mb-4 text-gray-800">Generate new problem</h3>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Problem type</label>
            <select
              className="w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-hidden"
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
            >
              {Object.keys(problemTypes)
                .sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }))
                .map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
            </select>
          </div>

          {currentTypeSpec && Object.keys(currentTypeSpec.presets).length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Preset</label>
              <div className="flex flex-wrap gap-2">
                {Object.keys(currentTypeSpec.presets).map((preset) => (
                  <button
                    key={preset}
                    type="button"
                    onClick={() => applyPreset(preset)}
                    className="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-sm border border-gray-300"
                  >
                    {preset}
                  </button>
                ))}
              </div>
            </div>
          )}

          {currentTypeSpec &&
            Object.entries(currentTypeSpec.params).map(([key, spec]) => {
              if (spec.type === "integer" || spec.type === "float") {
                return (
                  <div key={key}>
                    <ParamLabel name={key} description={spec.description} />
                    <input
                      type="number"
                      step={spec.type === "float" ? "any" : "1"}
                      className="w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-hidden"
                      value={currentParams[key] ?? ""}
                      onChange={(e) =>
                        setCurrentParams({
                          ...currentParams,
                          [key]:
                            spec.type === "float" ? parseFloat(e.target.value) || 0 : parseInt(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                );
              }
              if (spec.type === "boolean") {
                return (
                  <div key={key} className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id={`param-${key}`}
                      checked={!!currentParams[key]}
                      onChange={(e) => setCurrentParams({ ...currentParams, [key]: e.target.checked })}
                      className="w-4 h-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <ParamLabel name={key} description={spec.description} />
                  </div>
                );
              }
              if (spec.type === "choice") {
                const choices = spec.checks?.choices || [];
                return (
                  <div key={key}>
                    <ParamLabel name={key} description={spec.description} />
                    <select
                      className="w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 outline-hidden"
                      value={currentParams[key] ?? choices[0] ?? ""}
                      onChange={(e) => setCurrentParams({ ...currentParams, [key]: e.target.value })}
                    >
                      {choices.map((c: string) => (
                        <option key={c} value={c}>
                          {c}
                        </option>
                      ))}
                    </select>
                  </div>
                );
              }
              if (spec.type === "integer_list") {
                return (
                  <IntegerListInput
                    key={key}
                    name={key}
                    description={spec.description}
                    value={(currentParams[key] as number[]) || []}
                    onChange={(val) => setCurrentParams({ ...currentParams, [key]: val })}
                  />
                );
              }
              return null;
            })}
        </div>

        <div className="mt-6 flex justify-end gap-3">
          <button onClick={onClose} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-md transition-colors">
            Cancel
          </button>
          <button
            onClick={handleGenerate}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            Generate
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateProblemModal;
