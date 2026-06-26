import { createFileRoute, redirect } from '@tanstack/react-router'
import { useState } from 'react'
import { useImagesQuery, useUploadMutation, useDeleteMutation } from '../services/image.queries'

export const Route = createFileRoute('/')({
  beforeLoad: ({ context }) => {
    if (!context.auth.isSignedIn) {
      throw redirect({ to: '/login' })
    }
  },
  component: Dashboard,
})

function Dashboard() {
  const [file, setFile] = useState<File | null>(null)

  const { data: images = [], isLoading: isLoadingImages } = useImagesQuery()
  const uploadMutation = useUploadMutation()
  const deleteMutation = useDeleteMutation()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log(file)
    if (!file) return
    uploadMutation.mutate(file, {
      onSuccess: () => setFile(null),
    })
  }

  const formatSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const handleDownload = async (url: string, filename: string) => {
    try {
      const response = await fetch(url)
      const blob = await response.blob()
      const blobUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = blobUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(blobUrl)
    } catch (error) {
      console.error('Erro ao baixar a imagem:', error)
      window.open(url, '_blank')
    }
  }


  return (
    <div className="space-y-12">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Seu Workspace</h1>
        <p className="text-slate-500">Gerencie seus arquivos de forma totalmente isolada e segura.</p>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="flex w-full items-center justify-center">
            <label htmlFor="dropzone-file" className="flex h-44 w-full cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-300 bg-slate-50 hover:bg-slate-100 transition">
              <div className="flex flex-col items-center justify-center pb-6 pt-5">
                <p className="mb-2 text-sm text-slate-500"><span className="font-semibold">Clique para selecionar imagem</span> ou arraste e solte</p>
                <p className="text-xs text-slate-400">Formatos aceitos: PNG, JPG, JPEG, GIF</p>
              </div>
              <input id="dropzone-file" type="file" className="hidden" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
            </label>
          </div>

          {file && <div className="text-sm font-semibold text-sky-600">Selecionado: {file.name}</div>}

          <button type="submit" disabled={!file || uploadMutation.isPending} className="inline-flex justify-center rounded-xl bg-slate-950 px-4 py-3 text-sm font-semibold text-white shadow-sm hover:bg-slate-800 disabled:opacity-50 transition">
            {uploadMutation.isPending ? 'Enviando para o S3...' : 'Fazer Upload'}
          </button>
        </form>
      </div>

      <div className="space-y-4">
        <h2 className="text-xl font-bold text-slate-950">Seus Arquivos Salvos</h2>

        {isLoadingImages ? (
          <div className="text-slate-500">Buscando seus arquivos na nuvem...</div>
        ) : images.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-200 p-8 text-center text-slate-400">
            Nenhum arquivo encontrado para a sua conta. Faça seu primeiro upload acima!
          </div>
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {images.map((img) => (
              <div key={img.id} className="group relative flex flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:shadow-md">

                <div className="aspect-video w-full overflow-hidden bg-slate-100">
                  <img src={img.url} alt={img.filename} className="h-full w-full object-cover transition duration-300 group-hover:scale-105" />
                </div>

                <div className="flex flex-1 flex-col p-4">
                  <div className="flex-1">
                    <p className="truncate text-sm font-semibold text-slate-900" title={img.filename}>{img.filename}</p>
                    <p className="text-xs text-slate-400 mt-0.5">{formatSize(img.size)}</p>
                    <p className="text-xs text-slate-400 mt-0.5">{new Date(img.created_at).toLocaleDateString()}</p>
                  </div>

                  <div className="mt-4 flex gap-2">
                    <a href={img.url} target="_blank" rel="noreferrer" className="inline-flex flex-1 items-center justify-center rounded-xl border border-slate-200 bg-white px-2 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition">
                      Ver
                    </a>

                    <button type="button" onClick={() => handleDownload(img.url, img.filename)} className="inline-flex flex-1 items-center justify-center rounded-xl border border-sky-200 bg-sky-50 px-2 py-2 text-xs font-semibold text-sky-700 hover:bg-sky-100 transition">
                      Baixar
                    </button>

                    <button type="button" disabled={deleteMutation.isPending} onClick={() => { if (confirm('Excluir arquivo permanentemente da nuvem?')) deleteMutation.mutate(img.id) }} className="inline-flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-xl border border-red-200 bg-red-50 text-red-600 hover:bg-red-100 disabled:opacity-50 transition" title="Deletar Arquivo">
                      <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}