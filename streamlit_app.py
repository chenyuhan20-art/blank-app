import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Blue Energy Game!")

# --- CSS INJECTION FOR COMPACT, GAMIFIED UI & EPIC EFFECTS ---
st.markdown("""
<style>
    /* Pull everything up to the absolute top of the screen */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important; 
    }

    /* Playful dotted 'water bubble' background */
    .stApp {
        background-color: #f0f9ff;
        background-image: radial-gradient(#bae6fd 2px, transparent 2px);
        background-size: 30px 30px;
    }
    
    /* Big, bouncy headers with absolutely minimal margins */
    h1 { font-size: 3.2rem !important; color: #0369a1 !important; font-weight: 900 !important; text-shadow: 2px 2px #bae6fd; padding-bottom: 0rem !important; margin-bottom: 0rem !important; }
    h3 { font-size: 2.0rem !important; color: #0284c7 !important; margin-top: 0rem !important; padding-top: 0rem !important; font-weight: 800 !important; }
    
    /* Squish horizontal dividers to save space */
    hr { margin: 0.5em 0 !important; }

    /* ENLARGED: Chunky, colorful slider text */
    .stSlider label p { font-size: 1.6rem !important; font-weight: 900 !important; color: #0f172a !important; line-height: 1.2 !important; }
    
    /* ENLARGED: Slider thumb values and min/max limits */
    .stSlider div[data-testid="stThumbValue"] { font-size: 1.4rem !important; font-weight: 900 !important; color: #ea580c !important; }
    .stSlider div[data-testid="stTickBarMin"], .stSlider div[data-testid="stTickBarMax"] { font-size: 1.2rem !important; font-weight: bold !important; }
    
    /* Fun Alert boxes */
    .stAlert { padding: 0.8rem !important; }
    .stAlert p { font-size: 1.5rem !important; font-weight: 900 !important; line-height: 1.2 !important; margin: 0 !important; }
    
    /* System Overload Danger Alert */
    .danger-alert {
        background-color: #fee2e2;
        border: 5px solid #ef4444;
        border-radius: 15px;
        padding: 15px;
        color: #991b1b;
        font-size: 1.6rem;
        font-weight: 900;
        text-align: center;
        line-height: 1.3;
        animation: pulse-danger 1s infinite;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    @keyframes pulse-danger {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        50% { transform: scale(1.02); box-shadow: 0 0 25px 10px rgba(239, 68, 68, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    /* === NEW: CRITICALLY EPIC RAINBOW NEON VICTORY BANNER === */
    .victory-banner {
        background: linear-gradient(45deg, #ff007f, #ffaa00, #00ff66, #00ffff, #7f00ff, #ff007f);
        background-size: 400% 400%;
        animation: neon-flow 3s linear infinite, epic-bounce 0.6s infinite alternate;
        border: 6px solid #ffffff;
        border-radius: 25px;
        padding: 20px;
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 950;
        text-shadow: 3px 3px 0px #000, -1px -1px 0px #000, 1px -1px 0px #000, -1px 1px 0px #000;
        text-align: center;
        line-height: 1.4;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3), inset 0 0 20px rgba(255,255,255,0.6);
    }
    @keyframes neon-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes epic-bounce {
        0% { transform: translateY(0) scale(1); }
        100% { transform: translateY(-8px) scale(1.02); }
    }
</style>
""", unsafe_allow_html=True)

st.title("🌊 Blue Energy Game: Power from Water!")
st.write("### 🎮 **Your Mission:** Mix fresh river water with salty ocean water to spin the turbine and generate electricity! Can you find the perfect setup to get the **High Score**?")
st.markdown("---")

# ==========================================
# ROW 1: CONTROLS (LEFT) & SVG DIAGRAM (RIGHT)
# ==========================================
col1, col2 = st.columns([1, 1.4])

