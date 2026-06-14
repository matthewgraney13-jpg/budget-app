import streamlit as st
import pandas as pd
import os

# --- ADVANCED MOBI-FIRST DESIGN SYSTEM ---
st.set_page_config(page_title="Matt & Kait", layout="centered")

# Custom CSS to force a gorgeous, clean, mobile-first design layout
st.markdown("""
    <style>
    /* Global Background & Font Reset */
    .main { background-color: #F4F7FA; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 480px !important; }
    
    /* Sleek Title Card */
    .app-title { text-align: center; color: #0F172A; font-size: 24px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 5px; }
    .app-subtitle { text-align: center; color: #64748B; font-size: 13px; margin-bottom: 20px; }
    
    /* Clean iOS Card Layouts */
    div[data-testid="stMetricValue"] { font-size: 22px !important; font-weight: 700 !important; color: #0F172A !important; }
    div[data-testid="stMetricLabel"] { font-size: 12px !important; font-weight: 600 !important; color: #64748B !important; text-transform: uppercase; letter-spacing: 0.5px; }
    .stMetric {
        background-color: #FFFFFF !important; padding: 16px !important; border-radius: 16px !important;
        box-shadow: 0px 4px 20px rgba(15, 23, 42, 0.04) !important; border: 1px solid #E2E8F0 !important;
    }
    
    /* Action Button Makeover */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); color: white; 
        border-radius: 14px; padding: 12px; font-weight: 700; border: none; width: 100%;
        box-shadow: 0px 4px 12px rgba(59, 130, 246, 0.3); font-size: 15px; margin-top: 15px;
    }
    div.stButton > button:first-child:hover { background: #1D4ED8; color: white; }
    
    /* Custom Card Containers */
    .section-card {
        background-color: #FFFFFF; padding: 16px; border-radius: 16px;
        border: 1px solid #E2E8F0; margin-bottom: 15px;
    }
    
    /* Hide Default Side Navigation Clutter on Tiny Mobile Screens */
    .css-163e8hi { background-color: #FFFFFF; }
    hr { margin: 15px 0 !important; border-top: 1px solid #E2E8F0 !important; }
    </style>
""", unsafe_allow_html=True)

# App Branding Headers
st.markdown("<div class='app-title'>🚀 Matt & Kait's Runway</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>Your simple, high-speed financial tracker</div>", unsafe_allow_html=True)

# Data Log Configuration 
DATA_FILE = "budget_history.csv"
def load_data():
    if os.path.exists(DATA_FILE): return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Month", "Situation", "Matt_Pocket", "Kait_Pocket", "Joint_Savings", "MacBook_Savings"])

def save_data(df): df.to_csv(DATA_FILE, index=False)
history_df = load_data()

# --- APP NAVIGATION CENTER ---
st.sidebar.markdown("### 🧭 App View")
app_mode = st.sidebar.radio("Jump To View:", ["✨ Live App Dashboard", "📊 Our Monthly Logs"])
phase = st.sidebar.radio("Living Setup:", ["📍 Phase 1: At Parents", "🔑 Phase 2: Our Own Flat"])

# Clean Salary Segment Inputs
st.markdown("### 💰 Monthly Paychecks")
col1, col2 = st.columns(2)
with col1: m_net = st.number_input("Matt's Net (R):", value=33880, step=100)
with col2: p_net = st.number_input("Kait's Net (R):", value=15100, step=100)

m_fixed_bills = 12120

