import { useState } from "react";
import "./App.css";
import type { Workspace, Problem, Result, ProblemType, TabName, WorkspaceSettings, ProblemParams } from "./types";

import Sidebar from "./components/Sidebar/Sidebar";
import GeneratorView from "./components/Generator/GeneratorView";
import BenchmarkView from "./components/Benchmark/BenchmarkView";
import ResultsView from "./components/Results/ResultsView";
import SettingsView from "./components/Settings/SettingsView";
import useWorkspaces from "./hooks/useWorkspaces";

const App = () => {
  const { workspaces, isLoading, createWorkspace, deleteWorkspace } = useWorkspaces();
  const [activeWorkspaceId, setActiveWorkspaceId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabName>("settings");
  const [activeResultId, setActiveResultId] = useState<string | null>(null);
  const [notification, setNotification] = useState<{ message: string; type: "success" | "error" } | null>(null);

  const activeWorkspace: Workspace | null = null;

  const showNotification = (message: string, type: "success" | "error" = "success") => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const updateWorkspaceSettings = (settings: WorkspaceSettings) => {
    if (!activeWorkspaceId) return;
    // setWorkspaces(workspaces.map(ws => ws.id === activeWorkspaceId ? { ...ws, settings } : ws));
  };

  const addProblem = (type: ProblemType, params: ProblemParams) => {
    if (!activeWorkspaceId) return;
    const lengthsPart = params.lengths.join("_");
    const ts = Math.floor(Date.now() / 1000);
    const name = `Problem_${type.at(-1)}_clauses_${params.clauses}_lengths_${lengthsPart}_timestamp_${ts}`;
    const newProblem: Problem = { id: Date.now().toString(), name, type, params };
    // setWorkspaces(workspaces.map(ws => ws.id === activeWorkspaceId ? { ...ws, problems: [...ws.problems, newProblem] } : ws));
  };

  const deleteProblem = (problemId: string) => {
    if (!activeWorkspaceId) return;
    // setWorkspaces(workspaces.map(ws => ws.id === activeWorkspaceId ? { ...ws, problems: ws.problems.filter(p => p.id !== problemId) } : ws));
  };

  const submitBenchmark = (selectedProblemIds: string[], selectedProvers: string[]) => {
    if (!activeWorkspaceId) return;
    /*
    const currentWorkspace = workspaces.find(w => w.id === activeWorkspaceId);
    if (!currentWorkspace) return;

    const detailedResults = selectedProblemIds.map(id => {
      const problem = currentWorkspace.problems.find(p => p.id === id);
      const problemStatus = Math.random() > 0.5 ? 'SAT' : 'UNSAT';
      return {
        problemName: problem ? problem.name : 'Unknown',
        proverResults: selectedProvers.reduce((acc, prover) => ({
          ...acc,
          [prover]: {
            time: Number((Math.random() * 5).toFixed(3)),
            memory: Math.floor(Math.random() * 50000 + 1000),
            status: problemStatus
          }
        }), {})
      };
    });
    const newResult: Result = {
      id: Date.now().toString(),
      timestamp: new Date().toLocaleString(),
      provers: selectedProvers,
      problemCount: selectedProblemIds.length,
      detailedResults
    };
    setWorkspaces(workspaces.map(ws => ws.id === activeWorkspaceId ? { ...ws, results: [newResult, ...ws.results] } : ws));
    setActiveTab('results');
    setActiveResultId(newResult.id);
    */
  };

  const renderContent = () => {
    if (!activeWorkspace)
      return (
        <div className="flex items-center justify-center h-full text-gray-400">
          Select or create a Workspace to start.
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
        activeWorkspaceId={activeWorkspaceId}
        activeTab={activeTab}
        isLoading={isLoading}
        onCreateWorkspace={createWorkspace}
        onDeleteWorkspace={deleteWorkspace}
        onSelectWorkspace={setActiveWorkspaceId}
        onSelectTab={(workspaceId, tab) => {
          setActiveWorkspaceId(workspaceId);
          setActiveTab(tab);
          setActiveResultId(null);
        }}
      />
      <main className="flex-1 overflow-auto bg-white shadow-inner m-2 rounded-xl border border-gray-200">
        {renderContent()}
      </main>
      {notification && (
        <div
          className={`fixed top-6 left-1/2 -translate-x-1/2 px-6 py-3 rounded-lg shadow-xl text-white font-medium ${
            notification.type === "success" ? "bg-green-600" : "bg-red-600"
          } z-50 transition-all animate-fade-in`}
        >
          {notification.message}
        </div>
      )}
    </div>
  );
};

export default App;
