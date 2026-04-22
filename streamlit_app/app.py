import streamlit as st
from pages import pred_page, sim_page, explorer_page, insights_page

st.set_page_config(
    page_title="War Prediction & Conflict Simulator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #080c10;
    }
    .css-1d391kg {
        background-color: #0d1117;
    }
    h1, h2, h3 {
        color: #e6edf3 !important;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
    }
    .risk-critical { color: #ff3b3b; }
    .risk-high { color: #f59e0b; }
    .risk-medium { color: #fbbf24; }
    .risk-low { color: #10b981; }
</style>
""", unsafe_allow_html=True)

PAGES = {
    "Prediction Dashboard": pred_page,
    "War Simulator": sim_page,
    "Conflict Explorer": explorer_page,
    "Model Insights": insights_page
}

def main():
    with st.sidebar:
        st.title("🌍 War Predictor")
        st.markdown("---")
        
        selection = st.radio("Navigation", list(PAGES.keys()))
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        This system uses ML models to predict 
        conflict probability and simulate war 
        scenarios.
        
        **Disclaimer**: For academic research only.
        """)
    
    page_module = PAGES[selection]
    page_module.show()

if __name__ == "__main__":
    main()