import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useNotificationContext } from "./useNotificationContext";
import { useEffect } from "react";
import useMutationNotify from "./useMutationNotify";
import type { Problem } from "../types";
import { useActiveWorkspace } from "./useActiveWorkspace";

export type ProblemWithId = Problem & { id: string };

const queryKey = (workspace: string) => ["problems", workspace];

export default function useProblems(): {
  problems: ProblemWithId[];
  isLoading: boolean;
  generateProblem: (variables: { problem: string; params: any; seed?: number }) => void;
  deleteProblem: (id: string) => void;
} {
  const { showNotification } = useNotificationContext();
  const { workspace } = useActiveWorkspace();

  const query = useQuery({
    queryKey: queryKey(workspace || ""),
    queryFn: async (): Promise<ProblemWithId[]> => {
      if (!workspace) return [];
      const response = await axios.get(`/api/workspaces/${workspace}/problems`);
      const problemsMap = response.data.problems;
      return Object.entries(problemsMap).map(([path, data]) => ({
        ...(data as Problem),
        id: path,
      }));
    },
    enabled: !!workspace,
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
    mutationFn: async (variables: { problem: string; params: any; seed?: number }) => {
      if (!workspace) throw new Error("No active workspace");
      await axios.post(`/api/workspaces/${workspace}/problems`, variables);
    },
    queryKey: queryKey(workspace || ""),
    successMessage: "Problem generated successfully",
  });

  const remove = useMutationNotify({
    mutationFn: async (id: string) => {
      if (!workspace) throw new Error("No active workspace");
      await axios.delete(`/api/workspaces/${workspace}/problems`, { data: { path: id } });
    },
    queryKey: queryKey(workspace || ""),
    successMessage: "Problem deleted successfully",
  });

  return {
    problems: query.data || [],
    isLoading: query.isLoading,
    generateProblem: generate,
    deleteProblem: remove,
  };
}
