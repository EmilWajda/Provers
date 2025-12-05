import { useState } from 'react';
import { Folder, ChevronDown, ChevronRight, Settings, Zap, BarChart, FileText, Trash2 } from 'lucide-react';
import type { Workspace, TabName } from '../../types';
import SidebarTab from './SidebarTab';

interface WorkspaceItemProps {
  workspace: Workspace;
  isActive: boolean;
  isExpanded: boolean;
  activeTab: TabName;
  onToggleExpand: () => void;
  onDeleteWorkspace: (id: string) => void;
  onSelectTab: (tab: TabName) => void;
}

const WorkspaceItem = ({ workspace, isActive, isExpanded, activeTab, onToggleExpand, onDeleteWorkspace, onSelectTab }: WorkspaceItemProps) => {
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  return (
    <div className="mb-2 group relative">
      <div className={`flex items-center gap-1 rounded-md transition-colors pr-1 ${
          isActive ? 'bg-white shadow-sm border border-gray-200' : 'hover:bg-gray-200'
        }`}>
        <button 
          onClick={onToggleExpand}
          className="flex-1 flex items-center gap-2 p-2 text-left overflow-hidden"
        >
          {isExpanded ? <ChevronDown size={16} className="text-gray-500 flex-shrink-0" /> : <ChevronRight size={16} className="text-gray-500 flex-shrink-0" />}
          <Folder size={18} className={isActive ? 'text-blue-600 flex-shrink-0' : 'text-gray-500 flex-shrink-0'} />
          <span className={`font-medium text-sm truncate ${isActive ? 'text-gray-900' : 'text-gray-600'}`}>
            {workspace.name}
          </span>
        </button>
        
        <button 
            onClick={(e) => { e.stopPropagation(); setShowDeleteConfirm(true); }}
            className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-md opacity-0 group-hover:opacity-100 transition-all"
            title="Delete Workspace"
        >
            <Trash2 size={14} />
        </button>
      </div>

      {isExpanded && (
        <div className="ml-4 mt-1 pl-4 border-l-2 border-gray-300 space-y-1">
          <SidebarTab icon={<Settings size={16} />} label="Settings" active={isActive && activeTab === 'settings'} onClick={() => onSelectTab('settings')} />
          <SidebarTab icon={<Zap size={16} />} label="Generator" active={isActive && activeTab === 'generator'} onClick={() => onSelectTab('generator')} />
          <SidebarTab icon={<BarChart size={16} />} label="Benchmark" active={isActive && activeTab === 'benchmark'} onClick={() => onSelectTab('benchmark')} />
          <SidebarTab icon={<FileText size={16} />} label="Results" active={isActive && activeTab === 'results'} onClick={() => onSelectTab('results')} />
        </div>
      )}

      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
           <div className="bg-white p-6 rounded-lg shadow-xl max-w-sm w-full mx-4 animate-zoom-in text-center">
              <h3 className="text-lg font-semibold mb-2 text-gray-900">Delete Workspace</h3>
              <p className="text-gray-600 mb-6">Do you want to delete <span className="font-medium text-gray-900">{workspace.name}</span>?</p>
              <div className="flex justify-center gap-3">
                 <button onClick={() => setShowDeleteConfirm(false)} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-md font-medium transition-colors">Cancel</button>
                 <button onClick={() => { onDeleteWorkspace(workspace.id); setShowDeleteConfirm(false); }} className="px-4 py-2 bg-red-600 text-white hover:bg-red-700 rounded-md font-medium transition-colors">Delete</button>
              </div>
           </div>
        </div>
      )}
    </div>
  );
};

export default WorkspaceItem;