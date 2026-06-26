import { createFileRoute } from '@tanstack/react-router'
import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { api } from '../services/api'

export const Route = createFileRoute('/')({
  component: Dashboard,
})

function Dashboard() {
  const [file, setFile] = useState<File | null>(null)

  const uploadMutation = useMutation({
    mutationFn: async (selectedFile: File) => {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await api.post('/images/', formData, {
        headers: {
          // Authorization: `Bearer ${token}`,
        },
      })
      return response.data
    },
    onSuccess: () => {
      alert('Upload realizado com sucesso no S3 (MiniStack)!')
      setFile(null) 
   },
    onError: (error) => {
      console.error('Erro no upload:', error)
      alert('Falha ao enviar a imagem.')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return
    uploadMutation.mutate(file)
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Seu Workspace</h1>
        <p className="text-slate-500">Faça o upload dos seus arquivos de imagem para a nuvem.</p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          
          <div className="flex w-full items-center justify-center">
            <label htmlFor="dropzone-file" className="flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 hover:bg-slate-100 transition">
              <div className="flex flex-col items-center justify-center pb-6 pt-5">
                <svg className="mb-4 h-8 w-8 text-slate-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                  <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
                </svg>
                <p className="mb-2 text-sm text-slate-500"><span className="font-semibold">Clique para fazer upload</span> ou arraste e solte</p>
                <p className="text-xs text-slate-500">SVG, PNG, JPG ou GIF</p>
              </div>
              <input 
                id="dropzone-file" 
                type="file" 
                className="hidden" 
                accept="image/*"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
            </label>
          </div>

          {file && (
            <div className="text-sm font-medium text-sky-600">
              Arquivo selecionado: {file.name}
            </div>
          )}

          <button
            type="submit"
            disabled={!file || uploadMutation.isPending}
            className="inline-flex justify-center rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white shadow-sm hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {uploadMutation.isPending ? 'Enviando para a nuvem...' : 'Fazer Upload'}
          </button>
        </form>
      </div>
    </div>
  )
}