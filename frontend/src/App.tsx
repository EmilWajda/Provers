import { useState } from "react";
import "./App.css";
import type { TabName } from "./types";

import Sidebar from "./components/Sidebar/Sidebar";
import GeneratorView from "./components/Generator/GeneratorView";
import BenchmarkView from "./components/Benchmark/BenchmarkView";
import SettingsView from "./components/Settings/SettingsView";
import ResultView from "./components/Results/ResultView";
import ResultListView from "./components/Results/ResultListView";
import useWorkspaces from "./hooks/useWorkspaces";
import Notification from "./components/Notification";
import { useActiveWorkspace } from "./hooks/useActiveWorkspace";

const App = () => {
  const { workspaces, isLoading, createWorkspace, deleteWorkspace, renameWorkspace } = useWorkspaces();
  const { workspace: activeWorkspace, setWorkspace: setActiveWorkspace } = useActiveWorkspace();
  const [activeTab, setActiveTab] = useState<TabName>("settings");
  const [activeResultId, setActiveResultId] = useState<string | null>(null);

  const renderContent = () => {
    if (!activeWorkspace) {
      return (
        <div className="flex items-center justify-center h-full text-gray-400">
          Select or create a Workspace to start.
        </div>
      );
    }

    switch (activeTab) {
      case "settings":
        return <SettingsView key={activeWorkspace} />;
      case "generator":
        return <GeneratorView key={activeWorkspace} />;
      case "benchmark":
        return (
          <BenchmarkView
            key={activeWorkspace}
            onSubmit={(resultId) => {
              setActiveTab("results");
              setActiveResultId(resultId);
            }}
          />
        );
      case "results":
        if (activeResultId) {
          return <ResultView resultId={activeResultId} onBack={() => setActiveResultId(null)} />;
        } else {
          return <ResultListView onSelectResult={(resultId) => setActiveResultId(resultId)} />;
        }
      default:
        return (
          <div className="flex items-center justify-center h-full text-red-400">
            Tab '{activeTab}' is not implemented yet.
          </div>
        );
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 text-gray-800 font-sans overflow-hidden">
      <Sidebar
        workspaces={workspaces}
        activeTab={activeTab}
        isLoading={isLoading}
        onCreateWorkspace={createWorkspace}
        onRenameWorkspace={(workspace, newName) => {
          renameWorkspace(workspace, newName);
        }}
        onDeleteWorkspace={(workspace) => {
          deleteWorkspace(workspace);
          if (activeWorkspace === workspace) {
            setActiveWorkspace(null);
            setActiveTab("settings");
            setActiveResultId(null);
          }
        }}
        onSelectTab={(workspaceId, tab) => {
          setActiveWorkspace(workspaceId);
          setActiveTab(tab);
          setActiveResultId(null);
        }}
      />
      <main className="flex-1 overflow-auto bg-white shadow-inner m-2 rounded-xl border border-gray-200">
        {renderContent()}
      </main>
      <Notification />
    </div>
  );
};

export default App;
