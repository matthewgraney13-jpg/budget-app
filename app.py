import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIGURATION & THEME INJECTION ---
st.set_page_config(page_title="Matt & Kait's Dashboard", layout="centered")

# Custom CSS to make the interface look like a friendly, modern mobile app
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    div.stButton > button:first-child {
        background-color: #4A90E2; color: white; border-radius: 20px;
        padding: 10px 24px; font-weight: bold; border: none; width: 100%;
        box-shadow: 0px 4px 10px rgba(74, 144, 226, 0.3);
    }
    div.stButton > button:first-child:hover { background-color: #357ABD; color: white; }
    .reportview-container .main .block-container { max-width: 600px; }
    h1 { color: #1B365D; font-family: 'Segoe UI', sans-serif; font-weight: 800; }
    h3 { color: #2C3E50; font-family: 'Segoe UI', sans-serif; font-weight: 600; margin-top: 20px; }
    .stMetric {
        background-color: white; padding: 15px; border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05); border-left: 5px solid #4A90E2;
    }
    </style>
""", unsafe_allow_html=True)

# App Title & Welcoming Header
st.markdown("<h1>🚀 Matt & Kait's Financial Runway</h1>", unsafe_allow_html=True)
st.write("---")

# Data File System Setup
DATA_FILE = "budget_history.csv"
def load_data():
    if os.path.exists(DATA_FILE): return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Month", "Situation", "Matt_Pocket", "Kait_Pocket", "Joint_Savings", "MacBook_Savings"])

def save_data(df): df.to_csv(DATA_FILE, index=False)
history_df = load_data()

# --- APP MENU NAVIGATION ---
st.sidebar.markdown("### 🧭 App Control Center")
app_mode = st.sidebar.radio("Jump To View:", ["✨ Live App Dashboard", "📊 Our Monthly Logs"])
phase = st.sidebar.radio("Living Setup:", ["📍 Phase 1: Staying at Parents", "🔑 Phase 2: Our Own Apartment"])

st.sidebar.markdown("---")
st.sidebar.write("Designed with ❤️ for Matt & Kait")

# Shared Baseline Income Inputs
st.markdown("### 💰 Monthly Take-Home Pay Checks")
col1, col2 = st.columns(2)
with col1:
    m_net = st.number_input("Matt's Salary (R):", value=33880, step=100)
with col2:
    p_net = st.number_input("Kait's Salary (R):", value=15100, step=100)

m_fixed_bills = 12120

# -------------------------------------------------------------
# MODE 1: LIVE INTERACTIVE APP DASHBOARD
# -------------------------------------------------------------
if app_mode == "✨ Live App Dashboard":
    
    if phase == "📍 Phase 1: Staying at Parents":
        st.markdown("### 🏡 Phase 1: Parent Basecamp (Months 1–3)")
        st.caption("Goal: Clear out UK flights/visas & maximize Kait's tech fund stack up.")
        
        parent_rent = 4000
        
        # Interactive Slide Controls
        st.markdown("### 🎛️ Adjust Allocations for This Month")
        m_save = st.slider("Matt's Joint Savings Target (R):", 5000, 15000, 12000, 500)
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            p_save = st.number_input("Kait's Shared Contribution (R):", value=7500, step=500)
        with col_k2:
            macbook_save = st.number_input("Kait's MacBook Air Allocation (R):", value=4000, step=500)
            
        # Mathematical Breakdown Engines
        m_leftover = m_net - m_fixed_bills - parent_rent - m_save
        p_leftover = p_net - p_save - macbook_save
        total_saved_this_month = m_save + p_save
        
    else:
        st.markdown("### 🔑 Phase 2: Our New Flat (Months 4–12)")
        st.caption("Goal: Living in Bellville/Durbanville out of a balanced, fair income split.")
        
        # Rent Testing Sliders
        target_rent = st.slider("Select Rental Price Tag (R):", 9000, 16000, 13000, 500)
        household_utilities = st.slider("Estimated Variable Utilities & Groceries (R):", 4000, 9000, 6500, 250)
        
        total_household_cost = target_rent + household_utilities
        
        # Proportional calculation splits (69% Matt / 31% Kait)
        m_prop_share = int(total_household_cost * 0.69)
        p_prop_share = int(total_household_cost * 0.31)
        
        st.success(f"🏡 Total Joint Flat Expenses: **R{total_household_cost:,}** (Matt pays R{m_prop_share:,} | Kait pays R{p_prop_share:,})")
        
        st.markdown("### ✈️ Ongoing UK Holiday Savings Pool")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            m_uk_save = st.number_input("Matt's UK Ticket Slice (R):", value=3200, step=100)
        with col_s2:
            p_uk_save = st.number_input("Kait's UK Ticket Slice (R):", value=1400, step=100)
            
        m_leftover = m_net - m_fixed_bills - m_prop_share - m_uk_save
        p_leftover = p_net - p_prop_share - p_uk_save
        total_saved_this_month = m_uk_save + p_uk_save
        macbook_save = 0

    # DISPLAY INTERACTIVE OUTPUT CARDS
    st.markdown("---")
    st.markdown("### 💎 Your Free Spending Pocket Money")
    
    cm1, cm2 = st.columns(2)
    with cm1:
        st.metric(label="Matt's Spending Cash", value=f"R{m_leftover:,}", delta="Safe Buffer" if m_leftover > 3000 else "Tight Margin")
    with cm2:
        st.metric(label="Kait's Spending Cash", value=f"R{p_leftover:,}", delta="Safe Buffer" if p_leftover > 3000 else "Tight Margin")
        
    st.markdown("---")
    st.markdown("### 🎯 Shared Progress Toward Goal Targets This Month")
    
    st.write(f"**Joint Monthly Travel/Moving Stash Saved:** R{total_saved_this_month:,} / R19,500 target")
    st.progress(min(1.0, total_saved_this_month / 19500))
    
    if phase == "📍 Phase 1: Staying at Parents":
        st.write(f"**Kait's MacBook Air Monthly Chunk Added:** R{macbook_save:,} / R4,000 target")
        st.progress(min(1.0, macbook_save / 4000))

    # --- HISTORICAL LOCK BUTTON ---
    st.write("### 🔒 Finish Line Log")
    month_select = st.selectbox("Which Month are you locking down?", [f"Month {i}" for i in range(1, 13)])
    
    if st.button("Log this Month into Our History Records"):
        history_df = history_df[history_df["Month"] != month_select]
        new_row = {
            "Month": month_select, "Situation": phase,
            "Matt_Pocket": m_leftover, "Kait_Pocket": p_leftover,
            "Joint_Savings": total_saved_this_month, "MacBook_Savings": macbook_save
        }
        history_df = pd.concat([history_df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(history_df)
        st.balloons()
        st.success(f"📦 Great job! {month_select} financial statistics are officially banked!")

# -------------------------------------------------------------
# MODE 2: VISUAL HISTORICAL OVERVIEW
# -------------------------------------------------------------
else:
    st.markdown("### 📈 Our Shared Ledger & Track Record")
    
    if history_df.empty:
        st.warning("No entry records saved yet! Head over to the Live App Dashboard to track your first month together.")
    else:
        # Compute Running Totals dynamically
        total_joint_pool = history_df["Joint_Savings"].sum()
        total_macbook_pool = history_df["MacBook_Savings"].sum() + 10000 # Adds Kait's initial R10k seed cash
        
        st.markdown("### 🏆 Total Assets Accumulated to Date")
        tc1, tc2 = st.columns(2)
        with tc1:
            st.metric("Total Travel/Moving Capital Stacked", f"R{total_joint_pool:,}")
        with tc2:
            st.metric("Kait's Running MacBook Bank", f"R{total_macbook_pool:,} / R22,000")
            
        if total_macbook_pool >= 22000:
            st.snow()
            st.success("💻 MacBook Air fully unlocked! Head to the iStore, Kait! 🛍️")
            
        st.markdown("### 📅 Review Past Performance History Logs")
        display_df = history_df.copy()
        display_df.columns = ["Month", "Living State", "Matt Pocket Money", "Kait Pocket Money", "Joint Capital Banked", "MacBook Stash"]
        st.dataframe(display_df.set_index("Month"), use_container_width=True)
        
        # Clear Data Trigger
        if st.sidebar.button("⚠️ Clear App Database Records"):
            if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
            st.rerun()
