import { Link, createRootRouteWithContext, Outlet } from '@tanstack/react-router'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import type { QueryClient } from '@tanstack/react-query'
import { Show, SignInButton, SignUpButton, UserButton } from '@clerk/react'
import type { useAuth } from '@clerk/react'

export const Route = createRootRouteWithContext<{
  queryClient: QueryClient
  auth: ReturnType<typeof useAuth>
}>()({
  component: RootLayout,
  notFoundComponent: () => (
    <div className="grid min-h-[60vh] place-items-center text-center">
      <div>
        <p className="text-6xl font-bold text-slate-300">404</p>
        <p className="mt-2 text-lg font-medium text-slate-500">Página não encontrada</p>
        <Link to="/" className="mt-6 inline-flex items-center rounded-full bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:-translate-y-0.5 hover:bg-slate-800">
          Voltar ao início
        </Link>
      </div>
    </div>
  ),
})

function RootLayout() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(59,130,246,0.16),_transparent_32%),linear-gradient(180deg,#f8fafc_0%,#eef2ff_45%,#f8fafc_100%)] text-slate-900">
      <header className="sticky top-0 z-20 border-b border-white/70 bg-white/75 backdrop-blur-xl">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-4 px-5 py-4 sm:px-6 lg:px-8">
          <Link to="/" className="group flex items-center gap-3">
            <span className="grid h-11 w-11 place-items-center rounded-2xl bg-slate-950 text-sm font-semibold text-white shadow-lg shadow-slate-950/20 transition-transform duration-300 group-hover:-translate-y-0.5">
              GA
            </span>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-500">
                Arquivos
              </p>
              <p className="text-lg font-semibold tracking-tight text-slate-950">
                Gerenciador de Arquivos
              </p>
            </div>
          </Link>

          <div className="flex items-center gap-3">
            <Show when="signed-out">
              <div className="flex items-center gap-3">
                <SignInButton mode="modal">
                  <button
                    type="button"
                    className="inline-flex h-11 items-center rounded-full border border-slate-300 bg-white px-5 text-sm font-semibold text-slate-700 shadow-sm transition hover:-translate-y-0.5 hover:border-slate-400 hover:text-slate-950"
                  >
                    Entrar
                  </button>
                </SignInButton>

                <SignUpButton mode="modal">
                  <button
                    type="button"
                    className="inline-flex h-11 items-center rounded-full bg-slate-950 px-5 text-sm font-semibold text-white shadow-lg shadow-slate-950/20 transition hover:-translate-y-0.5 hover:bg-slate-800"
                  >
                    Criar conta
                  </button>
                </SignUpButton>
              </div>
            </Show>

            <Show when="signed-in">
              <div className="flex items-center gap-3 rounded-full border border-slate-200 bg-white px-3 py-2 shadow-sm">
                <span className="hidden text-sm font-medium text-slate-600 sm:inline">
                  Conta ativa
                </span>
                <UserButton />
              </div>
            </Show>
          </div>
        </div>
      </header>

      <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col px-5 py-8 sm:px-6 lg:px-8 lg:py-10">
        <Outlet />
      </main>

      <ReactQueryDevtools buttonPosition="bottom-left" />
    </div>
  )
}