with col1:
    st.markdown("### 🎛️ Game Controls")
    
    salinity = st.slider(
        "🌊 Ocean Saltiness (g/L) \n(Make it super salty!)", 
        10, 100, 35
    )
    
    flow_ratio = st.slider(
        "🚰 Water Mix Ratio (Ocean / River) \n(How fast is the water rushing in?)", 
        0.5, 5.0, 1.5
    )
    
    pressure = st.slider(
        "⚙️ Turbine Resistance ΔP (Bar) \n(How hard is it to push the generator?)", 
        0, 50, 14
    )
    
    # --- PRO Physics Engine ---
    A_membrane = 2.0
    pi_ocean = salinity * 0.76
    pi_river = 0.5 * 0.76 
    
    dilution_factor = flow_ratio / (flow_ratio + 0.25)
    delta_pi_eff = (pi_ocean - pi_river) * dilution_factor
    
    # Calculate the absolute theoretical maximum power point
    p_opt = delta_pi_eff / 2
    w_opt = A_membrane * (delta_pi_eff - p_opt) * p_opt * (100 / 3600)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # GAME STATE LOGIC
    is_overload = pressure >= delta_pi_eff
    
    if not is_overload:
        jw = A_membrane * (delta_pi_eff - pressure)
        power_density = jw * pressure * (100 / 3600)
        
        # --- THE GAMIFICATION REWARD SYSTEM (TIGHTENED TO 99% FOR MAXIMUM CHALLENGE) ---
        if power_density > 0 and w_opt > 0 and power_density >= (w_opt * 0.99):
            st.markdown("""
                <div class="victory-banner">
                    👑 ULTIMATE OSMASTER ACHIEVED! 👑<br>
                    🎉 PERFECT THERMODYNAMIC PEAK LOCKED! UNBELIEVABLE! 🎉
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            status_text = "👍 Good job! The turbine is spinning! But can you tweak the sliders to get MORE power?"
            st.info(status_text)
    else:
        jw = 0
        power_density = 0
        st.markdown("""
            <div class="danger-alert">
                🚨 DANGER! SYSTEM OVERLOAD! 🚨<br>
                The turbine resistance is too high! The water cannot push through the filter anymore. The turbine has STOPPED! Lower the pressure immediately!
            </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🔍 What's happening inside the machine?")
    
    lightning_scale = 1.0 + min(1.0, power_density / 5.0)
    lightning_opacity = "0" if is_overload else "1"
    
    flow_anim_seawater = "none" if is_overload else "flow 1.2s linear infinite"
    flow_anim_river = "none" if is_overload else "flow 1s linear infinite"
    flow_anim_hp = "none" if is_overload else "flow 1s linear infinite"
    flow_anim_lp = "none" if is_overload else "flow 1.5s linear infinite"
    flow_anim_brine = "none" if is_overload else "flow 1.8s linear infinite"
    flow_anim_jw = "none" if is_overload else "flow-up 0.6s linear infinite"
    
    turbine_anim = "none" if is_overload else f"spin {max(0.2, 2.0 - power_density/5.0)}s linear infinite"
    
    jw_text = "BLOCKED!" if is_overload else f"Jw = {jw:.1f}"
    jw_color = "#ef4444" if is_overload else "#0ea5e9"
    membrane_opacity = "0" if is_overload else "1"
    
    overload_overlay = ""
    if is_overload:
        overload_overlay = """
        <rect x="-120" y="-10" width="1170" height="310" fill="#ef4444" opacity="0.15" />
        <text x="465" y="140" font-family="'Comic Sans MS', 'Chalkboard SE', sans-serif" font-size="45" font-weight="900" fill="#dc2626" text-anchor="middle" style="animation: pulse 0.8s infinite;">🚨 WARNING: OVERLOAD 🚨</text>
        <text x="465" y="180" font-family="'Comic Sans MS', 'Chalkboard SE', sans-serif" font-size="22" font-weight="900" fill="#991b1b" text-anchor="middle">WATER BLOCKED! TURBINE STOPPED!</text>
        """
    
    pfd_html = f"""
    <div style="width: 100%; margin: 0 auto; text-align: center;">
        <svg viewBox="-120 -10 1050 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background-color: #ffffff; border-radius: 20px; border: 4px solid #bae6fd; box-shadow: 0 10px 20px rgba(0,0,0,0.05);">
            
            <defs>
                <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
                    <feDropShadow dx="3" dy="5" stdDeviation="4" flood-opacity="0.2" />
                </filter>
            </defs>

            <style>
                .pipe {{ stroke: #cbd5e1; stroke-width: 8; fill: none; stroke-linecap: round; stroke-linejoin: round; }}
                
                .seawater {{ stroke: #2563eb; stroke-width: 4; fill: none; stroke-dasharray: 8, 8; animation: {flow_anim_seawater}; }}
                .river {{ stroke: #38bdf8; stroke-width: 4; fill: none; stroke-dasharray: 8, 8; animation: {flow_anim_river}; }}
                .hp-diluted {{ stroke: #1d4ed8; stroke-width: 4; fill: none; stroke-dasharray: 8, 8; animation: {flow_anim_hp}; }}
                .lp-diluted {{ stroke: #7dd3fc; stroke-width: 4; fill: none; stroke-dasharray: 8, 8; animation: {flow_anim_lp}; }}
                .brine {{ stroke: #1e3a8a; stroke-width: 4; fill: none; stroke-dasharray: 8, 8; animation: {flow_anim_brine}; }}
                
                .jw-stream {{ stroke: {jw_color}; stroke-width: 3; fill: none; stroke-dasharray: 5, 5; animation: {flow_anim_jw}; opacity: {membrane_opacity}; }}
                
                @keyframes flow {{ to {{ stroke-dashoffset: -24; }} }}
                @keyframes flow-up {{ to {{ stroke-dashoffset: -15; }} }}
                @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
                @keyframes pulse {{ 0% {{ opacity: 0.4; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.4; }} }}
                
                .turbine-blades {{ transform-origin: 600px 120px; animation: {turbine_anim}; }}
                .lightning {{ animation: pulse 0.8s ease-in-out infinite; fill: #fbbf24; opacity: {lightning_opacity}; }}
                
                .label {{ font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif; font-size: 16px; fill: #0f172a; font-weight: 800; }}
                .sub-label {{ font-family: 'Comic Sans MS', sans-serif; font-size: 13px; fill: #64748b; font-weight: bold; }}
                .dyn-val {{ font-family: 'Comic Sans MS', sans-serif; font-size: 16px; fill: #ea580c; font-weight: 900; }}
            </style>
            
            <path d="M 20 120 L 90 120" class="pipe"/>
            <path d="M 135 120 L 240 120" class="pipe"/>
            <path d="M 740 185 L 440 185" class="pipe"/>
            <path d="M 240 185 L 20 185" class="pipe"/>
            <path d="M 440 120 L 530 120" class="pipe"/>
            <path d="M 530 120 L 578 120" class="pipe"/>
            <path d="M 530 120 L 530 60 L 135 60" class="pipe"/>
            <path d="M 90 60 L 20 60" class="pipe"/>
            <path d="M 620 120 L 740 120" class="pipe"/>
            <path d="M 600 100 Q 600 45 680 45" style="stroke: #fef08a; stroke-width: 6; fill: none; opacity: {lightning_opacity};"/>
            
            <path d="M 20 120 L 90 120" class="seawater"/>
            <path d="M 135 120 L 240 120" class="seawater"/>
            <path d="M 740 185 L 440 185" class="river"/>
            <path d="M 240 185 L 20 185" class="brine"/>
            <path d="M 440 120 L 530 120" class="hp-diluted"/>
            <path d="M 530 120 L 578 120" class="hp-diluted"/>
            <path d="M 530 120 L 530 60 L 135 60" class="hp-diluted"/>
            <path d="M 90 60 L 20 60" class="lp-diluted"/>
            <path d="M 620 120 L 740 120" class="lp-diluted"/>
            <path d="M 600 100 Q 600 45 680 45" style="stroke: #f59e0b; stroke-width: 6; fill: none; stroke-dasharray: 10,6; animation: {flow_anim_hp}; opacity: {lightning_opacity};"/>
            
            <polygon points="70,111 86,120 70,129" fill="#2563eb"/>
            <polygon points="215,111 231,120 215,129" fill="#2563eb"/>
            <polygon points="486,176 470,185 486,194" fill="#38bdf8"/>
            <polygon points="56,176 40,185 56,194" fill="#1e3a8a"/>
            <polygon points="485,111 501,120 485,129" fill="#1d4ed8"/>
            <polygon points="555,111 571,120 555,129" fill="#1d4ed8"/>
            <polygon points="176,51 160,60 176,69" fill="#1d4ed8"/>
            <polygon points="56,51 40,60 56,69" fill="#7dd3fc"/>
            <polygon points="720,111 736,120 720,129" fill="#7dd3fc"/>
            <polygon points="670,36 686,45 670,54" fill="#f59e0b" opacity="{lightning_opacity}"/>
            
            <rect x="90" y="45" width="45" height="105" rx="12" fill="#e0f2fe" stroke="#0369a1" stroke-width="3" filter="url(#shadow)"/>
            <text x="112" y="102" class="label" font-size="14" text-anchor="middle" fill="#0369a1">PX</text>
            
            <rect x="240" y="90" width="200" height="135" rx="15" fill="#f8fafc" stroke="#334155" stroke-width="4" filter="url(#shadow)"/>
            <line x1="242" y1="156" x2="438" y2="156" stroke="#cbd5e1" stroke-width="12" stroke-dasharray="6,6"/>
            <line x1="240" y1="152" x2="440" y2="152" stroke="#8b5cf6" stroke-width="4"/>
            
            <path d="M 270 182 L 270 135 M 310 182 L 310 135 M 350 182 L 350 135 M 390 182 L 390 135" class="jw-stream"/>
            <g opacity="{membrane_opacity}">
                <polygon points="266,142 270,132 274,142" fill="{jw_color}"/>
                <polygon points="306,142 310,132 314,142" fill="{jw_color}"/>
                <polygon points="346,142 350,132 354,142" fill="{jw_color}"/>
                <polygon points="386,142 390,132 394,142" fill="{jw_color}"/>
            </g>
            <text x="340" y="146" class="dyn-val" text-anchor="middle" fill="{jw_color}" style="animation: {'pulse 1s infinite' if is_overload else 'none'}">{jw_text}</text>
            
            <circle cx="600" cy="120" r="28" fill="#ffedd5" stroke="#ea580c" stroke-width="4" filter="url(#shadow)"/>
            <g class="turbine-blades">
                <line x1="576" y1="120" x2="624" y2="120" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
                <line x1="600" y1="96" x2="600" y2="144" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
                <line x1="583" y1="103" x2="617" y2="137" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
                <line x1="583" y1="137" x2="617" y2="103" stroke="#ea580c" stroke-width="4" stroke-linecap="round"/>
            </g>
            
            <polygon points="705,60 720,45 712,45 722,25 702,40 710,40" class="lightning" style="transform: scale({lightning_scale}); transform-origin: 710px 45px;"/>
            
            <text x="5" y="115" class="label" text-anchor="end">Salty Ocean</text>
            <text x="5" y="130" class="sub-label" text-anchor="end">({salinity} g/L)</text>
            
            <text x="5" y="180" class="label" text-anchor="end">Waste Water</text>
            <text x="5" y="195" class="sub-label" text-anchor="end">Too salty!</text>
            
            <text x="5" y="55" class="label" text-anchor="end">Diluted Water</text>
            <text x="5" y="70" class="sub-label" text-anchor="end">Low Pressure</text>
            
            <text x="755" y="180" class="label" text-anchor="start">Fresh River</text>
            <text x="755" y="195" class="sub-label" text-anchor="start">Clean Water</text>
            
            <text x="755" y="115" class="label" text-anchor="start">Mixed Water</text>
            <text x="755" y="130" class="sub-label" text-anchor="start">Discharge</text>
            
            <text x="340" y="105" class="label" text-anchor="middle" fill="#0369a1">Salty Side</text>
            <text x="340" y="215" class="label" text-anchor="middle" fill="#0284c7">Fresh Side</text>
            
            <text x="112" y="170" class="label" text-anchor="middle">Pressure Helper</text>
            <text x="340" y="255" class="label" text-anchor="middle">✨ The Magic Sponge Filter ✨</text>
            <text x="600" y="175" class="label" text-anchor="middle">Spinning Turbine!</text>
            
            <text x="665" y="18" class="label" text-anchor="middle" opacity="{lightning_opacity}">SCORE!</text>
            <text x="665" y="38" class="dyn-val" text-anchor="middle" fill="#ea580c" font-size="18" opacity="{lightning_opacity}">{power_density:.2f} Watts</text>
            
            {overload_overlay}
        </svg>
    </div>
    """
    st.components.v1.html(pfd_html, height=350)

# ==========================================
# ROW 2: HORIZONTAL INLINE SCOREBOARD 
# ==========================================
st.markdown("---")
st.markdown("### 🕹️ Live Scoreboard")

m1, m2, m3 = st.columns(3)

card_style = """
    background-color: #ffffff; 
    border: 4px solid #bae6fd; 
    border-radius: 20px; 
    padding: 12px 20px; 
    display: flex; 
    flex-direction: row; 
    justify-content: space-between; 
    align-items: center; 
    box-shadow: 0 6px 12px rgba(0,0,0,0.08);
"""
label_style = "font-size: 1.6rem; font-weight: 900; color: #334155; text-align: left; line-height: 1;"

val_color = "#ef4444" if is_overload else "#ea580c"
value_style = f"font-size: 3.2rem; font-weight: 900; color: {val_color}; text-shadow: 2px 2px #fef08a; line-height: 1; margin-left: 10px;"

with m1:
    st.markdown(f"""
        <div style="{card_style}">
            <div style="{label_style}">⚡ ELECTRICITY SCORE! (Watts)</div>
            <div style="{value_style}">{power_density:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
        <div style="{card_style}">
            <div style="{label_style}">💦 Water Speed Through Filter</div>
            <div style="{value_style}">{jw:.1f}</div>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
        <div style="{card_style}">
            <div style="{label_style}">🧲 Natural Osmotic Push (Bar)</div>
            <div style="{value_style}">{delta_pi_eff:.1f}</div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# ROW 3: POWER MOUNTAIN CHART
# ==========================================
st.markdown("---")
st.markdown("### ⛰️ Can you climb the Power Mountain?")
st.markdown("<div style='font-size: 1.8rem; font-weight: 900; color: #334155; padding-bottom: 15px;'>🎯 Move the red ball to the very top of the green mountain to get the highest score!</div>", unsafe_allow_html=True)

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
    'Turbine Resistance (Bar)': p_space,
    'Power Score (Watts)': w_space
})

df_point = pd.DataFrame({
    'Turbine Resistance (Bar)': [pressure],
    'Power Score (Watts)': [power_density]
})

area_color = alt.Gradient(
    gradient='linear',
    stops=[alt.GradientStop(color='#fca5a5' if is_overload else '#bbf7d0', offset=0), 
           alt.GradientStop(color='#ef4444' if is_overload else '#22c55e', offset=1)],
    x1=1, x2=1, y1=1, y2=0
)

area_chart = alt.Chart(df_curve).mark_area(
    color=area_color,
    opacity=0.8
).encode(
    x=alt.X('Turbine Resistance (Bar):Q', scale=alt.Scale(domain=[0, 50])),
    y=alt.Y('Power Score (Watts):Q', title='Power Score (Watts)', scale=alt.Scale(domain=[0, max(w_space)*1.2 if max(w_space)>0 else 5])),
    tooltip=['Turbine Resistance (Bar)', 'Power Score (Watts)']
)

point_chart = alt.Chart(df_point).mark_circle(color='#b91c1c' if is_overload else '#ef4444', size=600, opacity=1).encode(
    x='Turbine Resistance (Bar):Q',
    y='Power Score (Watts):Q',
    tooltip=['Turbine Resistance (Bar)', 'Power Score (Watts)']
)

final_chart = alt.layer(area_chart, point_chart).properties(height=280).interactive().configure_axis(
    labelFontSize=16,
    titleFontSize=20,
    titleFontWeight='bold',
    labelColor='#334155',
    titleColor='#0f172a',
    gridColor='#f1f5f9'
)
st.altair_chart(final_chart, use_container_width=True)
