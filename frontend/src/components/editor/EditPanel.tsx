import { useState, useEffect } from 'react'
import { Region } from '@/types'

interface EditPanelProps {
  region: Region
  originalText: string
  translatedText: string
  visible: boolean
  ignored: boolean
  onTranslationEdit: (text: string) => void
  onToggleVisible: () => void
  onToggleIgnore: () => void
  onDelete: () => void
}

export default function EditPanel({
  region,
  originalText,
  translatedText,
  visible,
  ignored,
  onTranslationEdit,
  onToggleVisible,
  onToggleIgnore,
  onDelete
}: EditPanelProps) {
  const [editText, setEditText] = useState(translatedText)

  useEffect(() => {
    setEditText(translatedText)
  }, [translatedText])

  const handleSave = () => {
    onTranslationEdit(editText)
  }

  return (
    <div className="mt-6 p-4 border-t">
      <h3 className="text-lg font-bold mb-4">Edit Region</h3>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">
            Original Text (Read-only)
          </label>
          <div className="p-2 bg-gray-100 border rounded text-sm">
            {originalText || '(no text detected)'}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Translated Text
          </label>
          <textarea
            value={editText}
            onChange={(e) => setEditText(e.target.value)}
            className="w-full p-2 border rounded resize-none"
            rows={4}
          />
          <button
            onClick={handleSave}
            className="mt-2 btn-primary text-sm"
          >
            Save Changes
          </button>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="visible"
              checked={visible}
              onChange={onToggleVisible}
              className="mr-2"
            />
            <label htmlFor="visible" className="text-sm">
              Show Translation
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="ignored"
              checked={ignored}
              onChange={onToggleIgnore}
              className="mr-2"
            />
            <label htmlFor="ignored" className="text-sm">
              Ignore Region
            </label>
          </div>
        </div>

        <div>
          <button
            onClick={onDelete}
            className="w-full btn-danger"
          >
            Delete Region
          </button>
        </div>

        <div className="text-xs text-gray-600">
          <p>Position: {region.bbox.x}, {region.bbox.y}</p>
          <p>Size: {region.bbox.width} × {region.bbox.height}</p>
        </div>
      </div>
    </div>
  )
}
