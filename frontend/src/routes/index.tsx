import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/')({ component: Home })

function Home() {
  return (
    <div className="grid gap-8 lg:grid-cols-[1.25fr_0.75fr] lg:items-center">
      <section className="space-y-6 py-6 lg:py-10">
        <div className="inline-flex items-center rounded-full border border-sky-200 bg-sky-50 px-4 py-2 text-sm font-medium text-sky-700 shadow-sm">
          Clerk autenticado e pronto para uso
        </div>

        <div className="space-y-4">
          <h1 className="max-w-3xl text-5xl font-semibold tracking-tight text-slate-950 sm:text-6xl">
            Organize arquivos com uma base de autenticação já integrada.
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-slate-600 sm:text-xl">
            Use os controles no topo para entrar ou criar uma conta. Depois, siga para a área
            autenticada para continuar a construção do fluxo de upload e gerenciamento.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          {[
            ['Login pronto', 'Fluxo de sign-in disponível para teste imediato.'],
            ['Cadastro visível', 'O botão de criação de conta aparece na navegação.'],
            ['Perfil do usuário', 'UserButton exibido quando a sessão está ativa.'],
          ].map(([title, body]) => (
            <div key={title} className="rounded-3xl border border-white/70 bg-white/85 p-5 shadow-sm backdrop-blur">
              <p className="text-base font-semibold text-slate-950">{title}</p>
              <p className="mt-2 text-sm leading-6 text-slate-600">{body}</p>
            </div>
          ))}
        </div>
      </section>

      <aside className="relative overflow-hidden rounded-[2rem] border border-slate-200 bg-slate-950 p-8 text-white shadow-2xl shadow-slate-950/20">
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/35 to-transparent" />
        <div className="absolute -right-20 top-10 h-48 w-48 rounded-full bg-sky-400/20 blur-3xl" />
        <div className="absolute -left-16 bottom-0 h-56 w-56 rounded-full bg-indigo-400/20 blur-3xl" />

        <div className="relative space-y-5">
          <p className="text-sm font-semibold uppercase tracking-[0.28em] text-sky-200/80">
            Próximos passos
          </p>
          <h2 className="text-2xl font-semibold tracking-tight">
            Teste a autenticação com a sua primeira conta.
          </h2>
          <p className="text-sm leading-7 text-slate-300">
            Entre ou crie uma conta pelo cabeçalho. Quando o avatar aparecer, a sessão já estará
            funcionando e você pode seguir com a navegação autenticada.
          </p>

          <div className="space-y-3 rounded-2xl border border-white/10 bg-white/5 p-4">
            <p className="text-sm font-medium text-white">Tudo que já está pronto</p>
            <ul className="space-y-2 text-sm leading-6 text-slate-300">
              <li>• Clerk Provider configurado no ponto de entrada.</li>
              <li>• Navegação pública com ações de entrada e cadastro.</li>
              <li>• Área autenticada protegida por sessão ativa.</li>
            </ul>
          </div>
        </div>
      </aside>
    </div>
  )
}
