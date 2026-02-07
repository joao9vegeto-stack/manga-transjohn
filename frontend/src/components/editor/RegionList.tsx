import { TranslationData } from '@/types'

interface RegionListProps {
  translations: TranslationData[]
  selectedRegionId: number | null
  onRegionSelect: (id: number) => void
}

export default function RegionList({
  translations,
  selectedRegionId,
  onRegionSelect
}: RegionListProps) {
  return (
    <div className="space-y-2 mb-4">
      {translations.map((data, idx) => (
        <div
          key={idx}
          onClick={() => onRegionSelect(idx)}
          className={`p-3 border rounded cursor-pointer transition-colors ${
            selectedRegionId === idx
              ? 'border-blue-600 bg-blue-50'
              : 'border-gray-300 hover:border-blue-400'
          } ${!data.visible ? 'opacity-50' : ''}`}
        >
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-semibold text-gray-600">
              Region #{idx + 1}
            </span>
            {!data.visible && (
              <span className="text-xs text-red-600">Hidden</span>
            )}
          </div>
          <div className="text-sm text-gray-800 truncate">
            {data.translatedText || '(empty)'}
          </div>
        </div>
      ))}
      
      {translations.length === 0 && (
        <p className="text-sm text-gray-500 text-center py-4">
          No regions detected
        </p>
      )}
    </div>
  )
}
