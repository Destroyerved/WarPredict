import React from 'react'
import { useCountryStore } from '../../store/countryStore'

function RiskPanel() {
  const { countries, selectCountry, selectedCountry } = useCountryStore()
  
  const sortedCountries = [...countries].sort((a, b) => b.risk - a.risk)
  
  const getRiskColor = (risk) => {
    if (risk >= 70) return 'text-war-red'
    if (risk >= 50) return 'text-war-amber'
    if (risk >= 30) return 'text-yellow-400'
    return 'text-war-green'
  }
  
  const getRiskDot = (risk) => {
    if (risk >= 70) return 'bg-war-red'
    if (risk >= 50) return 'bg-war-amber'
    if (risk >= 30) return 'bg-yellow-400'
    return 'bg-war-green'
  }

  return (
    <div>
      <h2 className="font-display text-sm text-war-muted mb-4">HIGH RISK ZONES</h2>
      
      <div className="space-y-2">
        {sortedCountries.slice(0, 10).map(country => (
          <button
            key={country.code}
            onClick={() => selectCountry(country)}
            className={`w-full text-left p-3 rounded-lg border transition-all ${
              selectedCountry?.code === country.code
                ? 'border-war-blue bg-war-blue/10'
                : 'border-war-border hover:border-war-muted'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="font-medium text-sm">{country.code}</span>
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${getRiskDot(country.risk)}`}></span>
                <span className={`font-mono text-sm ${getRiskColor(country.risk)}`}>
                  {country.risk}
                </span>
              </div>
            </div>
            <div className="text-xs text-war-muted mt-1">{country.name}</div>
          </button>
        ))}
      </div>
      
      <div className="mt-6 p-3 bg-war-elevated rounded-lg">
        <h4 className="text-xs font-display text-war-muted mb-2">RISK LEVELS</h4>
        <div className="space-y-1 text-xs">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-war-red"></span>
            <span className="text-war-muted">Critical (70+)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-war-amber"></span>
            <span className="text-war-muted">High (50-69)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-yellow-400"></span>
            <span className="text-war-muted">Medium (30-49)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-war-green"></span>
            <span className="text-war-muted">Low (&lt;30)</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RiskPanel