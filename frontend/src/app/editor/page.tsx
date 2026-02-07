'use client'

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import { runPipeline, getImageUrl, updateProject } from '@/lib/api'
import { Region, TranslationData, Tool, HistoryState } from '@/types'
import ImageCanvas from '@/components/editor/ImageCanvas'
import Toolbar from '@/components/editor/Toolbar'
import RegionList from '@/components/editor/RegionList'
import EditPanel from '@/components/editor/EditPanel'

export default function EditorPage() {
  const searchParams = useSearchParams()
  const imageId = searchParams.get('imageId')
  const sourceLang = searchParams.get('sourceLang') || 'ja'
  const coverMode = searchParams.get('coverMode') === 'true'

  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState(false)
  const [projectId, setProjectId] = useState<string | null>(null)
  const [regions, setRegions] = useState<Region[]>([])
  const [texts, setTexts] = useState<string[]>([])
  const [translations, setTranslations] = useState<string[]>([])
  const [deletedRegions, setDeletedRegions] = useState<Set<number>>(new Set())
  const [ignoredRegions, setIgnoredRegions] = useState<Set<number>>(new Set())
  const [selectedRegionId, setSelectedRegionId] = useState<number | null>(null)
  const [currentTool, setCurrentTool] = useState<Tool>('select')
  const [history, setHistory] = useState<HistoryState[]>([])
  const [historyIndex, setHistoryIndex] = useState(-1)

  useEffect(() => {
    if (imageId) {
      loadAndProcess()
    }
  }, [imageId])

  const loadAndProcess = async () => {
    if (!imageId) return

    setLoading(true)
    setProcessing(true)
    try {
      const result = await runPipeline(
        imageId,
        sourceLang,
        coverMode,
        Array.from(ignoredRegions)
      )

      setProjectId(result.project_id)
      setRegions(result.regions)
      setTexts(result.texts)
      setTranslations(result.translations)
      
      // Save initial state to history
      saveToHistory(result.translations, new Set())
    } catch (error) {
      console.error('Pipeline failed:', error)
      alert('Failed to process image. Please try again.')
    } finally {
      setLoading(false)
      setProcessing(false)
    }
  }

  const saveToHistory = (newTranslations: string[], newDeletedRegions: Set<number>) => {
    const newHistory = history.slice(0, historyIndex + 1)
    newHistory.push({
      translations: [...newTranslations],
      deletedRegions: new Set(newDeletedRegions)
    })
    setHistory(newHistory)
    setHistoryIndex(newHistory.length - 1)
  }

  const undo = () => {
    if (historyIndex > 0) {
      const prevState = history[historyIndex - 1]
      setTranslations(prevState.translations)
      setDeletedRegions(prevState.deletedRegions)
      setHistoryIndex(historyIndex - 1)
    }
  }

  const redo = () => {
    if (historyIndex < history.length - 1) {
      const nextState = history[historyIndex + 1]
      setTranslations(nextState.translations)
      setDeletedRegions(nextState.deletedRegions)
      setHistoryIndex(historyIndex + 1)
    }
  }

  const handleTranslationEdit = (regionId: number, newText: string) => {
    const newTranslations = [...translations]
    newTranslations[regionId] = newText
    setTranslations(newTranslations)
    saveToHistory(newTranslations, deletedRegions)
  }

  const handleRegionDelete = (regionId: number) => {
    const newDeletedRegions = new Set(deletedRegions)
    newDeletedRegions.add(regionId)
    setDeletedRegions(newDeletedRegions)
    saveToHistory(translations, newDeletedRegions)
    setSelectedRegionId(null)
  }

  const handleRegionToggle = (regionId: number) => {
    const newDeletedRegions = new Set(deletedRegions)
    if (newDeletedRegions.has(regionId)) {
      newDeletedRegions.delete(regionId)
    } else {
      newDeletedRegions.add(regionId)
    }
    setDeletedRegions(newDeletedRegions)
    saveToHistory(translations, newDeletedRegions)
  }

  const handleIgnoreToggle = (regionId: number) => {
    const newIgnoredRegions = new Set(ignoredRegions)
    if (newIgnoredRegions.has(regionId)) {
      newIgnoredRegions.delete(regionId)
    } else {
      newIgnoredRegions.add(regionId)
    }
    setIgnoredRegions(newIgnoredRegions)
  }

  const handleRerunTranslation = async () => {
    if (!imageId) return

    setProcessing(true)
    try {
      const result = await runPipeline(
        imageId,
        sourceLang,
        coverMode,
        Array.from(ignoredRegions)
      )

      // Preserve user edits
      const newTranslations = result.translations.map((t, i) => {
        if (deletedRegions.has(i)) {
          return translations[i] || t
        }
        return t
      })

      setRegions(result.regions)
      setTexts(result.texts)
      setTranslations(newTranslations)
      saveToHistory(newTranslations, deletedRegions)
    } catch (error) {
      console.error('Re-run failed:', error)
      alert('Failed to re-run translation.')
    } finally {
      setProcessing(false)
    }
  }

  const handleExportImage = () => {
    if (!imageId) return
    const url = getImageUrl(imageId, 'output')
    window.open(url, '_blank')
  }

  const handleExportProject = async () => {
    if (!projectId) return

    const projectData = {
      projectId,
      imageId,
      sourceLang,
      regions,
      texts,
      translations,
      deletedRegions: Array.from(deletedRegions),
      ignoredRegions: Array.from(ignoredRegions)
    }

    const blob = new Blob([JSON.stringify(projectData, null, 2)], {
      type: 'application/json'
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `manga-transjohn-${projectId}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const translationData: TranslationData[] = regions.map((region, i) => ({
    region,
    originalText: texts[i] || '',
    translatedText: translations[i] || '',
    visible: !deletedRegions.has(i)
  }))

  if (!imageId) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>No image selected</p>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl">Processing image...</p>
          <p className="text-sm text-gray-600 mt-2">
            Detecting text → OCR → Translating → Inpainting → Typesetting
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Left Toolbar */}
      <div className="w-64 bg-white shadow-lg p-4 overflow-y-auto">
        <Toolbar
          currentTool={currentTool}
          onToolChange={setCurrentTool}
          onUndo={undo}
          onRedo={redo}
          canUndo={historyIndex > 0}
          canRedo={historyIndex < history.length - 1}
          onRerun={handleRerunTranslation}
          onExportImage={handleExportImage}
          onExportProject={handleExportProject}
          processing={processing}
        />
      </div>

      {/* Center Canvas */}
      <div className="flex-1 p-4 overflow-hidden">
        <ImageCanvas
          imageUrl={getImageUrl(imageId, 'output')}
          regions={regions}
          translations={translationData}
          selectedRegionId={selectedRegionId}
          onRegionSelect={setSelectedRegionId}
          currentTool={currentTool}
        />
      </div>

      {/* Right Panel */}
      <div className="w-96 bg-white shadow-lg overflow-y-auto">
        <div className="p-4">
          <h2 className="text-xl font-bold mb-4">Regions</h2>
          <RegionList
            translations={translationData}
            selectedRegionId={selectedRegionId}
            onRegionSelect={setSelectedRegionId}
          />

          {selectedRegionId !== null && (
            <EditPanel
              region={regions[selectedRegionId]}
              originalText={texts[selectedRegionId]}
              translatedText={translations[selectedRegionId]}
              visible={!deletedRegions.has(selectedRegionId)}
              ignored={ignoredRegions.has(selectedRegionId)}
              onTranslationEdit={(text) => handleTranslationEdit(selectedRegionId, text)}
              onToggleVisible={() => handleRegionToggle(selectedRegionId)}
              onToggleIgnore={() => handleIgnoreToggle(selectedRegionId)}
              onDelete={() => handleRegionDelete(selectedRegionId)}
            />
          )}
        </div>
      </div>
    </div>
  )
}
