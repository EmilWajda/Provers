import { useState, useEffect } from "react";
import { Settings, Save, Clock, Hash, Shuffle, ToggleRight } from "lucide-react";
import type { WorkspaceSettings } from "../../types";
import { useQuery } from "@tanstack/react-query";
import { useActiveWorkspace } from "../../hooks/useActiveWorkspace";
import { useNotificationContext } from "../../hooks/useNotificationContext";
import axios from "axios";
import useMutationNotify from "../../hooks/useMutationNotify";

const queryKey = (workspace: string) => ["settings", workspace];

export default function SettingsView() {
  const activeWorkspace = useActiveWorkspace().workspace;
  const { showNotification } = useNotificationContext();

  const query = useQuery({
    queryKey: queryKey(activeWorkspace!),
    queryFn: async (): Promise<WorkspaceSettings> => {
      const response = await axios.get(`/api/workspaces/${activeWorkspace}/settings`);
      return response.data;
    },
  });

  const updateSettings = useMutationNotify({
    mutationFn: async (newSettings: WorkspaceSettings) => {
      await axios.put(`/api/workspaces/${activeWorkspace}/settings`, newSettings);
    },
    queryKey: queryKey(activeWorkspace!),
    successMessage: "Workspace settings updated successfully.",
  });

  const [seedMode, setSeedMode] = useState<"random" | "custom" | null>(null);
  const [customSeed, setCustomSeed] = useState<number>(0);
  const [proverTimeout, setProverTimeout] = useState<number>(60);
  const [checkEnabled, setCheckEnabled] = useState<boolean>(true);

  useEffect(() => {
    if (query.data) {
      if (query.data.seed !== null) {
        setSeedMode("custom");
        setCustomSeed(query.data.seed);
      } else {
        setSeedMode("random");
        setCustomSeed(0);
      }
      setProverTimeout(query.data.timeout);
      setCheckEnabled(query.data.check);
    }
  }, [query.data]);

  const handleSave = () => {
    if (seedMode === "custom" && !Number.isFinite(customSeed)) {
      showNotification({
        message: "Please enter a valid seed value.",
        type: "error",
      });
      return;
    }

    const newSettings: WorkspaceSettings = {
      seed: seedMode === "custom" ? customSeed : null,
      timeout: proverTimeout,
      check: checkEnabled,
    };
    updateSettings(newSettings);
  };

  return (
    <div className="p-8 h-full flex flex-col overflow-y-auto">
      <div className="flex items-center gap-3 mb-8 border-b pb-4">
        <Settings className="text-gray-600 w-8 h-8" />
        <div>
          <h2 className="text-3xl font-bold text-gray-800">Workspace Settings</h2>
          <p className="text-gray-500 text-sm">
            Configuration for: <span className="font-medium text-gray-700">{activeWorkspace}</span>
          </p>
        </div>
      </div>

      <div className="max-w-3xl space-y-6">
        {/* Seed Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Hash size={20} className="text-blue-500" /> Seed Configuration
          </h3>
          <p className="text-gray-500 text-sm mb-4">
            Choose how random numbers are generated. Setting a specific seed allows for reproducible experiments.
          </p>

          <div className="space-y-4">
            <div className="flex gap-4">
              <button
                onClick={() => setSeedMode("random")}
                className={`flex-1 p-4 rounded-lg border-2 transition-all flex flex-col items-center gap-2 ${
                  seedMode === "random"
                    ? "border-blue-500 bg-blue-50 text-blue-700"
                    : "border-gray-200 hover:border-gray-300 text-gray-600 hover:bg-gray-50"
                }`}
              >
                <Shuffle size={24} />
                <span className="font-medium">Random Seed</span>
              </button>
              <button
                onClick={() => setSeedMode("custom")}
                className={`flex-1 p-4 rounded-lg border-2 transition-all flex flex-col items-center gap-2 ${
                  seedMode === "custom"
                    ? "border-blue-500 bg-blue-50 text-blue-700"
                    : "border-gray-200 hover:border-gray-300 text-gray-600 hover:bg-gray-50"
                }`}
              >
                <Hash size={24} />
                <span className="font-medium">Custom Seed</span>
              </button>
            </div>

            {seedMode === "custom" && (
              <div className="animate-in fade-in slide-in-from-top-2 duration-200 pt-2">
                <label htmlFor="custom-seed" className="block text-sm font-medium text-gray-700 mb-1">
                  Seed Value
                </label>
                <input
                  id="custom-seed"
                  type="number"
                  value={customSeed}
                  onChange={(e) => setCustomSeed(Number(e.target.value))}
                  placeholder="Enter an integer (e.g., 12345)"
                  className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-hidden transition-shadow"
                />
                <p className="text-xs text-gray-400 mt-1">Enter an integer to serve as the generator seed.</p>
              </div>
            )}
          </div>
        </div>

        {/* Timeout Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Clock size={20} className="text-orange-500" /> Time Limit (Timeout)
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
                value={proverTimeout}
                onChange={(e) => setProverTimeout(Number(e.target.value))}
                min="1"
                className="w-32 border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-hidden transition-shadow"
              />
              <span className="text-gray-500 text-sm">seconds per problem</span>
            </div>
          </div>
        </div>

        {/* Flags Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <ToggleRight size={20} className="text-green-500" />
            Additional Flags
          </h3>
          <p className="text-gray-500 text-sm mb-4">Enable or disable additional flags for this workspace.</p>
          <label
            htmlFor="check-enabled"
            className="flex items-center justify-between gap-3 p-3 rounded-lg border border-gray-200 hover:border-gray-300 cursor-pointer"
          >
            <div>
              <p className="text-sm font-medium text-gray-800">Enable generator checks</p>
              <p className="text-xs text-gray-500">
                When enabled, the generator will run a TPTP syntax checker to ensure correctness.
              </p>
            </div>
            <input
              id="check-enabled"
              type="checkbox"
              checked={checkEnabled}
              onChange={(e) => setCheckEnabled(e.target.checked)}
              className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
          </label>
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
}
