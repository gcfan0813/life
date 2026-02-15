import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import QuantumLifeTimeline from './components/QuantumLifeTimeline'
import GenesisCharacterCreation from './components/GenesisCharacterCreation'
import Settings from './components/Settings'
import Navigation from './components/Navigation'
import ErrorBoundary from './components/ErrorBoundary'
import { useLifeStore } from './stores/lifeStore'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})

function App() {
  const { currentProfile, isInitialized, initialize } = useLifeStore()
  
  useEffect(() => {
    initialize()
  }, [initialize])

  if (!isInitialized) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-100">
        <div className="text-center space-y-3">
          <div className="relative inline-flex">
            <div className="animate-spin rounded-full h-16 w-16 border-[3px] border-indigo-500/30 border-t-indigo-400"></div>
            <div className="absolute inset-2 rounded-full bg-indigo-500/10 blur-xl" />
          </div>
          <div className="text-sm tracking-wide text-slate-300">正在加载无限人生系统...</div>
        </div>
      </div>
    )
  }

  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary>
        <Router>
          <div className="relative min-h-screen bg-slate-950 text-slate-50 overflow-x-hidden">
          {/* Background Elements */}
          <div className="pointer-events-none fixed inset-0 z-0">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(99,102,241,0.15),transparent_45%),radial-gradient(circle_at_80%_10%,rgba(14,165,233,0.18),transparent_40%),radial-gradient(circle_at_50%_80%,rgba(56,189,248,0.12),transparent_35%)]" />
            <div className="absolute inset-0 opacity-[0.03] bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]" />
          </div>

          <Navigation />
          
          <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
            <Routes>
              <Route 
                path="/" 
                element={currentProfile ? <QuantumLifeTimeline /> : <GenesisCharacterCreation />} 
              />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </main>
          
          {/* Decorative gradients */}
          <div className="pointer-events-none fixed top-0 left-0 w-full h-full overflow-hidden z-[-1]">
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-500/10 blur-[120px] rounded-full animate-pulse-slow" />
            <div className="absolute bottom-[10%] right-[-5%] w-[35%] h-[35%] bg-sky-500/10 blur-[100px] rounded-full animate-pulse-slow" style={{ animationDelay: '2s' }} />
            <div className="absolute top-[40%] left-[50%] w-[30%] h-[30%] bg-purple-500/5 blur-[150px] rounded-full animate-pulse-slow" style={{ animationDelay: '1s' }} />
          </div>

          </div>
        </Router>
      </ErrorBoundary>
    </QueryClientProvider>
  )



}

export default App