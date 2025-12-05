import type { ReactNode } from 'react';

interface SidebarTabProps {
  icon: ReactNode;
  label: string;
  active: boolean;
  onClick: () => void;
}

const SidebarTab = ({ icon, label, active, onClick }: SidebarTabProps) => (
  <button 
    onClick={(e) => {
      e.stopPropagation();
      onClick();
    }}
    className={`w-full flex items-center gap-2 p-2 text-sm rounded transition-colors ${
      active ? 'bg-blue-100 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-200'
    }`}
  >
    {icon}
    {label}
  </button>
);

export default SidebarTab;