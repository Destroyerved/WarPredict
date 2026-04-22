import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

COUNTRIES = {
    "USA": "United States", "CHN": "China", "RUS": "Russia", "IND": "India",
    "PAK": "Pakistan", "IRN": "Iran", "ISR": "Israel", "TUR": "Turkey",
    "DEU": "Germany", "GBR": "United Kingdom", "FRA": "France", "BRA": "Brazil",
    "JPN": "Japan", "KOR": "South Korea", "NGA": "Nigeria", "EGY": "Egypt",
    "SAU": "Saudi Arabia", "UKR": "Ukraine", "VEN": "Venezuela", "SYR": "Syria"
}


def calculate_risk(country_a: str, country_b: str, border: bool, alliance: bool, 
                   tensions: float, events: int) -> dict:
    base_risk = np.random.uniform(10, 40)
    
    if border:
        base_risk += 15
    if tensions > 0.6:
        base_risk += 20
    if events > 10:
        base_risk += 15
    if alliance:
        base_risk -= 10
    
    risk = min(100, max(0, base_risk))
    
    if risk >= 70:
        level = "Critical"
    elif risk >= 50:
        level = "High"
    elif risk >= 30:
        level = "Medium"
    else:
        level = "Low"
    
    return {"risk": risk, "level": level}


def show():
    st.title("🌍 Conflict Prediction Dashboard")
    st.markdown("Predict conflict probability between country pairs")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Country Selection")
        
        country_a = st.selectbox("Country A", list(COUNTRIES.keys()), 
                                  format_func=lambda x: f"{x} - {COUNTRIES[x]}")
        country_b = st.selectbox("Country B", list(COUNTRIES.keys()),
                                  format_func=lambda x: f"{x} - {COUNTRIES[x]}",
                                  index=1)
        
        st.markdown("### Risk Factors")
        
        border = st.checkbox("Contiguous Border", value=False)
        alliance = st.checkbox("Shared Alliance", value=False)
        tensions = st.slider("Diplomatic Tensions", 0.0, 1.0, 0.3)
        events = st.slider("Hostile Events (30d)", 0, 50, 5)
        
        years_ahead = st.selectbox("Prediction Timeframe", [1, 5, 10], 
                                    format_func=lambda x: f"{x} year(s)")
        
        if st.button("Calculate Risk", type="primary"):
            result = calculate_risk(country_a, country_b, border, alliance, tensions, events)
            st.session_state["prediction"] = result
    
    with col2:
        if "prediction" in st.session_state:
            result = st.session_state["prediction"]
            
            risk_color = {
                "Critical": "#ff3b3b", "High": "#f59e0b", 
                "Medium": "#fbbf24", "Low": "#10b981"
            }[result["level"]]
            
            st.markdown(f"""
            <div style="text-align: center; padding: 30px; background: #161b22; 
                        border-radius: 15px; margin-bottom: 20px;">
                <h2 style="margin: 0; color: {risk_color}; font-size: 48px;">
                    {result['risk']:.1f}%
                </h2>
                <h3 style="margin: 10px 0; color: #8b949e;">
                    {result['level'].upper()} RISK
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Risk Factor Breakdown")
            
            factors_data = pd.DataFrame({
                "Factor": ["Border Proximity", "Diplomatic Tensions", 
                          "Recent Hostile Events", "Alliance Status"],
                "Contribution": [15 if border else 0, int(tensions * 25),
                                min(25, events), -10 if alliance else 5]
            })
            
            fig = px.bar(factors_data, x="Factor", y="Contribution", 
                         orientation="v", color="Contribution",
                         color_continuous_scale=["#10b981", "#f59e0b", "#ff3b3b"])
            fig.update_layout(
                plot_bgcolor="#0d1117",
                paper_bgcolor="#0d1117",
                font_color="#e6edf3"
            )
            st.plotly_chart(fig, width='stretch')
        
        else:
            st.info("Select countries and risk factors, then click 'Calculate Risk'")
        
        st.subheader("Global Hot Zones")
        
        risk_scores = []
        for code in list(COUNTRIES.keys())[:10]:
            score = np.random.uniform(15, 75)
            risk_scores.append({"Country": COUNTRIES[code], "Risk Score": score})
        
        risk_df = pd.DataFrame(risk_scores).sort_values("Risk Score", ascending=False)
        
        fig2 = px.scatter(risk_df, x="Country", y="Risk Score", size="Risk Score",
                         color="Risk Score", color_continuous_scale=["#10b981", "#f59e0b", "#ff3b3b"])
        fig2.update_layout(
            plot_bgcolor="#0d1117",
            paper_bgcolor="#0d1117",
            font_color="#e6edf3"
        )
        st.plotly_chart(fig2, width='stretch')

if __name__ == "__main__":
    show()