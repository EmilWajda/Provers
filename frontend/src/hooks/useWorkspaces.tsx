import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

const QUERY_KEY = ["workspaces"];

export default function useWorkspaces(): {
  workspaces: string[];
  isLoading: boolean;
  createWorkspace: (name: string) => void;
  deleteWorkspace: (name: string) => void;
} {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: QUERY_KEY,
    queryFn: async (): Promise<string[]> => {
      const response = await axios.get("/api/workspaces");
      return response.data.workspaces;
    },
  });

  const create = useMutation({
    mutationFn: async (name: string) => {
      await axios.post("/api/workspaces", { name });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEY });
    },
    onError: (error) => {
      console.error("Error creating workspace:", error);
    },
  });

  const remove = useMutation({
    mutationFn: async (name: string) => {
      await axios.delete("/api/workspaces", { data: { name } });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEY });
    },
    onError: (error) => {
      console.error("Error deleting workspace:", error);
    },
  });

  return {
    workspaces: query.data || [],
    isLoading: query.isLoading,
    createWorkspace: create.mutate,
    deleteWorkspace: remove.mutate,
  };
}
