import { useState, useEffect } from "react";
import SidebarHeader from "./SidebarHeader";
import CreateWorkspace from "./CreateWorkspace";
import WorkspaceItem from "./WorkspaceItem";
import type { TabName } from "../../types";

interface SidebarProps {
  workspaces: string[];
  activeWorkspaceId: string | null;
  activeTab: TabName;
  isLoading: boolean;
  onCreateWorkspace: (name: string) => void;
  onDeleteWorkspace: (id: string) => void;
  onSelectWorkspace: (id: string | null) => void;
  onSelectTab: (workspaceId: string, tab: TabName) => void;
}

const Sidebar = ({
  workspaces,
  activeWorkspaceId,
  activeTab,
  isLoading,
  onCreateWorkspace,
  onDeleteWorkspace,
  onSelectWorkspace,
  onSelectTab,
}: SidebarProps) => {
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (activeWorkspaceId) {
      setExpandedIds((prev) => {
        const newSet = new Set(prev);
        if (!newSet.has(activeWorkspaceId)) {
          newSet.add(activeWorkspaceId);
          return newSet;
        }
        return prev;
      });
    }
  }, [activeWorkspaceId]);

  const toggleExpansion = (id: string) => {
    const newSet = new Set(expandedIds);
    if (newSet.has(id)) {
      newSet.delete(id);
      if (id === activeWorkspaceId) {
        onSelectWorkspace(null);
      }
    } else {
      newSet.add(id);
    }
    setExpandedIds(newSet);
  };

  return (
    <div className="w-64 bg-gray-100 flex flex-col border-r border-gray-200 h-full flex-shrink-0">
      <SidebarHeader />
      <CreateWorkspace onCreate={onCreateWorkspace} isLoading={isLoading} />

      <div className="flex-1 overflow-y-auto px-2">
        {workspaces.map((ws) => (
          <WorkspaceItem
            key={ws}
            workspace={ws}
            isActive={ws === activeWorkspaceId}
            isExpanded={expandedIds.has(ws)}
            activeTab={activeTab}
            onToggleExpand={() => toggleExpansion(ws)}
            onDeleteWorkspace={onDeleteWorkspace}
            onSelectTab={(tab) => onSelectTab(ws, tab)}
          />
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
