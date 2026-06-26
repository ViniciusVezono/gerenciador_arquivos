import { createFileRoute } from '@tanstack/react-router'
import { SignIn } from '@clerk/react'

export const Route = createFileRoute('/login')({
  component: () => (
    <div className="grid min-h-[calc(100vh-8rem)] place-items-center py-10">
      <div className="w-full max-w-115 rounded-4xl border border-slate-200 bg-white p-4 shadow-2xl shadow-slate-950/10">
        <SignIn routing="path" path="/login" fallbackRedirectUrl="/" />
      </div>
    </div>
  ),
})