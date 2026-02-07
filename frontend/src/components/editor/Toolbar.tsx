import { Tool } from '@/types'

interface ToolbarProps {
  currentTool: Tool
  onToolChange: (tool: Tool) => void
  onUndo: () => void
  onRedo: () => void
  canUndo: boolean
  canRedo: boolean
  onRerun: () => void
  onExportImage: () => void
  onExportProject: () => void
  processing: boolean
}

export default function Toolbar({
  currentTool,
  onToolChange,
  onUndo,
  onRedo,
  canUndo,
  canRedo,
  onRerun,
  onExportImage,
  onExportProject,
  processing
}: ToolbarProps) {
  const tools: { id: Tool; name: string; icon: string }[] = [
    { id: 'select', name: 'Select', icon: '🔍' },
    { id: 'erase', name: 'Eraser', icon: '🧹' },
    { id: 'add-region', name: 'Add Region', icon: '➕' },
  ]

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold">Tools</h2>
      
      <div className="space-y-2">
        {tools.map((tool) => (
          <button
            key={tool.id}
            onClick={() => onToolChange(tool.id)}
            className={`w-full px-4 py-2 rounded flex items-center space-x-2 ${
              currentTool === tool.id
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 hover:bg-gray-300'
            }`}
          >
            <span className="text-xl">{tool.icon}</span>
            <span>{tool.name}</span>
          </button>
        ))}
      </div>

      <hr className="my-4" />

      <h3 className="text-md font-semibold">History</h3>
      <div className="flex space-x-2">
        <button
          onClick={onUndo}
          disabled={!canUndo}
          className="flex-1 btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ↶ Undo
        </button>
        <button
          onClick={onRedo}
          disabled={!canRedo}
          className="flex-1 btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ↷ Redo
        </button>
      </div>

      <hr className="my-4" />

      <h3 className="text-md font-semibold">Actions</h3>
      <div className="space-y-2">
        <button
          onClick={onRerun}
          disabled={processing}
          className="w-full btn-secondary disabled:opacity-50"
        >
          {processing ? 'Processing...' : '🔄 Re-run Translation'}
        </button>
        
        <button
          onClick={onExportImage}
          className="w-full btn-primary"
        >
          📥 Export Image
        </button>
        
        <button
          onClick={onExportProject}
          className="w-full btn-secondary"
        >
          💾 Export Project JSON
        </button>
      </div>
    </div>
  )
}
