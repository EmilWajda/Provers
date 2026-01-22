import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useNotificationContext } from "./useNotificationContext";
import { useEffect } from "react";
import type { ProblemTypeList } from "../types";

const QUERY_KEY = ["problemTypes"];

export default function useProblemTypes(): {
  problemTypes: ProblemTypeList;
  isLoading: boolean;
} {
  const { showNotification } = useNotificationContext();

  const query = useQuery({
    queryKey: QUERY_KEY,
    queryFn: async (): Promise<ProblemTypeList> => {
      const response = await axios.get("/api/problems");
      return response.data.problems;
    },
  });

  useEffect(() => {
    if (query.isError) {
      showNotification({
        type: "error",
        message: "Failed to load problem types",
      });
    }
  }, [query.isError]);

  return {
    problemTypes: query.data || {},
    isLoading: query.isLoading,
  };
}
