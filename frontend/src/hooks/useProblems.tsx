import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useNotificationContext } from "./useNotificationContext";
import { useEffect } from "react";
import useMutationNotify from "./useMutationNotify";
import type { Problem, ProblemFileList } from "../types";
import { useActiveWorkspace } from "./useActiveWorkspace";

const queryKey = (workspace: string | null) => ["problems", workspace || ""];

export default function useProblems(): {
  problems: ProblemFileList;
  isLoading: boolean;
  generateProblem: (problem: Problem) => void;
  deleteProblem: (path: string) => void;
  renameProblem: (path: string, newName: string) => void;
} {
  const { showNotification } = useNotificationContext();
  const { workspace } = useActiveWorkspace();

  const query = useQuery({
    queryKey: queryKey(workspace),
    queryFn: async (): Promise<ProblemFileList> => {
      const response = await axios.get(`/api/workspaces/${workspace}/problems`);
      return response.data.problems;
    },
  });

  useEffect(() => {
    if (query.isError) {
      showNotification({
        type: "error",
        message: "Failed to load problems",
      });
    }
  }, [query.isError]);

  const generate = useMutationNotify({
    mutationFn: async (problem: Problem) => {
      if (!workspace) throw new Error("No active workspace");
      await axios.post(`/api/workspaces/${workspace}/problems`, problem);
    },
    queryKey: queryKey(workspace),
    successMessage: "Problem generated successfully",
  });

  const rename = useMutationNotify({
    mutationFn: async ({ path, newName }: { path: string; newName: string }) => {
      if (!workspace) throw new Error("No active workspace");
      await axios.put(`/api/workspaces/${workspace}/problems`, { path, newName });
    },
    queryKey: queryKey(workspace),
    successMessage: "Problem renamed successfully",
  });

  const remove = useMutationNotify({
    mutationFn: async (path: string) => {
      if (!workspace) throw new Error("No active workspace");
      await axios.delete(`/api/workspaces/${workspace}/problems`, { data: { path } });
    },
    queryKey: queryKey(workspace),
    successMessage: "Problem deleted successfully",
  });

  return {
    problems: query.data || {},
    isLoading: query.isLoading,
    generateProblem: generate,
    deleteProblem: remove,
    renameProblem: (path: string, newName: string) => rename({ path, newName }),
  };
}