# -------------------------------------------------------------
# MODE 1: LIVE INTERACTIVE APP DASHBOARD
# -------------------------------------------------------------
if app_mode == "✨ Live App Dashboard":
    
    if phase == "📍 Phase 1: At Parents":
        st.caption("✨ Living at Parents: Max savings mode for UK tickets & MacBook Air.")
        parent_rent = 4000
        
        st.markdown("### 🎛️ Allocation Sliders")
        m_save = st.slider("Matt to Joint Savings (R):", 5000, 15000, 12000, 500)
        p_save = st.slider("Kait to Joint Savings (R):", 3000, 10000, 7500, 500)
        macbook_save = st.slider("Kait to MacBook Stash (R):", 1000, 6000, 4000, 500)
            
        m_leftover = m_net - m_fixed_bills - parent_rent - m_save
        p_leftover = p_net - p_save - macbook_save
        total_saved_this_month = m_save + p_save
        
    else:
        st.caption("🏡 Renting Together: Splitting household bills proportionally (~69% / 31%).")
        
        target_rent = st.slider("Test Rental Price (R):", 9000, 16000, 13000, 500)
        household_utilities = st.slider("Groceries, Lights & Wi-Fi (R):", 4000, 9000, 6500, 250)
        
        total_household_cost = target_rent + household_utilities
        m_prop_share = int(total_household_cost * 0.69)
        p_prop_share = int(total_household_cost * 0.31)
        
        # Display the proportional split calculation in a clean block
        st.markdown(f"""
        <div class='section-card'>
            <span style='color:#64748B; font-size:12px; font-weight:700;'>PROPORTIONAL BILL SPLIT</span><br>
            <span style='font-size:14px; color:#0F172A;'>• Matt Pays (69%): <b>R{m_prop_share:,}</b></span><br>
            <span style='font-size:14px; color:#0F172A;'>• Kait Pays (31%): <b>R{p_prop_share:,}</b></span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ✈️ Travel Contributions")
        col_s1, col_s2 = st.columns(2)
        with col_s1: m_uk_save = st.number_input("Matt UK Save (R):", value=3200, step=100)
        with col_s2: p_uk_save = st.number_input("Kait UK Save (R):", value=1400, step=100)
            
        m_leftover = m_net - m_fixed_bills - m_prop_share - m_uk_save
        p_leftover = p_net - p_prop_share - p_uk_save
        total_saved_this_month = m_uk_save + p_uk_save
        macbook_save = 0

    # DISPLAY REMAINING SPENDING CASH POCKETS
    st.markdown("---")
    st.markdown("### 💎 Available Pocket Money")
    cm1, cm2 = st.columns(2)
    with cm1: st.metric(label="Matt's Cash Left", value=f"R{m_leftover:,}")
    with cm2: st.metric(label="Kait's Cash Left", value=f"R{p_leftover:,}")
        
    st.markdown("---")
    st.markdown("### 🎯 Core Target Progress")
    
    st.write(f"**Joint Monthly Travel Stash:** R{total_saved_this_month:,} / R19,500 target")
    st.progress(min(1.0, total_saved_this_month / 19500))
    
    if phase == "📍 Phase 1: At Parents":
        st.write(f"**Kait's MacBook Fund Allocation:** R{macbook_save:,} / R4,000 target")
        st.progress(min(1.0, macbook_save / 4000))

    # --- SIMPLIFIED LOGGING PANEL ---
    st.markdown("---")
    st.markdown("### 🔒 Log This Month")
    month_select = st.selectbox("Select Active Month:", [f"Month {i}" for i in range(1, 13)])
    
    if st.button("Commit Current Month to Record Logs"):
        history_df = history_df[history_df["Month"] != month_select]
        new_row = {
            "Month": month_select, "Situation": phase,
            "Matt_Pocket": m_leftover, "Kait_Pocket": p_leftover,
            "Joint_Savings": total_saved_this_month, "MacBook_Savings": macbook_save
        }
        history_df = pd.concat([history_df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(history_df)
        st.balloons()
        st.success(f"Log sheet metrics for {month_select} saved securely!")

# -------------------------------------------------------------
# MODE 2: VISUAL HISTORICAL OVERVIEW
# -------------------------------------------------------------
else:
    st.markdown("### 📈 Running Capital Stack")
    
    if history_df.empty:
        st.warning("No recorded logs found yet! Head over to the Live App Dashboard to track your first month.")
    else:
        total_joint_pool = history_df["Joint_Savings"].sum()
        total_macbook_pool = history_df["MacBook_Savings"].sum() + 10000 
        
        tc1, tc2 = st.columns(2)
        with tc1: st.metric("Total Travel Capital Stacked", f"R{total_joint_pool:,}")
        with tc2: st.metric("Kait's Laptop Fund", f"R{total_macbook_pool:,} / R22,000")
            
        if total_macbook_pool >= 22000:
            st.snow()
            st.success("💻 MacBook Air completely funded! Enjoy the store run, Kait! 🎉")
            
        st.markdown("---")
        st.markdown("### 📅 Historic Database Entries")
        
        display_df = history_df.copy()
        display_df.columns = ["Month", "Living Setup", "Matt Cash", "Kait Cash", "Joint Savings", "MacBook Stash"]
        st.dataframe(display_df.set_index("Month"), use_container_width=True)
        
        if st.sidebar.button("⚠️ Reset Database"):
            if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
            st.rerun()
