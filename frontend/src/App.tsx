import { useState } from "react";
import "./App.css";
import type { Workspace, Problem, Result, ProblemType, TabName, WorkspaceSettings, ProblemParams } from "./types";

import Sidebar from "./components/Sidebar/Sidebar";
import GeneratorView from "./components/Generator/GeneratorView";
import BenchmarkView from "./components/Benchmark/BenchmarkView";
import ResultsView from "./components/Results/ResultsView";
import SettingsView from "./components/Settings/SettingsView";
import useWorkspaces from "./hooks/useWorkspaces";
import Notification from "./components/Notification";
import { useActiveWorkspace } from "./hooks/useActiveWorkspace";

const App = () => {
  const { workspaces, isLoading, createWorkspace, deleteWorkspace } = useWorkspaces();
  const { workspace: activeWorkspace, setWorkspace: setActiveWorkspace } = useActiveWorkspace();
  const [activeTab, setActiveTab] = useState<TabName>("settings");
  const [activeResultId, setActiveResultId] = useState<string | null>(null);

  // const submitBenchmark = (selectedProblemIds: string[], selectedProvers: string[]) => {
  //   if (!activeWorkspaceId) return;
  //   const currentWorkspace = workspaces.find(w => w.id === activeWorkspaceId);
  //   if (!currentWorkspace) return;

  //   const detailedResults = selectedProblemIds.map(id => {
  //     const problem = currentWorkspace.problems.find(p => p.id === id);
  //     const problemStatus = Math.random() > 0.5 ? 'SAT' : 'UNSAT';
  //     return {
  //       problemName: problem ? problem.name : 'Unknown',
  //       proverResults: selectedProvers.reduce((acc, prover) => ({
  //         ...acc,
  //         [prover]: {
  //           time: Number((Math.random() * 5).toFixed(3)),
  //           memory: Math.floor(Math.random() * 50000 + 1000),
  //           status: problemStatus
  //         }
  //       }), {})
  //     };
  //   });
  //   const newResult: Result = {
  //     id: Date.now().toString(),
  //     timestamp: new Date().toLocaleString(),
  //     provers: selectedProvers,
  //     problemCount: selectedProblemIds.length,
  //     detailedResults
  //   };
  //   setWorkspaces(workspaces.map(ws => ws.id === activeWorkspaceId ? { ...ws, results: [newResult, ...ws.results] } : ws));
  //   setActiveTab('results');
  //   setActiveResultId(newResult.id);
  // };

  const renderContent = () => {
    if (!activeWorkspace) {
      return (
        <div className="flex items-center justify-center h-full text-gray-400">
          Select or create a Workspace to start.
        </div>
      );
    }

    return (
      // TODO: readd views
      <div className="flex items-center justify-center h-full text-green-400">
        Selected: {activeWorkspace}, tab: {activeTab}
      </div>
    );

    // switch (activeTab) {
    //   case 'settings':
    //     return (
    //       <SettingsView
    //         workspaceName={activeWorkspace.name}
    //         settings={activeWorkspace.settings}
    //         onSave={updateWorkspaceSettings}
    //         onNotify={showNotification}
    //       />
    //     );
    //   case 'generator':
    //     return <GeneratorView problems={activeWorkspace.problems} onAddProblem={addProblem} onDeleteProblem={deleteProblem} />;
    //   case 'benchmark':
    //     return <BenchmarkView problems={activeWorkspace.problems} onSubmit={submitBenchmark} onNotify={showNotification} />;
    //   case 'results':
    //     return <ResultsView results={activeWorkspace.results} activeResultId={activeResultId} onSelectResult={setActiveResultId} onBack={() => setActiveResultId(null)} />;
    //   default:
    //     return null;
    // }
  };

  return (
    <div className="flex h-screen bg-gray-50 text-gray-800 font-sans overflow-hidden">
      <Sidebar
        workspaces={workspaces}
        activeTab={activeTab}
        isLoading={isLoading}
        onCreateWorkspace={createWorkspace}
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
