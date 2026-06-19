import type { Problem, ProblemFileList } from "./types";

function formatParamName(str: string): string {
  return str
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function PrettyPrintParams({ problemData }: { problemData: Problem | null }) {
  if (!problemData) return <p>Unknown Problem</p>;
  const { problem, params, seed } = problemData;
  const paramsFormatted = Object.entries(params)
    .map(([key, value]) => `${formatParamName(key)}: ${JSON.stringify(value)}`)
    .join(", ");
  return (
    <>
      <p>{`Problem ${problem}`}</p>
      <p>{paramsFormatted}</p>
      <p>{`Seed: ${seed}`}</p>
    </>
  );
}

export function splitPath(path: string): { directory: string; fileName: string } {
  const parts = path.split("/");
  const fileName = parts.pop() || "";
  const directory = parts.join("/");
  return { directory, fileName };
}

export function groupProblems(
  problems: ProblemFileList,
): Record<string, { fileName: string; fullPath: string; problem: Problem | null }[]> {
  const groupedProblems: Record<string, { fileName: string; fullPath: string; problem: Problem | null }[]> = {};
  
  const sortedPaths = Object.keys(problems).sort((a, b) => 
    a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' })
  );
  
  for (const path of sortedPaths) {
    const problem = problems[path];
    const { directory, fileName } = splitPath(path);
    if (!groupedProblems[directory]) groupedProblems[directory] = [];
    groupedProblems[directory].push({ fileName, fullPath: path, problem });
  }
  return groupedProblems;
}
