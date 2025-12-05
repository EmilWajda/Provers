export type ProblemType = 'Problem 1' | 'Problem 2' | 'Problem 3';

export interface ProblemParams {
  clauses: number;
  lengths: number[];
}

export interface Problem {
  id: string;
  name: string;
  type: ProblemType;
  params: ProblemParams;
}

export interface BenchmarkMetric {
  time: number;
  memory: number;
  status: 'SAT' | 'UNSAT';
}

export interface ProblemResult {
  problemName: string;
  proverResults: Record<string, BenchmarkMetric>;
}

export interface Result {
  id: string;
  timestamp: string;
  provers: string[];
  problemCount: number;
  detailedResults: ProblemResult[];
}

export interface WorkspaceSettings {
  seedMode: 'random' | 'custom';
  customSeed?: number;
  timeout: number;
}

export interface Workspace {
  id: string;
  name: string;
  problems: Problem[];
  results: Result[];
  settings: WorkspaceSettings;
}

export type TabName = 'settings' | 'generator' | 'benchmark' | 'results';