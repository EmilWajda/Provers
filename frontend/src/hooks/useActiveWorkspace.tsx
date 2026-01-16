import { createContext, useContext, useState } from "react";

type ActiveWorkspaceContextValue = {
  workspace: string | null;
  setWorkspace: (id: string | null) => void;
};

const ActiveWorkspaceContext = createContext<ActiveWorkspaceContextValue | undefined>(undefined);

export const ActiveWorkspaceProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const [workspace, setWorkspace] = useState<string | null>(null);
  return (
    <ActiveWorkspaceContext.Provider value={{ workspace, setWorkspace }}>
      {children}
    </ActiveWorkspaceContext.Provider>
  );
};

export function useActiveWorkspace(): ActiveWorkspaceContextValue {
  const ctx = useContext(ActiveWorkspaceContext);
  if (!ctx) {
    throw new Error("useActiveWorkspace must be used within an ActiveWorkspaceProvider");
  }
  return ctx;
}
