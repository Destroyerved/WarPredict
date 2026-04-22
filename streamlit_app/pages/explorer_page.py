import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

CONFLICT_TYPES = ["Interstate War", "Civil War", "Proxy War", "Border Skirmish", "Insurgency"]
REGIONS = ["Europe", "Asia", "Middle East", "Africa", "Americas"]


def generate_conflict_data(n: int = 50) -> pd.DataFrame:
    np.random.seed(42)
    data = []
    
    for _ in range(n):
        year = np.random.randint(1945, 2024)
        conflict_type = np.random.choice(CONFLICT_TYPES)
        region = np.random.choice(REGIONS)
        
        if conflict_type == "Interstate War":
            intensity = np.random.choice(["Minor", "Medium", "Major"], p=[0.3, 0.4, 0.3])
        else:
            intensity = np.random.choice(["Low", "Medium", "High"], p=[0.4, 0.35, 0.25])
        
        if intensity == "Major" or intensity == "High":
            deaths = int(np.random.uniform(1000, 50000))
        elif intensity == "Medium":
            deaths = int(np.random.uniform(100, 1000))
        else:
            deaths = int(np.random.uniform(10, 100))
        
        data.append({
            "Year": year,
            "Type": conflict_type,
            "Region": region,
            "Intensity": intensity,
            "Deaths": deaths,
            "Duration (months)": int(np.random.uniform(1, 36))
        })
    
    return pd.DataFrame(data)


def show():
    st.title("📚 Historical Conflict Explorer")
    st.markdown("Browse and analyze historical conflict data")
    
    df = generate_conflict_data(100)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Filters")
        
        year_range = st.slider("Year Range", 1945, 2024, (1945, 2024))
        selected_types = st.multiselect("Conflict Type", CONFLICT_TYPES, default=CONFLICT_TYPES)
        selected_regions = st.multiselect("Region", REGIONS, default=REGIONS)
        
        filtered = df[
            (df["Year"] >= year_range[0]) & 
            (df["Year"] <= year_range[1]) &
            (df["Type"].isin(selected_types)) &
            (df["Region"].isin(selected_regions))
        ]
    
    with col2:
        st.subheader(f"Conflicts ({len(filtered)} found)")
        
        st.dataframe(
            filtered[["Year", "Type", "Region", "Intensity", "Deaths"]].sort_values("Year", ascending=False),
            width='stretch'
        )
    
    st.markdown("### Trend Analysis")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        yearly = filtered.groupby("Year").size().reset_index(name="Count")
        fig1 = px.line(yearly, x="Year", y="Count", title="Conflicts Over Time")
        fig1.update_layout(
            plot_bgcolor="#0d1117",
            paper_bgcolor="#0d1117",
            font_color="#e6edf3"
        )
        st.plotly_chart(fig1, width='stretch')
    
    with col_chart2:
        by_type = filtered.groupby("Type").agg({"Deaths": "sum"}).reset_index()
        fig2 = px.pie(by_type, values="Deaths", names="Type", 
                     title="Deaths by Conflict Type")
        fig2.update_layout(
            plot_bgcolor="#0d1117",
            paper_bgcolor="#0d1117",
            font_color="#e6edf3"
        )
        st.plotly_chart(fig2, width='stretch')
    
    col_map1, col_map2 = st.columns(2)
    
    with col_map1:
        by_region = filtered.groupby("Region").size().reset_index(name="Count")
        fig3 = px.bar(by_region, x="Region", y="Count", 
                     title="Conflicts by Region", color="Count",
                     color_continuous_scale="Reds")
        fig3.update_layout(
            plot_bgcolor="#0d1117",
            paper_bgcolor="#0d1117",
            font_color="#e6edf3"
        )
        st.plotly_chart(fig3, width='stretch')
    
    with col_map2:
        fig4 = px.scatter(filtered, x="Duration (months)", y="Deaths",
                         color="Type", size="Deaths", 
                         title="Duration vs Deaths",
                         log_y=True)
        fig4.update_layout(
            plot_bgcolor="#0d1117",
            paper_bgcolor="#0d1117",
            font_color="#e6edf3"
        )
        st.plotly_chart(fig4, width='stretch')

if __name__ == "__main__":
    show()