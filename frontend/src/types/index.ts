export interface Region {
  id: number
  bbox: {
    x: number
    y: number
    width: number
    height: number
  }
  polygon: number[][]
  area: number
}

export interface TranslationData {
  region: Region
  originalText: string
  translatedText: string
  visible: boolean
}

export interface EditorState {
  imageId: string
  projectId: string | null
  regions: Region[]
  texts: string[]
  translations: string[]
  deletedRegions: Set<number>
  ignoredRegions: Set<number>
  selectedRegionId: number | null
}

export type Tool = 'select' | 'erase' | 'add-region'

export interface HistoryState {
  translations: string[]
  deletedRegions: Set<number>
}
