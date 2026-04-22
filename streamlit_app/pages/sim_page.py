import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

COUNTRIES = {
    "USA": "United States", "CHN": "China", "RUS": "Russia", "IND": "India",
    "PAK": "Pakistan", "IRN": "Iran", "ISR": "Israel", "TUR": "Turkey",
    "DEU": "Germany", "GBR": "United Kingdom", "FRA": "France", "BRA": "Brazil",
    "JPN": "Japan", "KOR": "South Korea", "NGA": "Nigeria", "EGY": "Egypt",
    "SAU": "Saudi Arabia", "UKR": "Ukraine", "VEN": "Venezuela", "SYR": "Syria"
}

ALLIANCES = ["NATO", "CIS", "CSTO", "EU"]


def run_simulation(country_a: str, country_b: str, mil_a: float, mil_b: float,
                  eco_a: float, eco_b: float, resolve_a: float, resolve_b: float,
                  alliances_a: list, alliances_b: list, nuclear: bool) -> dict:
    
    mil_diff = abs(mil_a - mil_b)
    eco_diff = abs(eco_a - eco_b)
    
    stronger = country_a if mil_a > mil_b else country_b
    weaker = country_b if mil_a > mil_b else country_a
    
    base_duration = 60 + (mil_diff * 2) + (eco_diff * 1.5)
    duration = int(base_duration * np.random.uniform(0.7, 1.3))
    
    base_casualties = (mil_a + mil_b) * 500
    casualties = int(base_casualties * np.random.uniform(0.5, 1.5))
    
    base_economic = (eco_a + eco_b) * 1e9 * (duration / 365)
    economic = int(base_economic * np.random.uniform(0.5, 1.5))
    
    winner_prob_a = 0.5 + (mil_a - mil_b) * 0.01 + (resolve_a - resolve_b) * 0.005
    
    if nuclear:
        if nuclear:
            winner = stronger
            winner_prob_a = 0.9 if country_a == stronger else 0.1
            duration = int(duration * 0.3)
            casualties = int(casualties * 2.5)
        else:
            winner = None
    
    else:
        winner = stronger if winner_prob_a > 0.55 else (weaker if winner_prob_a < 0.45 else None)
    
    cascade_triggered = len(alliances_a) > 0 or len(alliances_b) > 0
    cascade_nations = []
    if cascade_triggered:
        cascade_nations = list(set(alliances_a + alliances_b))
    
    return {
        "duration_days": duration,
        "casualties": casualties,
        "economic_damage": economic,
        "winner": winner,
        "prob_a_win": winner_prob_a,
        "cascade": cascade_nations,
        "nuclear": nuclear
    }


def show():
    st.title("⚔️ War Outcome Simulator")
    st.markdown("Simulate conflict scenarios with agent-based modeling")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Scenario Builder")
        
        country_a = st.selectbox("Country A", list(COUNTRIES.keys()),
                                  format_func=lambda x: COUNTRIES[x], index=0)
        country_b = st.selectbox("Country B", list(COUNTRIES.keys()),
                                  format_func=lambda x: COUNTRIES[x], index=2)
        
        st.markdown("### Military Parameters")
        
        col_mil1, col_mil2 = st.columns(2)
        with col_mil1:
            mil_a = st.slider("Country A Military Power", 0, 100, 50)
            eco_a = st.slider("Country A Economy", 0, 100, 50)
            res_a = st.slider("Country A Resolve", 0, 100, 50)
        with col_mil2:
            mil_b = st.slider("Country B Military Power", 0, 100, 50)
            eco_b = st.slider("Country B Economy", 0, 100, 50)
            res_b = st.slider("Country B Resolve", 0, 100, 50)
        
        st.markdown("### Alliances")
        
        alliances_a = st.multiselect(f"{COUNTRIES[country_a]} Alliances", 
                                      ALLIANCES, default=[])
        alliances_b = st.multiselect(f"{COUNTRIES[country_b]} Alliances", 
                                      ALLIANCES, default=[])
        
        nuclear = st.toggle("Nuclear Capabilities Enabled", value=False)
        
        if st.button("Run Simulation", type="primary"):
            result = run_simulation(country_a, country_b, mil_a, mil_b,
                                   eco_a, eco_b, res_a, res_b,
                                   alliances_a, alliances_b, nuclear)
            st.session_state["sim_result"] = result
    
    with col2:
        if "sim_result" in st.session_state:
            r = st.session_state["sim_result"]
            
            st.subheader("Simulation Results")
            
            res_col1, res_col2, res_col3 = st.columns(3)
            
            with res_col1:
                st.metric("Duration", f"{r['duration_days']} days")
            with res_col2:
                st.metric("Casualties", f"{r['casualties']:,}")
            with res_col3:
                st.metric("Economic Damage", f"${r['economic_damage']/1e9:.1f}B")
            
            if r["winner"]:
                st.success(f"Predicted Winner: **{COUNTRIES.get(r['winner'], r['winner'])}**")
            else:
                st.warning("Outcome: Stalemate / Mutual Exhaustion")
            
            if r["cascade"]:
                st.markdown("### ⚠️ Alliance Cascade")
                st.error(f"Conflict draws in: {', '.join(r['cascade'])}")
            
            if r["nuclear"]:
                st.markdown("### ☢️ Nuclear Impact")
                st.warning("Nuclear exchange dramatically increases casualties and shortens duration")
            
            st.subheader("Win Probability")
            
            prob_data = pd.DataFrame({
                "Country": [COUNTRIES[country_a], COUNTRIES[country_b]],
                "Probability": [r['prob_a_win'] * 100, (1 - r['prob_a_win']) * 100]
            })
            
            fig = go.Figure(data=[
                go.Bar(x=prob_data["Country"], y=prob_data["Probability"],
                      marker_color=["#3b82f6", "#ef4444"])
            ])
            fig.update_layout(
                title="Victory Probability",
                yaxis_title="Probability (%)",
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font_color="#e6edf3"
            )
            st.plotly_chart(fig, width='stretch')
        
        else:
            st.info("Configure scenario and click 'Run Simulation'")

if __name__ == "__main__":
    show()