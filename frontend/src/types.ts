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

export class ResultSummary {
  filePath: string | null;
  timestamp: Date;
  provers: string[];
  problems: string[];

  constructor(timestamp: string, provers: string[], problems: string[], filePath: string | null = null) {
    this.timestamp = new Date(timestamp);
    this.provers = provers;
    this.problems = problems;
    this.filePath = filePath;
  }

  get id(): string {
    return this.filePath || Math.floor(this.timestamp.getTime() / 1000).toString();
  }
}

export type RunStats = {
  system_time: number;
  real_time: number;
  peak_memory: number;
};

export type ResultCell = {
  problem: string;
  prover: string;
  result: "satisfiable" | "unsatisfiable" | "unknown" | "timeout" | "unconverted" | null; // null means not finished yet
  stats: RunStats | null;
};

export interface WorkspaceSettings {
  seed: number | null;
  timeout: number;
  check: boolean;
}

export type TabName = "settings" | "generator" | "benchmark" | "results";

export interface NotificationData {
  type: "success" | "error";
  message: string;
}
