/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'war-bg': '#080c10',
        'war-surface': '#0d1117',
        'war-elevated': '#161b22',
        'war-border': '#21262d',
        'war-red': '#ff3b3b',
        'war-amber': '#f59e0b',
        'war-green': '#10b981',
        'war-blue': '#3b82f6',
        'war-cyan': '#06b6d4',
        'war-text': '#e6edf3',
        'war-muted': '#8b949e',
      },
      fontFamily: {
        'display': ['Orbitron', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
        'body': ['Space Grotesk', 'sans-serif'],
      },
    },
  },
  plugins: [],
}