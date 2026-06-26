import { api } from './api'
import type { ImageItem } from '../types/image.types'

export async function fetchImages(token: string | null): Promise<ImageItem[]> {
  const response = await api.get<ImageItem[]>('/images/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export async function uploadImage(token: string | null, file: File): Promise<ImageItem> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post<ImageItem>('/images/', formData, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response.data
}

export async function deleteImage(token: string | null, id: number): Promise<void> {
  await api.delete(`/images/${id}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}
