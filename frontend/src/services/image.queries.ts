import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useAuth } from '@clerk/react'
import { fetchImages, uploadImage, deleteImage } from './image.service'

const IMAGE_QUERY_KEY = ['images'] as const

export function useImagesQuery() {
  const { getToken } = useAuth()

  return useQuery({
    queryKey: IMAGE_QUERY_KEY,
    queryFn: async () => {
      const token = await getToken({ skipCache: true })
      return fetchImages(token)
    },
    staleTime: Infinity,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
  })
}

export function useUploadMutation() {
  const { getToken } = useAuth()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (file: File) => {
      const token = await getToken({ skipCache: true })
      return uploadImage(token, file)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: IMAGE_QUERY_KEY })
    },
    onError: (error) => console.error(error),
  })
}

export function useDeleteMutation() {
  const { getToken } = useAuth()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken({ skipCache: true })
      return deleteImage(token, id)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: IMAGE_QUERY_KEY })
    },
    onError: () => alert('Erro ao tentar deletar o arquivo.'),
  })
}
