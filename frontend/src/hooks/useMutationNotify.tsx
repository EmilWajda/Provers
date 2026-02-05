import { useMutation, useQueryClient, type UseMutateFunction, type QueryKey } from "@tanstack/react-query";
import { useNotificationContext } from "./useNotificationContext";

export default function useMutationNotify<TData = unknown, TError = unknown, TVariables = void, TContext = unknown>({
  mutationFn,
  queryKey,
  successMessage,
  additionalOnSuccess = () => {},
}: {
  mutationFn: (variables: TVariables) => Promise<TData>;
  queryKey: QueryKey;
  successMessage: string;
  additionalOnSuccess?: (data: TData) => void;
}): UseMutateFunction<TData, TError, TVariables, TContext> {
  const queryClient = useQueryClient();
  const { showNotification } = useNotificationContext();

  const mutation = useMutation<TData, TError, TVariables, TContext>({
    mutationFn,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey });
      showNotification({
        type: "success",
        message: successMessage,
      });
      additionalOnSuccess(data);
    },
    onError: (error: any) => {
      showNotification({
        type: "error",
        message: error?.response?.data?.error ?? error.message,
      });
      console.log(error);
    },
  });
  return mutation.mutate;
}
