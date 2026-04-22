import React, { useRef, useState, useEffect } from 'react'
import Globe from 'globe.gl'
import { useCountryStore } from '../../store/countryStore'

const COUNTRY_COORDS = {
  USA: [-95.7129, 37.0902], CHN: [104.1954, 35.8617], RUS: [105.3188, 61.524],
  IND: [78.9629, 20.5937], PAK: [69.3451, 30.3753], IRN: [53.688, 32.4279],
  ISR: [34.8516, 31.0461], TUR: [35.2433, 38.9637], SYR: [38.9968, 34.8021],
  UKR: [31.1656, 48.3794], VEN: [-67.7679, 8.506], NGA: [8.6753, 9.082],
  EGY: [30.8025, 26.8206], SAU: [45.0792, 23.8859], PRK: [127.5101, 40.3399],
  GBR: [-3.436, 55.3781], FRA: [2.2137, 46.2276], DEU: [10.4515, 51.1657],
  BRA: [-51.9253, -14.235], JPN: [138.2529, 36.2048]
}

const RISK_COLORS = {
  critical: '#ff3b3b',
  high: '#f59e0b', 
  medium: '#fbbf24',
  low: '#10b981'
}

function GlobeScene() {
  const globeEl = useRef()
  const globeRef = useRef(null)
  const { countries, selectCountry } = useCountryStore()
  const [arcs, setArcs] = useState([])

  useEffect(() => {
    if (!globeEl.current) return

    const pointsData = countries.map(c => ({
      lat: COUNTRY_COORDS[c.code]?.[1] || 0,
      lng: COUNTRY_COORDS[c.code]?.[0] || 0,
      country: c
    }))

    const globe = Globe()(globeEl.current)
      .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
      .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
      .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
      .pointsData(pointsData)
      .pointAltitude(0.02)
      .pointColor(d => {
        const risk = d.country.risk
        if (risk >= 70) return RISK_COLORS.critical
        if (risk >= 50) return RISK_COLORS.high
        if (risk >= 30) return RISK_COLORS.medium
        return RISK_COLORS.low
      })
      .pointRadius(d => 0.5 + (d.country.risk / 50))
      .onPointClick(d => selectCountry(d.country))
      .pointLabel(d => `
        <div style="background: rgba(13,17,23,0.95); padding: 8px 12px; 
                    border-radius: 6px; border: 1px solid #21262d; color: #e6edf3;
                    font-family: 'Space Grotesk', sans-serif;">
          <strong style="color: ${RISK_COLORS[d.country.risk >= 70 ? 'critical' : d.country.risk >= 50 ? 'high' : d.country.risk >= 30 ? 'medium' : 'low']}">
            ${d.country.name}
          </strong><br/>
          Risk Score: ${d.country.risk}/100
        </div>
      `)

    globeRef.current = globe

    const timer = setTimeout(() => {
      setArcs([
        {
          startLat: COUNTRY_COORDS['RUS']?.[1] || 0,
          startLng: COUNTRY_COORDS['RUS']?.[0] || 0,
          endLat: COUNTRY_COORDS['UKR']?.[1] || 0,
          endLng: COUNTRY_COORDS['UKR']?.[0] || 0,
          color: '#ff3b3b'
        },
        {
          startLat: COUNTRY_COORDS['PAK']?.[1] || 0,
          startLng: COUNTRY_COORDS['PAK']?.[0] || 0,
          endLat: COUNTRY_COORDS['IND']?.[1] || 0,
          endLng: COUNTRY_COORDS['IND']?.[0] || 0,
          color: '#f59e0b'
        }
      ])
    }, 1000)

    return () => {
      clearTimeout(timer)
    }
  }, [countries, selectCountry])

  useEffect(() => {
    if (globeRef.current && arcs.length > 0) {
      const globe = globeRef.current
      globe.arcsData(arcs)
      globe.arcColor('color')
      globe.arcAltitude(0.1)
      globe.arcStroke(1.5)
      globe.arcDashLength(0.5)
      globe.arcDashGap(0.2)
      globe.arcDashAnimateTime(2000)
    }
  }, [arcs])

  return (
    <div ref={globeEl} className="w-full h-full" />
  )
}

export default GlobeScene