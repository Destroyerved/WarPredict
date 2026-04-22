import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import GlobeScene from './components/Globe/GlobeScene'
import RiskPanel from './components/Dashboard/RiskPanel'
import CountryCard from './components/Shared/CountryCard'
import ScenarioBuilder from './components/Simulator/ScenarioBuilder'
import { useCountryStore } from './store/countryStore'

function App() {
  const [activeTab, setActiveTab] = useState('overview')
  const { selectedCountry, riskData } = useCountryStore()

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '🌍' },
    { id: 'simulator', label: 'Simulator', icon: '⚔️' },
    { id: 'explorer', label: 'Explorer', icon: '📊' },
    { id: 'intelligence', label: 'Intelligence', icon: '📰' }
  ]

  return (
    <div className="min-h-screen bg-war-bg">
      {/* Header */}
      <header className="h-14 bg-war-surface border-b border-war-border flex items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🎯</span>
          <h1 className="text-lg font-display text-war-cyan">WAR PREDICTION SYSTEM</h1>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-xs font-mono">
            <span className="w-2 h-2 rounded-full bg-war-green animate-pulse"></span>
            <span className="text-war-green">LIVE</span>
          </div>
          <button className="text-war-muted hover:text-war-text text-sm">?</button>
        </div>
      </header>

      {/* Navigation */}
      <nav className="h-12 bg-war-elevated border-b border-war-border flex items-center px-6 gap-2">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 text-sm font-medium rounded-md transition-all ${
              activeTab === tab.id
                ? 'bg-war-blue/20 text-war-blue'
                : 'text-war-muted hover:text-war-text hover:bg-war-surface'
            }`}
          >
            <span className="mr-2">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Main Content */}
      <main className="flex h-[calc(100vh-56px-48px)]">
        {/* Sidebar */}
        <aside className="w-72 bg-war-surface border-r border-war-border p-4 overflow-y-auto">
          <RiskPanel />
        </aside>

        {/* Main Canvas */}
        <section className="flex-1 flex flex-col">
          <div className="flex-1 relative">
            {activeTab === 'overview' && <GlobeScene />}
            {activeTab === 'simulator' && <ScenarioBuilder />}
            {activeTab === 'explorer' && (
              <div className="flex items-center justify-center h-full text-war-muted">
                Conflict Explorer - Coming Soon
              </div>
            )}
            {activeTab === 'intelligence' && (
              <div className="flex items-center justify-center h-full text-war-muted">
                Intelligence Feed - Coming Soon
              </div>
            )}
          </div>

          {/* Bottom Panel */}
          {selectedCountry && activeTab === 'overview' && (
            <div className="h-64 border-t border-war-border bg-war-surface p-4">
              <CountryCard country={selectedCountry} />
            </div>
          )}
        </section>

        {/* Right Panel */}
        <aside className="w-80 bg-war-surface border-l border-war-border p-4 overflow-y-auto">
          <h3 className="font-display text-sm text-war-muted mb-4">RISK BREAKDOWN</h3>
          
          {riskData && (
            <div className="space-y-3">
              {riskData.factors?.map((factor, i) => (
                <div key={i} className="card">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-war-text">{factor.name}</span>
                    <span className={factor.value > 50 ? 'text-war-red' : 'text-war-green'}>
                      {factor.value}%
                    </span>
                  </div>
                  <div className="h-1 bg-war-border rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        factor.value > 50 ? 'bg-war-red' : 'bg-war-green'
                      }`}
                      style={{ width: `${factor.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}

          {!riskData && (
            <p className="text-war-muted text-sm">Select a country on the globe to view risk factors</p>
          )}
        </aside>
      </main>
    </div>
  )
}

export default App