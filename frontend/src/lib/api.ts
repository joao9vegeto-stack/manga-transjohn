import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface UploadResponse {
  image_id: string
  filename: string
  path: string
}

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

export interface PipelineResponse {
  image_id: string
  project_id: string
  regions: Region[]
  texts: string[]
  translations: string[]
  output_path: string
  status: string
}

export interface Project {
  project_id: string
  image_id: string
  source_lang: string
  target_lang: string
  regions: Region[]
  texts: string[]
  translations: string[]
  deleted_regions: number[]
  ignored_regions: number[]
  created_at: string
  updated_at: string
}

export async function uploadImage(file: File): Promise<UploadResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await axios.post(`${API_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export async function runPipeline(
  imageId: string,
  sourceLang: string,
  coverMode: boolean = false,
  ignoredRegions: number[] = []
): Promise<PipelineResponse> {
  const response = await axios.post(`${API_URL}/pipeline`, {
    image_id: imageId,
    source_lang: sourceLang,
    cover_mode: coverMode,
    ignored_regions: ignoredRegions,
  })

  return response.data
}

export async function getProject(projectId: string): Promise<Project> {
  const response = await axios.get(`${API_URL}/project/${projectId}`)
  return response.data
}

export async function updateProject(
  projectId: string,
  regions: Region[],
  deletedRegions: number[] = [],
  ignoredRegions: number[] = []
): Promise<void> {
  await axios.post(`${API_URL}/project/update`, {
    project_id: projectId,
    regions,
    deleted_regions: deletedRegions,
    ignored_regions: ignoredRegions,
  })
}

export function getImageUrl(imageId: string, type: 'original' | 'inpainted' | 'output' = 'original'): string {
  return `${API_URL}/image/${imageId}?type=${type}`
}

export async function translateTexts(
  texts: string[],
  sourceLang: string
): Promise<string[]> {
  const response = await axios.post(`${API_URL}/translate`, {
    texts,
    source_lang: sourceLang,
    target_lang: 'pt-BR',
  })

  return response.data.translations
}
