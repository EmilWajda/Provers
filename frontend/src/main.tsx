import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { NotificationProvider } from "./hooks/useNotificationContext";
import { ActiveWorkspaceProvider } from "./hooks/useActiveWorkspace";

const queryClient = new QueryClient();

const rootElement = document.getElementById("root");
if (rootElement) {
  const root = createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <QueryClientProvider client={queryClient}>
        <NotificationProvider>
          <ActiveWorkspaceProvider>
            <App />
          </ActiveWorkspaceProvider>
        </NotificationProvider>
      </QueryClientProvider>
    </React.StrictMode>,
  );
}
