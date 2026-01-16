import { useState, type FormEvent } from "react";
import { Plus } from "lucide-react";

interface CreateWorkspaceProps {
  isLoading: boolean;
  onCreate: (name: string) => void;
}

const CreateWorkspace = ({ isLoading, onCreate }: CreateWorkspaceProps) => {
  const [isCreating, setIsCreating] = useState(false);
  const [name, setName] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      onCreate(name);
      setName("");
      setIsCreating(false);
    }
  };

  if (!isCreating) {
    return (
      <div className="p-4">
        <button
          onClick={() => setIsCreating(true)}
          className={`w-full flex items-center justify-center gap-2 ${
            isLoading ? "cursor-not-allowed bg-gray-600 hover:bg-gray-700" : "bg-blue-600 hover:bg-blue-700"
          } text-white py-2 px-4 rounded-lg transition-colors shadow-sm font-medium`}
          disabled={isLoading}
        >
          <Plus size={18} /> Create Workspace
        </button>
      </div>
    );
  }

  return (
    <div className="p-4">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-2 bg-white p-3 rounded-lg border border-gray-300 shadow-sm"
      >
        <input
          autoFocus
          type="text"
          placeholder="Workspace Name..."
          className="w-full border-b border-gray-300 focus:border-blue-500 outline-none text-sm py-1"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <div className="flex justify-end gap-2 mt-2">
          <button
            type="button"
            onClick={() => setIsCreating(false)}
            className="text-xs text-gray-500 hover:text-gray-700"
          >
            Cancel
          </button>
          <button type="submit" className="text-xs bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">
            Create
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateWorkspace;
