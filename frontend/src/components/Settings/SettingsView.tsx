import { useState, useEffect } from 'react';
import { Settings, Save, Clock, Hash, Shuffle } from 'lucide-react';
import type { WorkspaceSettings } from '../../types';

interface SettingsViewProps {
  workspaceName: string;
  settings: WorkspaceSettings;
  onSave: (settings: WorkspaceSettings) => void;
  onNotify: (message: string, type?: 'success' | 'error') => void;
}

const SettingsView = ({ workspaceName, settings, onSave, onNotify }: SettingsViewProps) => {
  const [seedMode, setSeedMode] = useState<'random' | 'custom'>(settings.seedMode);
  const [customSeed, setCustomSeed] = useState<string>(settings.customSeed?.toString() || '');
  const [timeout, setTimeout] = useState<number>(settings.timeout);

  useEffect(() => {
    setSeedMode(settings.seedMode);
    setCustomSeed(settings.customSeed?.toString() || '');
    setTimeout(settings.timeout);
  }, [settings]);

  const handleSave = () => {
    if (seedMode === 'custom' && !customSeed) {
      onNotify('Please enter a valid seed value.', 'error');
      return;
    }

    const newSettings: WorkspaceSettings = {
      seedMode,
      customSeed: seedMode === 'custom' ? Number.parseInt(customSeed) : undefined,
      timeout
    };
    onSave(newSettings);
    onNotify('Settings saved successfully.');
  };

  return (
    <div className="p-8 h-full flex flex-col overflow-y-auto">
      <div className="flex items-center gap-3 mb-8 border-b pb-4">
        <Settings className="text-gray-600 w-8 h-8" />
        <div>
          <h2 className="text-3xl font-bold text-gray-800">Workspace Settings</h2>
          <p className="text-gray-500 text-sm">Configuration for: <span className="font-medium text-gray-700">{workspaceName}</span></p>
        </div>
      </div>

      <div className="max-w-3xl space-y-6">
        {/* Seed Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Hash size={20} className="text-blue-500"/> Seed Configuration
          </h3>
          <p className="text-gray-500 text-sm mb-4">
            Choose how random numbers are generated. Setting a specific seed allows for reproducible experiments.
          </p>
          
          <div className="space-y-4">
            <div className="flex gap-4">
              <button
                onClick={() => setSeedMode('random')}
                className={`flex-1 p-4 rounded-lg border-2 transition-all flex flex-col items-center gap-2 ${
                  seedMode === 'random' 
                  ? 'border-blue-500 bg-blue-50 text-blue-700' 
                  : 'border-gray-200 hover:border-gray-300 text-gray-600 hover:bg-gray-50'
                }`}
              >
                <Shuffle size={24} />
                <span className="font-medium">Random Seed</span>
              </button>
              <button
                onClick={() => setSeedMode('custom')}
                className={`flex-1 p-4 rounded-lg border-2 transition-all flex flex-col items-center gap-2 ${
                  seedMode === 'custom' 
                  ? 'border-blue-500 bg-blue-50 text-blue-700' 
                  : 'border-gray-200 hover:border-gray-300 text-gray-600 hover:bg-gray-50'
                }`}
              >
                <Hash size={24} />
                <span className="font-medium">Custom Seed</span>
              </button>
            </div>

            {seedMode === 'custom' && (
              <div className="animate-in fade-in slide-in-from-top-2 duration-200 pt-2">
                <label htmlFor="custom-seed" className="block text-sm font-medium text-gray-700 mb-1">
                  Seed Value
                </label>
                <input
                  id="custom-seed"
                  type="number"
                  value={customSeed}
                  onChange={(e) => setCustomSeed(e.target.value)}
                  placeholder="Enter an integer (e.g., 12345)"
                  className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none transition-shadow"
                />
                <p className="text-xs text-gray-400 mt-1">Enter an integer to serve as the generator seed.</p>
              </div>
            )}
          </div>
        </div>

        {/* Timeout Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Clock size={20} className="text-orange-500"/> Time Limit (Timeout)
          </h3>
          <p className="text-gray-500 text-sm mb-4">
            Specify the maximum time a prover can spend solving a single problem.
          </p>
          <div>
            <label htmlFor="timeout" className="block text-sm font-medium text-gray-700 mb-1">
              Maximum execution time (seconds)
            </label>
            <div className="flex items-center gap-3">
              <input
                id="timeout"
                type="number"
                value={timeout}
                onChange={(e) => setTimeout(Number(e.target.value))}
                min="1"
                className="w-32 border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none transition-shadow"
              />
              <span className="text-gray-500 text-sm">seconds per problem</span>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end pt-4">
          <button 
            onClick={handleSave}
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium shadow-md transition-colors flex items-center gap-2"
          >
            <Save size={20} /> Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingsView;
