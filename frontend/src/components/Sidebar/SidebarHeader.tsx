import { Layers } from 'lucide-react';

const SidebarHeader = () => (
  <div className="p-4 border-b border-gray-200 bg-gray-50">
    <h1 className="text-xl font-bold text-gray-700 flex items-center gap-2">
      <Layers className="w-6 h-6 text-blue-600" />
      LOFT
    </h1>
  </div>
);

export default SidebarHeader;