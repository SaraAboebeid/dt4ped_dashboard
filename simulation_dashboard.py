import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ast
from collections import Counter

st.set_page_config(
    page_title="DT4PED Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Sidebar navigation + sticky footer
st.sidebar.markdown("# 📊 DT4PED")
st.sidebar.markdown("## 📂 Navigation")

# Navigation links
st.sidebar.markdown(
    """
<div class="sidebar-links">
    <a href="#dt4ped-retrofit-simulation-dashboard">🏠 Home</a>
    <a href="#key-performance-indicators">📊 Key Insights</a>
    <a href="#2d-pareto-plots">🌟 2D Pareto Plots</a>
    <a href="#heating-demand-distribution">📉 Histograms</a>
    <a href="#parallel-coordinates-plot">🧵 Parallel Coordinates</a>
    <a href="#top-10-packages">🏆 Top 10 Packages</a>
    <a href="#most-common-materials">🏗️ Material Usage</a>
    <a href="#multi-criteria-selector-for-top-packages">🎛️ Multi-Criteria Selector</a>
</div>
""",
    unsafe_allow_html=True
)

# Inject sticky footer using absolute positioning
st.sidebar.markdown(
    """
<style>
/* Sidebar links style */
.sidebar-links a {
    text-decoration: none;
    color: #4B8BBE;
    font-weight: 500;
    padding: 6px 0;
    display: block;
    transition: all 0.2s ease-in-out;
}
.sidebar-links a:hover {
    color: #306998;
    transform: translateX(5px);
}

/* Footer sticky at the bottom of sidebar */
#custom-footer {
    position: fixed;
    bottom: 30px;
    left: 16px;
    width: 260px;
    font-size: 0.85rem;
    color: #888;
    border-top: 1px solid #DDD;
    padding-top: 10px;
}
</style>

<div id="custom-footer">
    <strong>📘 Project:</strong> DT4PED Retrofit Study<br>
    <strong>📍 Location:</strong> Jättestensgatan 7<br>
    <strong>👥 Contributors:</strong><br>
    David Sindelar (Materials)<br>
    Sara Abouebeid (Simulation & Dashboard)<br>
    <br>
    <em>© 2025</em>
</div>
""",
    unsafe_allow_html=True
)


# ----------------- Title and Intro -----------------
st.markdown("<a id='home'></a>", unsafe_allow_html=True)
st.title("DT4PED Retrofit Simulation Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    _Building: Jättestensgatan 7, Gothenburg_

    This tool visualizes the results of a large-scale EnergyPlus simulation exploring **retrofitting strategies** based on different material combinations.

    The goal is to identify the most effective solutions for:
    - 🌍 **Global Warming Potential (GWP)**
    - 💰 **Material Cost (SEK)**
    - 🔋 **Heating Demand (kWh/m²)**
    """)

with col2:
    st.markdown("""
    #### 🔍 What You Can Do Here
    - 📈 Explore trade-offs between sustainability, cost, and energy performance  
    - 🏆 Select top-performing retrofit packages based on your preferences  
    - 🧱 Understand which materials appear most frequently in optimal packages

    **Contributors**  
    **Material DB compiled by:** David Sindelar   
    **Energy modelling and dashboard:** Sara Abouebeid 
    """)

st.divider()

@st.cache_data
def load_data():
    df = pd.read_csv("summary.csv")
    df["wall_materials"] = df["wall_materials"].apply(ast.literal_eval)
    df["roof_materials"] = df["roof_materials"].apply(ast.literal_eval)
    df["wall_materials_str"] = df["wall_materials"].apply(lambda x: ", ".join(x))
    df["roof_materials_str"] = df["roof_materials"].apply(lambda x: ", ".join(x))
    return df

df = load_data()

# Get best-performing packages
best_heat_pkg = df.sort_values("heating_demand_kwh_per_m2").iloc[0]
best_gwp_pkg = df.sort_values("gwp_kgco2e").iloc[0]
best_cost_pkg = df.sort_values("cost_sek").iloc[0]

# Medians
median_heat = df["heating_demand_kwh_per_m2"].median()
median_gwp = df["gwp_kgco2e"].median()
median_cost = df["cost_sek"].median()

# Show KPI Metrics
st.markdown("### 📊 Key Performance Indicators")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("🔋 Lowest Heating Demand", f"{best_heat_pkg['heating_demand_kwh_per_m2']:.2f} kWh/m²", delta=f"vs median {median_heat:.1f}")
    st.markdown(f"**Package:** `{best_heat_pkg['package']}`")
    st.markdown("**Wall:** " + ", ".join(best_heat_pkg["wall_materials"]))
    st.markdown("**Roof:** " + ", ".join(best_heat_pkg["roof_materials"]))

with kpi2:
    st.metric("🌍 Lowest GWP", f"{best_gwp_pkg['gwp_kgco2e']:,.0f} kgCO₂e", delta=f"vs median {median_gwp:,.0f}")
    st.markdown(f"**Package:** `{best_gwp_pkg['package']}`")
    st.markdown("**Wall:** " + ", ".join(best_gwp_pkg["wall_materials"]))
    st.markdown("**Roof:** " + ", ".join(best_gwp_pkg["roof_materials"]))

with kpi3:
    st.metric("💰 Lowest Cost", f"{best_cost_pkg['cost_sek']:,.0f} SEK", delta=f"vs median {median_cost:,.0f}")
    st.markdown(f"**Package:** `{best_cost_pkg['package']}`")
    st.markdown("**Wall:** " + ", ".join(best_cost_pkg["wall_materials"]))
    st.markdown("**Roof:** " + ", ".join(best_cost_pkg["roof_materials"]))

# ----------------- Insights -----------------
st.markdown("<a id='key-insights'></a>", unsafe_allow_html=True)
# Extract insulation materials (3rd item in each list)
wall_insulations = df["wall_materials"].apply(lambda x: x[2] if len(x) > 2 else "None")
most_common_insulation = wall_insulations.value_counts().idxmax()
most_common_insulation_count = wall_insulations.value_counts().max()

st.markdown("### 💡 Key Insights")
st.success(f"""
- 🔋 **Lowest Heating Demand**: `{best_heat_pkg['package']}` with **{best_heat_pkg['heating_demand_kwh_per_m2']:.2f} kWh/m²**
- 🌍 **Lowest GWP**: `{best_gwp_pkg['package']}` with **{best_gwp_pkg['gwp_kgco2e']:,.0f} kgCO₂e**
- 💰 **Cost Range**: from **{df['cost_sek'].min():,.0f} SEK** to **{df['cost_sek'].max():,.0f} SEK**, showing wide variation across packages
""")

st.divider()

# ---------------- SCATTER PLOTS ----------------
st.markdown("<a id='2d-pareto-plots'></a>", unsafe_allow_html=True)
st.subheader("🌟 2D Pareto Plots")
pareto1, pareto2 = st.columns(2)

with pareto1:
    fig1 = px.scatter(
        df, x="cost_sek", y="gwp_kgco2e", color="heating_demand_kwh_per_m2",
        hover_name="package", hover_data=["wall_materials_str", "roof_materials_str"],
        labels={
            "cost_sek": "Cost (SEK)",
            "gwp_kgco2e": "GWP (kgCO₂e)",
            "heating_demand_kwh_per_m2": "Heating (kWh/m²)"
        },
        title="💰 Cost vs 🌍 GWP", color_continuous_scale="Viridis"
    )
    fig1.update_layout(
        height=600,  # 👈 Make height fixed
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig1, use_container_width=True)  # 👈 Let width fill column

with pareto2:
    fig2 = px.scatter(
        df, x="heating_demand_kwh_per_m2", y="gwp_kgco2e", color="cost_sek",
        hover_name="package", hover_data=["wall_materials_str", "roof_materials_str"],
        labels={
            "heating_demand_kwh_per_m2": "Heating (kWh/m²)",
            "gwp_kgco2e": "GWP (kgCO₂e)",
            "cost_sek": "Cost (SEK)"
        },
        title="🔋 Heating vs 🌍 GWP", color_continuous_scale="Magma"
    )
    fig2.update_layout(
        height=600,  # 👈 Same here
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig2, use_container_width=True)

# ----------------  Histograms ----------------
st.markdown("<a id='histograms'></a>", unsafe_allow_html=True)
dist_col1, dist_col2, dist_col3 = st.columns(3)
with dist_col1:
    st.plotly_chart(px.histogram(df, x="heating_demand_kwh_per_m2", nbins=30, title="Heating Demand Distribution"), use_container_width=True)
with dist_col2:
    st.plotly_chart(px.histogram(df, x="gwp_kgco2e", nbins=30, title="GWP Distribution"), use_container_width=True)
with dist_col3:
    st.plotly_chart(px.histogram(df, x="cost_sek", nbins=30, title="Cost Distribution"), use_container_width=True)

# ----------------- Plots ------------------

# ---------------- PARALLEL COORDINATES ----------------
st.markdown("<a id='parallel-coordinates-plot'></a>", unsafe_allow_html=True)
st.subheader("🧵 Parallel Coordinates Plot")
for i, label in enumerate(["cladding", "membrane", "insulation"]):
    df[f"wall_{label}"] = df["wall_materials"].apply(lambda x: x[i] if len(x) > i else "None")
    df[f"roof_{label}"] = df["roof_materials"].apply(lambda x: x[i] if len(x) > i else "None")

material_cols = [f"{typ}_{layer}" for typ in ["roof", "wall"] for layer in ["cladding", "membrane", "insulation"]]
tick_dict = {}
for col in material_cols:
    unique = df[col].unique()
    tick_dict[col] = pd.Series(range(len(unique)), index=unique)
    df[col + "_dummy"] = df[col].map(tick_dict[col])

dimensions = []
for col in material_cols:
    dummy = col + "_dummy"
    dimensions.append(dict(
        range=[0, df[dummy].max()],
        tickvals=list(tick_dict[col].values),
        ticktext=list(tick_dict[col].index),
        label=col.replace("_", " ").title(),
        values=df[dummy]
    ))
for kpi in ["heating_demand_kwh_per_m2", "gwp_kgco2e", "cost_sek"]:
    dimensions.append(dict(label=kpi.replace("_", " ").title(), values=df[kpi]))

fig = go.Figure(data=go.Parcoords(
    line=dict(color=df["gwp_kgco2e"], colorscale='Magma', showscale=True),
    dimensions=dimensions,
    unselected=dict(line=dict(color='grey', opacity=0.1))  # Add this line
))
fig.update_layout(height=500,
                   margin=dict(l=90, r=20, t=40, b=20),
                   font=dict(family="Arial", size=14, color="#222")  # Clean font, no stroke
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- TOP 10 TABLES ----------------
st.markdown("<a id='top-10-packages'></a>", unsafe_allow_html=True)
st.subheader("🏆 Top 10 Packages")
tabs = st.tabs(["Lowest GWP", "Lowest Cost", "Lowest Heating"])
with tabs[0]: st.dataframe(df.sort_values("gwp_kgco2e").head(10), use_container_width=True)
with tabs[1]: st.dataframe(df.sort_values("cost_sek").head(10), use_container_width=True)
with tabs[2]: st.dataframe(df.sort_values("heating_demand_kwh_per_m2").head(10), use_container_width=True)



# ---------------- MULTI-CRITERIA FILTER ----------------
st.markdown("<a id='multi-criteria-selector'></a>", unsafe_allow_html=True)
st.subheader("🔧 Multi-Criteria Selector for Top Packages")

st.markdown("Choose how much each factor matters to you. We will normalize the weights.")
gw_raw = st.slider("🌍 GWP importance", 0.0, 1.0, 0.4, 0.01)
cw_raw = st.slider("💰 Cost importance", 0.0, 1.0, 0.3, 0.01)
hw_raw = st.slider("🔋 Heating importance", 0.0, 1.0, 0.3, 0.01)

total_weight = gw_raw + cw_raw + hw_raw
if total_weight == 0:
    st.warning("Please assign some weight to at least one criterion.")
else:
    gw = gw_raw / total_weight
    cw = cw_raw / total_weight
    hw = hw_raw / total_weight

    st.markdown(f"""
    **Normalized Weights**  
    🌍 GWP: `{gw:.2f}`  
    💰 Cost: `{cw:.2f}`  
    🔋 Heating: `{hw:.2f}`
    """)

    df["score"] = (
        df["gwp_kgco2e"].rank() * gw +
        df["cost_sek"].rank() * cw +
        df["heating_demand_kwh_per_m2"].rank() * hw
    )

    top_custom = df.sort_values("score").head(6)
    st.dataframe(top_custom, use_container_width=True)

st.markdown("---")
st.caption("Made with Streamlit + Plotly for EnergyPlus Package Evaluation")
