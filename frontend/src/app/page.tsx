'use client'

import { useState, useRef, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { uploadImage } from '@/lib/api'

const LANGUAGES = [
  { code: 'ja', name: 'Japanese (日本語)' },
  { code: 'ko', name: 'Korean (한국어)' },
  { code: 'zh-CN', name: 'Chinese Simplified (简体中文)' },
  { code: 'zh-TW', name: 'Chinese Traditional (繁體中文)' },
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Spanish (Español)' },
  { code: 'fr', name: 'French (Français)' },
]

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [sourceLang, setSourceLang] = useState('ja')
  const [coverMode, setCoverMode] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const router = useRouter()

  const handleFileSelect = (file: File) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    }
  }

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    
    const file = e.dataTransfer.files[0]
    handleFileSelect(file)
  }, [])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
  }, [])

  const handlePaste = useCallback((e: ClipboardEvent) => {
    const items = e.clipboardData?.items
    if (!items) return

    for (let i = 0; i < items.length; i++) {
      if (items[i].type.startsWith('image/')) {
        const file = items[i].getAsFile()
        if (file) {
          handleFileSelect(file)
        }
        break
      }
    }
  }, [])

  useState(() => {
    document.addEventListener('paste', handlePaste as any)
    return () => {
      document.removeEventListener('paste', handlePaste as any)
    }
  })

  const handleTranslate = async () => {
    if (!selectedFile) return

    setUploading(true)
    try {
      const result = await uploadImage(selectedFile)
      
      // Navigate to editor with image_id and settings
      router.push(
        `/editor?imageId=${result.image_id}&sourceLang=${sourceLang}&coverMode=${coverMode}`
      )
    } catch (error) {
      console.error('Upload failed:', error)
      alert('Failed to upload image. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-2">Manga TransJohn</h1>
        <p className="text-center text-gray-600 mb-8">
          Traduza manga/manhwa para Português (Brasil)
        </p>

        <div
          className={`drop-zone ${dragOver ? 'drag-over' : ''} p-12 text-center mb-6`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => fileInputRef.current?.click()}
        >
          {previewUrl ? (
            <div className="space-y-4">
              <img
                src={previewUrl}
                alt="Preview"
                className="max-h-96 mx-auto rounded"
              />
              <p className="text-sm text-gray-600">{selectedFile?.name}</p>
            </div>
          ) : (
            <div className="space-y-4">
              <svg
                className="mx-auto h-16 w-16 text-gray-400"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
              >
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <div className="text-gray-600">
                <p className="text-lg font-semibold">
                  Arraste uma imagem aqui
                </p>
                <p className="text-sm mt-2">
                  ou clique para selecionar, ou Cole (Ctrl+V)
                </p>
              </div>
            </div>
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => {
              const file = e.target.files?.[0]
              if (file) handleFileSelect(file)
            }}
          />
        </div>

        {selectedFile && (
          <div className="space-y-4 bg-white p-6 rounded-lg shadow">
            <div>
              <label className="block text-sm font-medium mb-2">
                Idioma de Origem
              </label>
              <select
                value={sourceLang}
                onChange={(e) => setSourceLang(e.target.value)}
                className="w-full border rounded px-3 py-2"
              >
                {LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Idioma de Destino
              </label>
              <input
                type="text"
                value="Português (Brasil)"
                disabled
                className="w-full border rounded px-3 py-2 bg-gray-100"
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="coverMode"
                checked={coverMode}
                onChange={(e) => setCoverMode(e.target.checked)}
                className="mr-2"
              />
              <label htmlFor="coverMode" className="text-sm">
                Modo Capa (ignora títulos grandes/estilizados)
              </label>
            </div>

            <button
              onClick={handleTranslate}
              disabled={uploading}
              className="w-full btn-primary disabled:opacity-50"
            >
              {uploading ? 'Enviando...' : 'Traduzir'}
            </button>
          </div>
        )}

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Usando Gemini 2.5 Flash para tradução</p>
          <p>Fonte: WildWorlds</p>
        </div>
      </div>
    </main>
  )
}
