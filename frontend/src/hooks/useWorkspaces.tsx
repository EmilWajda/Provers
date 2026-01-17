import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useNotificationContext } from "./useNotificationContext";
import { useEffect } from "react";
import useMutationNotify from "./useMutationNotify";

const QUERY_KEY = ["workspaces"];

export default function useWorkspaces(): {
  workspaces: string[];
  isLoading: boolean;
  createWorkspace: (name: string) => void;
  deleteWorkspace: (name: string) => void;
} {
  const { showNotification } = useNotificationContext();

  const query = useQuery({
    queryKey: QUERY_KEY,
    queryFn: async (): Promise<string[]> => {
      const response = await axios.get("/api/workspaces");
      return response.data.workspaces;
    },
  });

  useEffect(() => {
    if (query.isError) {
      showNotification({
        type: "error",
        message: "Failed to load workspaces",
      });
    }
  }, [query.isError]);

  const create = useMutationNotify({
    mutationFn: async (name: string) => {
      await axios.post("/api/workspaces", { name });
    },
    queryKey: QUERY_KEY,
    successMessage: "Workspace created successfully",
  });

  const remove = useMutationNotify({
    mutationFn: async (name: string) => {
      await axios.delete("/api/workspaces", { data: { name } });
    },
    queryKey: QUERY_KEY,
    successMessage: "Workspace deleted successfully",
  });

  return {
    workspaces: query.data || [],
    isLoading: query.isLoading,
    createWorkspace: create,
    deleteWorkspace: remove,
  };
}
