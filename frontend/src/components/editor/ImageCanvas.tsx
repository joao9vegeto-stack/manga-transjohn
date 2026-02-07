import { useRef, useEffect, useState } from 'react'
import { Region, TranslationData, Tool } from '@/types'

interface ImageCanvasProps {
  imageUrl: string
  regions: Region[]
  translations: TranslationData[]
  selectedRegionId: number | null
  onRegionSelect: (id: number | null) => void
  currentTool: Tool
}

export default function ImageCanvas({
  imageUrl,
  regions,
  translations,
  selectedRegionId,
  onRegionSelect,
  currentTool
}: ImageCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const [imageLoaded, setImageLoaded] = useState(false)
  const [scale, setScale] = useState(1)

  useEffect(() => {
    const canvas = canvasRef.current
    const container = containerRef.current
    if (!canvas || !container) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const img = new Image()
    img.crossOrigin = 'anonymous'
    img.src = imageUrl

    img.onload = () => {
      // Calculate scale to fit in container
      const containerWidth = container.clientWidth
      const containerHeight = container.clientHeight
      const scaleX = containerWidth / img.width
      const scaleY = containerHeight / img.height
      const newScale = Math.min(scaleX, scaleY, 1)
      
      setScale(newScale)
      
      canvas.width = img.width * newScale
      canvas.height = img.height * newScale
      
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
      
      // Draw region overlays
      drawRegions(ctx, newScale)
      setImageLoaded(true)
    }
  }, [imageUrl])

  useEffect(() => {
    if (!imageLoaded) return
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Redraw when regions or selection changes
    const img = new Image()
    img.crossOrigin = 'anonymous'
    img.src = imageUrl
    img.onload = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
      drawRegions(ctx, scale)
    }
  }, [regions, selectedRegionId, translations, scale])

  const drawRegions = (ctx: CanvasRenderingContext2D, scale: number) => {
    translations.forEach((data, idx) => {
      if (!data.visible) return

      const bbox = data.region.bbox
      
      ctx.save()
      
      // Draw bounding box
      ctx.strokeStyle = selectedRegionId === idx ? '#3B82F6' : '#10B981'
      ctx.lineWidth = selectedRegionId === idx ? 3 : 2
      ctx.strokeRect(
        bbox.x * scale,
        bbox.y * scale,
        bbox.width * scale,
        bbox.height * scale
      )
      
      // Draw region number
      ctx.fillStyle = selectedRegionId === idx ? '#3B82F6' : '#10B981'
      ctx.font = `${14 * scale}px Arial`
      ctx.fillText(
        `#${idx + 1}`,
        bbox.x * scale + 5,
        bbox.y * scale + 15 * scale
      )
      
      ctx.restore()
    })
  }

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current
    if (!canvas) return

    const rect = canvas.getBoundingClientRect()
    const x = (e.clientX - rect.left) / scale
    const y = (e.clientY - rect.top) / scale

    // Find clicked region
    for (let i = regions.length - 1; i >= 0; i--) {
      const bbox = regions[i].bbox
      if (
        x >= bbox.x &&
        x <= bbox.x + bbox.width &&
        y >= bbox.y &&
        y <= bbox.y + bbox.height &&
        translations[i].visible
      ) {
        onRegionSelect(i)
        return
      }
    }

    // Clicked outside regions
    onRegionSelect(null)
  }

  return (
    <div
      ref={containerRef}
      className="w-full h-full flex items-center justify-center bg-gray-200 rounded overflow-auto"
    >
      <canvas
        ref={canvasRef}
        onClick={handleCanvasClick}
        className="cursor-pointer shadow-lg"
        style={{
          maxWidth: '100%',
          maxHeight: '100%',
          cursor: currentTool === 'erase' ? 'crosshair' : 'pointer'
        }}
      />
    </div>
  )
}
