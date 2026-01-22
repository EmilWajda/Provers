export interface ParamSpec {
  checks: { [check: string]: any };
  description: string;
  type: "integer" | "float" | "boolean" | "choice" | "integer_list";
}

export type ProblemParams = { [paramName: string]: any };

export interface ProblemType {
  params: { [param: string]: ParamSpec };
  presets: { [preset: string]: ProblemParams };
}

export type ProblemTypeList = { [generator: string]: ProblemType };

export interface Problem {
  params: ProblemParams;
  problem: string; // ProblemType name
  seed: number;
}

export type ProblemFileList = { [filePath: string]: Problem | null };

export interface BenchmarkMetric {
  time: number;
  memory: number;
  status: "SAT" | "UNSAT";
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
  seed: number | null;
  timeout: number;
}

export interface Workspace {
  id: string;
  name: string;
  problems: Problem[];
  results: Result[];
  settings: WorkspaceSettings;
}

export type TabName = "settings" | "generator" | "benchmark" | "results";

export interface NotificationData {
  type: "success" | "error";
  message: string;
}
