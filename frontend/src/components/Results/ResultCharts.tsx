import { useState, useMemo } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import type { ResultCell, ProblemFileList, ProblemTypeList } from "../../types";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface ResultChartsProps {
  cells: ResultCell[];
  provers: string[];
  problems: ProblemFileList;
  problemTypes: ProblemTypeList;
}

type ChartMetric = "system_time" | "real_time" | "peak_memory";

const CHART_COLORS = [
  "rgb(59, 130, 246)",
  "rgb(239, 68, 68)",
  "rgb(34, 197, 94)",
  "rgb(234, 179, 8)",
  "rgb(168, 85, 247)",
  "rgb(249, 115, 22)",
  "rgb(20, 184, 166)",
  "rgb(236, 72, 153)",
];

const METRIC_LABELS: Record<ChartMetric, string> = {
  system_time: "System Time (s)",
  real_time: "Real Time (s)",
  peak_memory: "Peak Memory (KB)",
};

function extractAllParameters(problems: ProblemFileList, problemTypes: ProblemTypeList, cells: ResultCell[]): string[] {
  const paramSet = new Set<string>();

  // Get unique problem names from cells (problems in this result)
  const resultProblemNames = new Set(cells.map((cell) => cell.problem));

  for (const [path, problem] of Object.entries(problems)) {
    if (!problem?.params) continue;

    // Only consider problems that are part of this result
    const matchesResult = Array.from(resultProblemNames).some((name) => path.includes(name));
    if (!matchesResult) continue;

    const typeSpec = problemTypes[problem.problem];
    if (!typeSpec) continue;

    for (const paramName of Object.keys(problem.params)) {
      const paramSpec = typeSpec.params[paramName];
      // Only include numeric parameters (integer or float)
      if (paramSpec && (paramSpec.type === "integer" || paramSpec.type === "float")) {
        paramSet.add(paramName);
      }
    }
  }

  return Array.from(paramSet).sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }));
}

function getParameterValue(problem: ProblemFileList[string], paramName: string): number | null {
  const value = problem?.params?.[paramName];
  if (value === undefined) return null;
  return typeof value === "number" ? value : null;
}

function prepareChartData(
  cells: ResultCell[],
  problems: ProblemFileList,
  prover: string,
  paramName: string,
  metric: ChartMetric,
): { labels: number[]; dataPoints: number[] } {
  const pointsMap = new Map<number, number[]>();

  for (const cell of cells) {
    if (cell.prover !== prover || !cell.stats) continue;

    // Find the problem data
    const problemEntry = Object.entries(problems).find(([path]) => path.includes(cell.problem));
    if (!problemEntry) continue;

    const [, problemData] = problemEntry;
    const paramValue = getParameterValue(problemData, paramName);
    if (paramValue === null) continue;

    const metricValue = cell.stats[metric];

    if (!pointsMap.has(paramValue)) {
      pointsMap.set(paramValue, []);
    }
    pointsMap.get(paramValue)!.push(metricValue);
  }

  // Calculate averages and sort by X value
  const sortedEntries = Array.from(pointsMap.entries())
    .map(([x, values]) => ({
      x,
      y: values.reduce((sum, v) => sum + v, 0) / values.length,
    }))
    .sort((a, b) => a.x - b.x);

  return {
    labels: sortedEntries.map((p) => p.x),
    dataPoints: sortedEntries.map((p) => p.y),
  };
}

function SingleChart({
  cells,
  problems,
  prover,
  paramName,
  metric,
  colorIndex,
}: Readonly<{
  cells: ResultCell[];
  problems: ProblemFileList;
  prover: string;
  paramName: string;
  metric: ChartMetric;
  colorIndex: number;
}>) {
  const { labels, dataPoints } = useMemo(
    () => prepareChartData(cells, problems, prover, paramName, metric),
    [cells, problems, prover, paramName, metric],
  );

  const color = CHART_COLORS[colorIndex % CHART_COLORS.length];

  const data = {
    labels: labels.map(String),
    datasets: [
      {
        label: prover,
        data: dataPoints,
        borderColor: color,
        backgroundColor: color.replace("rgb", "rgba").replace(")", ", 0.5)"),
        tension: 0.3,
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top" as const,
      },
      title: {
        display: true,
        text: `${prover} - ${METRIC_LABELS[metric]}`,
        font: {
          size: 14,
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: paramName,
        },
      },
      y: {
        title: {
          display: true,
          text: METRIC_LABELS[metric],
        },
        // For peak_memory, don't start at zero to show variations in the data
        beginAtZero: metric !== "peak_memory",
      },
    },
  };

  if (dataPoints.length === 0) {
    return (
      <div className="h-48 flex items-center justify-center bg-gray-50 rounded-sm border border-gray-200 text-gray-400 text-sm">
        No data for {prover} with parameter "{paramName}"
      </div>
    );
  }

  return (
    <div className="h-48">
      <Line data={data} options={options} />
    </div>
  );
}

const ResultCharts = ({ cells, provers, problems, problemTypes }: ResultChartsProps) => {
  const [selectedParam, setSelectedParam] = useState<string>("");
  const [showCharts, setShowCharts] = useState(false);

  const availableParams = useMemo(
    () => extractAllParameters(problems, problemTypes, cells),
    [problems, problemTypes, cells],
  );

  // Auto-select first parameter if none selected
  const effectiveParam = selectedParam || availableParams[0] || "";

  const handleGenerateCharts = () => {
    if (effectiveParam) {
      setShowCharts(true);
    }
  };

  const metrics: ChartMetric[] = ["system_time", "real_time", "peak_memory"];

  if (availableParams.length === 0) {
    return (
      <div className="mt-8 p-6 bg-gray-50 rounded-lg border border-gray-200 text-center text-gray-400">
        No numeric parameters available for charting. Generate problems with numeric parameters first.
      </div>
    );
  }

  return (
    <div className="mt-8">
      <div className="flex items-center gap-4 mb-6">
        <div className="flex items-center gap-2">
          <label htmlFor="param-select" className="text-sm font-medium text-gray-700">
            Parameter:
          </label>
          <select
            id="param-select"
            value={effectiveParam}
            onChange={(e) => {
              setSelectedParam(e.target.value);
              setShowCharts(false);
            }}
            className="border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-hidden bg-white min-w-[180px]"
          >
            {availableParams.map((param) => (
              <option key={param} value={param}>
                {param}
              </option>
            ))}
          </select>
        </div>
        <button
          onClick={handleGenerateCharts}
          disabled={!effectiveParam}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg font-medium shadow-sm transition-colors"
        >
          Generate Charts
        </button>
      </div>

      {showCharts && effectiveParam && (
        <div className="space-y-6 animate-in fade-in duration-300">
          {provers.map((prover, proverIndex) => (
            <div key={prover} className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">{prover}</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {metrics.map((metric) => (
                  <SingleChart
                    key={`${prover}-${metric}`}
                    cells={cells}
                    problems={problems}
                    prover={prover}
                    paramName={effectiveParam}
                    metric={metric}
                    colorIndex={proverIndex}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {!showCharts && (
        <div className="h-64 bg-gray-50 rounded-lg border border-gray-200 flex items-center justify-center text-gray-400">
          Select a parameter and click "Generate Charts" to view performance charts
        </div>
      )}
    </div>
  );
};

export default ResultCharts;
