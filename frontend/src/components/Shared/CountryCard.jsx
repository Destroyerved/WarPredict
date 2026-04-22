import React from 'react'

function CountryCard({ country }) {
  if (!country) return null
  
  const stats = [
    { label: 'GDP', value: '$' + (Math.random() * 20).toFixed(1) + 'T' },
    { label: 'Population', value: (Math.random() * 300).toFixed(0) + 'M' },
    { label: 'Military', value: (Math.random() * 5).toFixed(1) + '% GDP' },
    { label: 'Stability', value: Math.floor(Math.random() * 40 + 40) + '/100' }
  ]

  return (
    <div className="flex gap-6 h-full">
      <div className="w-48 flex-shrink-0">
        <div className="text-4xl font-display mb-2">{country.code}</div>
        <div className="text-lg text-war-text">{country.name}</div>
        <div className={`text-2xl font-mono mt-2 ${
          country.risk >= 70 ? 'text-war-red' :
          country.risk >= 50 ? 'text-war-amber' :
          'text-war-green'
        }`}>
          {country.risk}/100
        </div>
        <div className="text-xs text-war-muted mt-1">Risk Score</div>
      </div>
      
      <div className="flex-1 grid grid-cols-4 gap-4">
        {stats.map((stat, i) => (
          <div key={i} className="card flex flex-col justify-center">
            <div className="text-xs text-war-muted mb-1">{stat.label}</div>
            <div className="text-xl font-mono">{stat.value}</div>
          </div>
        ))}
      </div>
      
      <div className="w-64 border-l border-war-border pl-6">
        <h4 className="font-display text-sm text-war-muted mb-3">RECENT EVENTS</h4>
        <div className="space-y-2 text-xs">
          <div className="flex gap-2">
            <span className="text-war-red">●</span>
            <span className="text-war-text">Military exercises increased</span>
          </div>
          <div className="flex gap-2">
            <span className="text-war-amber">●</span>
            <span className="text-war-text">Diplomatic tensions noted</span>
          </div>
          <div className="flex gap-2">
            <span className="text-war-green">●</span>
            <span className="text-war-text">Trade negotiations ongoing</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CountryCard