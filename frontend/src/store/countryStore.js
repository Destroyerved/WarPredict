import { create } from 'zustand'

const useCountryStore = create((set) => ({
  selectedCountry: null,
  riskData: null,
  countries: [
    { code: 'USA', name: 'United States', risk: 15 },
    { code: 'CHN', name: 'China', risk: 25 },
    { code: 'RUS', name: 'Russia', risk: 45 },
    { code: 'IND', name: 'India', risk: 35 },
    { code: 'PAK', name: 'Pakistan', risk: 72 },
    { code: 'IRN', name: 'Iran', risk: 65 },
    { code: 'ISR', name: 'Israel', risk: 58 },
    { code: 'TUR', name: 'Turkey', risk: 38 },
    { code: 'SYR', name: 'Syria', risk: 85 },
    { code: 'UKR', name: 'Ukraine', risk: 78 },
    { code: 'VEN', name: 'Venezuela', risk: 55 },
    { code: 'NGA', name: 'Nigeria', risk: 48 },
    { code: 'EGY', name: 'Egypt', risk: 42 },
    { code: 'SAU', name: 'Saudi Arabia', risk: 32 },
    { code: 'PRK', name: 'North Korea', risk: 68 },
  ],
  
  selectCountry: (country) => {
    const factors = []
    if (country.risk > 70) {
      factors.push({ name: 'Political Instability', value: country.risk - 10 })
      factors.push({ name: 'Rivalry Score', value: country.risk - 20 })
      factors.push({ name: 'Recent Hostile Events', value: country.risk - 30 })
    } else if (country.risk > 40) {
      factors.push({ name: 'Political Instability', value: 35 })
      factors.push({ name: 'Military Tension', value: 45 })
      factors.push({ name: 'Economic Stress', value: 25 })
    } else {
      factors.push({ name: 'Stability', value: 85 })
      factors.push({ name: 'Allies', value: 70 })
      factors.push({ name: 'Economy', value: 60 })
    }
    
    set({ 
      selectedCountry: country,
      riskData: {
        country: country.code,
        riskScore: country.risk,
        factors: factors
      }
    })
  },
  
  clearSelection: () => set({ selectedCountry: null, riskData: null }),
}))

export { useCountryStore }