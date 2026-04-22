import React, { useState } from 'react'
import { motion } from 'framer-motion'

const COUNTRIES = ['USA', 'CHN', 'RUS', 'IND', 'PAK', 'IRN', 'ISR', 'TUR', 'UKR', 'SYR']

function ScenarioBuilder() {
  const [scenario, setScenario] = useState({
    countryA: 'USA',
    countryB: 'CHN',
    militaryA: 50,
    militaryB: 50,
    economyA: 50,
    economyB: 50,
    alliancesA: [],
    alliancesB: [],
    nuclear: false
  })
  
  const [result, setResult] = useState(null)

  const runSimulation = () => {
    const milDiff = Math.abs(scenario.militaryA - scenario.militaryB)
    const ecoDiff = Math.abs(scenario.economyA - scenario.economyB)
    
    const baseDuration = 60 + (milDiff * 2) + (ecoDiff * 1.5)
    const duration = Math.floor(baseDuration * (0.7 + Math.random() * 0.6))
    
    const baseCasualties = (scenario.militaryA + scenario.militaryB) * 500
    const casualties = Math.floor(baseCasualties * (0.5 + Math.random()))
    
    const baseEconomic = (scenario.economyA + scenario.economyB) * 1e9 * (duration / 365)
    const economic = Math.floor(baseEconomic * (0.5 + Math.random()))
    
    const winnerA = 0.5 + (scenario.militaryA - scenario.militaryB) * 0.01
    const winner = scenario.militaryA > scenario.militaryB ? scenario.countryA : scenario.countryB
    
    const cascade = scenario.alliancesA.length > 0 || scenario.alliancesB.length > 0
    
    setResult({
      duration,
      casualties,
      economic,
      winner: Math.random() > 0.1 ? winner : 'Stalemate',
      probA: winnerA,
      cascade: cascade ? [...new Set([...scenario.alliancesA, ...scenario.alliancesB])] : [],
      nuclear: scenario.nuclear
    })
  }

  return (
    <div className="flex h-full">
      {/* Configuration Panel */}
      <div className="w-80 bg-war-surface border-r border-war-border p-6 overflow-y-auto">
        <h2 className="font-display text-lg text-war-cyan mb-6">SCENARIO BUILDER</h2>
        
        <div className="space-y-6">
          <div>
            <label className="block text-sm text-war-muted mb-2">Country A</label>
            <select
              value={scenario.countryA}
              onChange={e => setScenario({...scenario, countryA: e.target.value})}
              className="w-full bg-war-bg border border-war-border rounded-lg p-3 text-war-text"
            >
              {COUNTRIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          
          <div>
            <label className="block text-sm text-war-muted mb-2">Country B</label>
            <select
              value={scenario.countryB}
              onChange={e => setScenario({...scenario, countryB: e.target.value})}
              className="w-full bg-war-bg border border-war-border rounded-lg p-3 text-war-text"
            >
              {COUNTRIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-war-muted mb-2">Military A</label>
              <input
                type="range" min="0" max="100"
                value={scenario.militaryA}
                onChange={e => setScenario({...scenario, militaryA: parseInt(e.target.value)})}
                className="w-full"
              />
              <div className="text-center font-mono text-sm">{scenario.militaryA}</div>
            </div>
            <div>
              <label className="block text-xs text-war-muted mb-2">Military B</label>
              <input
                type="range" min="0" max="100"
                value={scenario.militaryB}
                onChange={e => setScenario({...scenario, militaryB: parseInt(e.target.value)})}
                className="w-full"
              />
              <div className="text-center font-mono text-sm">{scenario.militaryB}</div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-war-muted mb-2">Economy A</label>
              <input
                type="range" min="0" max="100"
                value={scenario.economyA}
                onChange={e => setScenario({...scenario, economyA: parseInt(e.target.value)})}
                className="w-full"
              />
              <div className="text-center font-mono text-sm">{scenario.economyA}</div>
            </div>
            <div>
              <label className="block text-xs text-war-muted mb-2">Economy B</label>
              <input
                type="range" min="0" max="100"
                value={scenario.economyB}
                onChange={e => setScenario({...scenario, economyB: parseInt(e.target.value)})}
                className="w-full"
              />
              <div className="text-center font-mono text-sm">{scenario.economyB}</div>
            </div>
          </div>
          
          <div>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={scenario.nuclear}
                onChange={e => setScenario({...scenario, nuclear: e.target.checked})}
                className="w-4 h-4"
              />
              <span className="text-sm">Nuclear Capabilities</span>
            </label>
          </div>
          
          <button
            onClick={runSimulation}
            className="w-full btn-primary"
          >
            Run Simulation
          </button>
        </div>
      </div>
      
      {/* Results Panel */}
      <div className="flex-1 p-6 overflow-y-auto">
        {result ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <h2 className="font-display text-lg">SIMULATION RESULTS</h2>
            
            <div className="grid grid-cols-3 gap-4">
              <div className="card text-center">
                <div className="text-xs text-war-muted mb-2">Duration</div>
                <div className="text-2xl font-mono">{result.duration} days</div>
              </div>
              <div className="card text-center">
                <div className="text-xs text-war-muted mb-2">Casualties</div>
                <div className="text-2xl font-mono text-war-red">{result.casualties.toLocaleString()}</div>
              </div>
              <div className="card text-center">
                <div className="text-xs text-war-muted mb-2">Economic Damage</div>
                <div className="text-2xl font-mono">${(result.economic / 1e9).toFixed(1)}B</div>
              </div>
            </div>
            
            <div className="card">
              <h3 className="font-display text-sm text-war-muted mb-4">PREDICTED OUTCOME</h3>
              <div className="flex items-center gap-8">
                <div className="flex-1">
                  <div className="text-sm text-war-muted">{scenario.countryA}</div>
                  <div className="h-2 bg-war-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-war-blue rounded-full"
                      style={{ width: `${result.probA * 100}%` }}
                    />
                  </div>
                  <div className="text-right text-sm">{Math.round(result.probA * 100)}%</div>
                </div>
                <div className="text-war-amber">VS</div>
                <div className="flex-1">
                  <div className="text-sm text-war-muted">{scenario.countryB}</div>
                  <div className="h-2 bg-war-border rounded-full overflow-hidden">
                    <div
                      className="h-full bg-war-red rounded-full"
                      style={{ width: `${(1 - result.probA) * 100}%` }}
                    />
                  </div>
                  <div className="text-right text-sm">{Math.round((1 - result.probA) * 100)}%</div>
                </div>
              </div>
            </div>
            
            {result.cascade.length > 0 && (
              <div className="card border-war-amber">
                <h3 className="font-display text-sm text-war-amber mb-2">ALLIANCE CASCADE</h3>
                <p className="text-war-muted text-sm">
                  Conflict triggers: {result.cascade.join(', ')}
                </p>
              </div>
            )}
            
            {result.nuclear && (
              <div className="card border-war-red">
                <h3 className="font-display text-sm text-war-red mb-2">NUCLEAR IMPACT</h3>
                <p className="text-war-muted text-sm">
                  Nuclear exchange dramatically increases casualties and shortens duration
                </p>
              </div>
            )}
          </motion.div>
        ) : (
          <div className="flex items-center justify-center h-full text-war-muted">
            Configure scenario and run simulation
          </div>
        )}
      </div>
    </div>
  )
}

export default ScenarioBuilder