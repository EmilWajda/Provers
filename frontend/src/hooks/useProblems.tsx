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
  };
}
