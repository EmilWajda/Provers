import { useState } from "react";
import { Zap, Plus } from "lucide-react";
import type { ProblemParams, WorkspaceSettings } from "../../types";
import CreateProblemModal from "./CreateProblemModal";
import ProblemList from "./ProblemList";
import useProblems from "../../hooks/useProblems";
import { useActiveWorkspace } from "../../hooks/useActiveWorkspace";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

function getRandomSeed() {
  return Math.floor(Math.random() * (2 ** 32 - 1));
}

const GeneratorView = () => {
  const activeWorkspace = useActiveWorkspace().workspace;
  const { problems, generateProblem, deleteProblem } = useProblems();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const settings = useQuery({
    queryKey: ["settings", activeWorkspace],
    queryFn: async (): Promise<WorkspaceSettings> => {
      const response = await axios.get(`/api/workspaces/${activeWorkspace}/settings`);
      return response.data;
    },
  });

  const handleGenerate = (type: string, params: ProblemParams) => {
    generateProblem({ problem: type, params, seed: settings.data?.seed || getRandomSeed() });
    setIsModalOpen(false);
  };

  return (
    <div className="p-8 h-full flex flex-col">
      <div className="flex justify-between items-center mb-8 border-b pb-4">
        <h2 className="text-3xl font-bold text-gray-800 flex items-center gap-3">
          <Zap className="text-yellow-500 w-8 h-8" /> Generator
        </h2>
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium shadow-md transition-colors flex items-center gap-2"
        >
          <Plus size={20} /> Generate Problems
        </button>
      </div>

      <ProblemList problems={problems} onDeleteProblem={deleteProblem} />

      {isModalOpen && <CreateProblemModal onClose={() => setIsModalOpen(false)} onGenerate={handleGenerate} />}
    </div>
  );
};

export default GeneratorView;
