import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { useNotificationContext } from "./useNotificationContext";
import { useEffect } from "react";

const QUERY_KEY = ["workspaces"];

export default function useWorkspaces(): {
  workspaces: string[];
  isLoading: boolean;
  createWorkspace: (name: string) => void;
  deleteWorkspace: (name: string) => void;
} {
  const queryClient = useQueryClient();
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

  const create = useMutation({
    mutationFn: async (name: string) => {
      await axios.post("/api/workspaces", { name });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEY });
      showNotification({
        type: "success",
        message: "Workspace created successfully",
      });
    },
    onError: (error: any) => {
      showNotification({
        type: "error",
        message: error?.response?.data?.error ?? error.message,
      });
      console.log(error);
    },
  });

  const remove = useMutation({
    mutationFn: async (name: string) => {
      await axios.delete("/api/workspaces", { data: { name } });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEY });
      showNotification({
        type: "success",
        message: "Workspace deleted successfully",
      });
    },
    onError: (error: any) => {
      showNotification({
        type: "error",
        message: error?.response?.data?.error ?? error.message,
      });
    },
  });

  return {
    workspaces: query.data || [],
    isLoading: query.isLoading,
    createWorkspace: create.mutate,
    deleteWorkspace: remove.mutate,
  };
}
