import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Blue Energy PRO Dashboard")

st.title("🌊 Blue Energy Explorer: Power from River & Ocean Mixing")
st.write("When fresh river water meets salty ocean water, tremendous osmotic energy is released. This is **Pressure Retarded Osmosis (PRO)**. Adjust the parameters to maximize electricity generation!")
st.markdown("---")

# 2. Dual-column Layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("⚙️ System Controls")
    
    # Slider 1: Draw Solution Salinity
    salinity = st.slider(
        "Ocean Water Salinity (g/L)\n(Typical Ocean ≈ 35, Desalination Brine > 70)", 
        10, 100, 35
    )
    
    # Slider 2: Flow Rate Ratio (Draw / Feed)
    flow_ratio = st.slider(
        "Flow Rate Ratio (Ocean Flow / River Flow)\n(Higher ratio reduces internal dilution but increases pumping penalty)", 
        0.5, 5.0, 1.5
    )
    
    # Slider 3: Hydrostatic Pressure (Controlled by turbine)
    pressure = st.slider(
        "Applied Controlled Pressure ΔP (Bar)\n(The resistance load exerted by the power turbine)", 
        0, 50, 14
    )
    
    # --- PRO Physics Engine ---
    A_membrane = 2.0  # Water permeability, L/(m²·h·bar)
    pi_ocean = salinity * 0.76
    pi_river = 0.5 * 0.76  # River water background
    
    # Dilution effect model proxy
    dilution_factor = flow_ratio / (flow_ratio + 0.25)
    delta_pi_eff = (pi_ocean - pi_river) * dilution_factor
    
    # Operating Regime Logic
    if pressure < delta_pi_eff:
        jw = A_membrane * (delta_pi_eff - pressure)
        power_density = jw * pressure * (100 / 3600)  # Convert to W/m²
        status_text = "🚀 Power Generation Active: River water permeates into ocean side, spinning the turbine!"
        status_type = "success"
    else:
        jw = 0
        power_density = 0
        status_text = "⚠️ Reverse Osmosis Regime: Pressure is too high! You are consuming energy instead of generating power."
        status_type = "warning"
        
    st.markdown("---")
    st.subheader("💡 Live Performance Metrics")
    
    if status_type == "success":
        st.success(status_text)
    else:
        st.warning(status_text)
        
    st.metric(label="⚡ Power Density Generated (Target: > 5 W/m²)", value=f"{power_density:.2f} W/m²")
    st.metric(label="💧 Trans-membrane Water Flux (Jw)", value=f"{jw:.1f} L/(m²·h)")
    st.metric(label="🧬 Effective Osmotic Driving Force (Δπ)", value=f"{delta_pi_eff:.1f} Bar")

with col2:
    # --- Component 1: Process Flow Diagram (PFD) ---
    st.subheader("🔍 Process Flow Diagram (工艺流程图)")
    
    pfd_html = f"""
    <div style="font-family: sans-serif; background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; text-align: center; font-weight: bold; font-size: 12px;">
            <div style="flex: 1; background-color: #e3f2fd; padding: 10px; border-radius: 4px; border: 1px solid #90caf9;">
                💧 River Water (Feed)<br><span style="font-weight:normal; color:#555;">Low Salinity</span>
            </div>
            <div style="padding: 0 10px; color: #1e88e5;">➔</div>
            
            <div style="flex: 1.5; background-color: #fff; padding: 15px; border-radius: 6px; border: 2px dashed #00b0ff; position: relative;">
                <div style="background-color: #e1f5fe; padding: 4px; margin-bottom: 6px; border-radius: 2px;">Feed Side (Jw ➔)</div>
                <div style="border-top: 2px solid #ccc; margin: 8px 0;">PRO Membrane 🧬</div>
                <div style="background-color: #ede7f6; padding: 4px; margin-top: 6px; border-radius: 2px;">Draw Side (ΔP = {pressure} Bar)</div>
            </div>
            
            <div style="padding: 0 10px; color: #7e57c2;">➔</div>
            <div style="flex: 1.2; background-color: #fff3e0; padding: 10px; border-radius: 4px; border: 1px solid #ffcc80;">
                ⚡ Hydro-Turbine<br>
                <span style="color: #e65100; font-size: 14px;">{power_density:.2f} W/m²</span>
            </div>
        </div>
        <div style="margin-top: 12px; display: flex; align-items: center; font-size: 12px; font-weight: bold;">
            <div style="background-color: #ede7f6; padding: 8px; border-radius: 4px; border: 1px solid #b39ddb; text-align: center;">
                🌊 Ocean Water (Draw)<br><span style="font-weight:normal; color:#555;">{salinity} g/L</span>
            </div>
            <div style="padding: 0 10px; color: #7e57c2;">➔</div>
            <div style="background-color: #f5f5f5; padding: 6px; border-radius: 4px; border: 1px solid #ccc;">
                泵 HP Pump
            </div>
            <div style="padding: 0 10px; color: #7e57c2;">➔ (Flow Ratio: {flow_ratio:.1f}) ➔ Draw Side Entry</div>
        </div>
    </div>
    """
    st.components.v1.html(pfd_html, height=180)
    
    # --- Component 2: Interactive Altair Chart ---
    st.subheader("📊 Power Optimization Curve")
    st.write("Hover over the green line to see precise calculations. The **Red Dot** tracking represents your current setup.")
    
    # Generate Parabolic Curve Data
    p_space = np.linspace(0, 50, 150)
    w_space = []
    for p in p_space:
        if p < delta_pi_eff:
            j = A_membrane * (delta_pi_eff - p)
            w = j * p * (100 / 3600)
        else:
            w = 0.0
        w_space.append(w)
        
    df_curve = pd.DataFrame({
        'Applied Pressure (Bar)': p_space,
        'Power Density (W/m²)': w_space
    })
    
    df_point = pd.DataFrame({
        'Applied Pressure (Bar)': [pressure],
        'Power Density (W/m²)': [power_density]
    })
    
    # Base Curve Chart
    curve_chart = alt.Chart(df_curve).mark_line(color='#2ca02c', size=3).encode(
        x=alt.X('Applied Pressure (Bar):Q', scale=alt.Scale(domain=[0, 50])),
        y=alt.Y('Power Density (W/m²):Q', title='Power Density Jw·ΔP (W/m²)', scale=alt.Scale(domain=[0, max(w_space)*1.2 if max(w_space)>0 else 5])),
        tooltip=['Applied Pressure (Bar)', 'Power Density (W/m²)']
    )
    
    # Dynamic Operating Point (Red Dot)
    point_chart = alt.Chart(df_point).mark_circle(color='red', size=180).encode(
        x='Applied Pressure (Bar):Q',
        y='Power Density (W/m²):Q',
        tooltip=['Applied Pressure (Bar)', 'Power Density (W/m²)']
    )
    
    # Layer and render the charts
    final_chart = alt.layer(curve_chart, point_chart).interactive()
    st.altair_chart(final_chart, use_container_width=True)