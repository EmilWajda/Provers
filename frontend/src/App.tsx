import { useState } from 'react';
import './App.css';
import type { Workspace, Problem, Result, ProblemType, TabName, WorkspaceSettings, ProblemParams } from './types';

import Sidebar from './components/Sidebar/Sidebar';
import GeneratorView from './components/Generator/GeneratorView';
import BenchmarkView from './components/Benchmark/BenchmarkView';
import ResultsView from './components/Results/ResultsView';
import SettingsView from './components/Settings/SettingsView';

const App = () => {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [activeWorkspaceId, setActiveWorkspaceId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabName>('settings');
  const [activeResultId, setActiveResultId] = useState<string | null>(null);
  const [notification, setNotification] = useState<{message: string, type: 'success' | 'error'} | null>(null);

  const activeWorkspace = workspaces.find(w => w.id === activeWorkspaceId);

  const showNotification = (message: string, type: 'success' | 'error' = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const createWorkspace = (name: string) => {
    if (workspaces.some(w => w.name === name)) {
      showNotification('Workspace with this name already exists.', 'error');
      return;
    }
    const newWorkspace: Workspace = { 
      id: Date.now().toString(), 
      name: name, 
      problems: [], 
      results: [],
      settings: {
        seedMode: 'random',
        timeout: 60
      }
    };
    setWorkspaces([...workspaces, newWorkspace]);
    setActiveWorkspaceId(newWorkspace.id);
    setActiveTab('settings');
    showNotification('Workspace created successfully');
  };

  const deleteWorkspace = (id: string) => {
    setWorkspaces(workspaces.filter(w => w.id !== id));
    if (activeWorkspaceId === id) {
      setActiveWorkspaceId(null);
    }
    showNotification('Workspace deleted successfully');
  };

  const updateWorkspaceSettings = (settings: WorkspaceSettings) => {
    if (!activeWorkspaceId) return;
    setWorkspaces(workspaces.map(ws => ws.id === activeWorkspaceId ? { ...ws, settings } : ws));
  };

  const addProblem = (type: ProblemType, params: ProblemParams) => {
    if (!activeWorkspaceId) return;
    const newProblem: Problem = { id: Date.now().toString(), name: `Problem_${type.at(-1)}_${Date.now().toString().slice(-5)}`, type, params };
    setWorkspaces(workspaces.map(ws => ws.id === activeWorkspaceId ? { ...ws, problems: [...ws.problems, newProblem] } : ws));
  };

  const deleteProblem = (problemId: string) => {
    if (!activeWorkspaceId) return;
    setWorkspaces(workspaces.map(ws => ws.id === activeWorkspaceId ? { ...ws, problems: ws.problems.filter(p => p.id !== problemId) } : ws));
  };

  const submitBenchmark = (selectedProblemIds: string[], selectedProvers: string[]) => {
    if (!activeWorkspaceId) return;
// tymczasowa logika generowania wyników benchmarku
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
// koniec tymczasowej logiki
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
  };

  const renderContent = () => {
    if (!activeWorkspace) return <div className="flex items-center justify-center h-full text-gray-400">Select or create a Workspace to start.</div>;
    
    switch (activeTab) {
      case 'settings': 
        return (
          <SettingsView 
            workspaceName={activeWorkspace.name} 
            settings={activeWorkspace.settings} 
            onSave={updateWorkspaceSettings} 
            onNotify={showNotification}
          />
        );
      case 'generator':  
        return <GeneratorView problems={activeWorkspace.problems} onAddProblem={addProblem} onDeleteProblem={deleteProblem} />;
      case 'benchmark': 
        return <BenchmarkView problems={activeWorkspace.problems} onSubmit={submitBenchmark} onNotify={showNotification} />;
      case 'results': 
        return <ResultsView results={activeWorkspace.results} activeResultId={activeResultId} onSelectResult={setActiveResultId} onBack={() => setActiveResultId(null)} />;
      default: 
        return null;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 text-gray-800 font-sans overflow-hidden">
      <Sidebar 
        workspaces={workspaces}
        activeWorkspaceId={activeWorkspaceId}
        activeTab={activeTab}
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
        <div className={`fixed top-6 left-1/2 -translate-x-1/2 px-6 py-3 rounded-lg shadow-xl text-white font-medium ${notification.type === 'success' ? 'bg-green-600' : 'bg-red-600'} z-50 transition-all animate-fade-in`}>
          {notification.message}
        </div>
      )}
    </div>
  );
};

export default App;