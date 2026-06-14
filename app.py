import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(page_title="Matt & Kait's Budget Tracker", layout="centered")

st.title("📊 Matt & Kait: Financial Dashboard")
st.write("Track your monthly savings, log your real history, and see your progress over time.")

# --- PERSISTENT DATA STORAGE SYSTEM ---
# This creates a small database file on your server to save your history over time
DATA_FILE = "budget_history.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Month", "Situation", "Matt_Pocket_Money", "Kait_Pocket_Money", "Joint_Savings_Logged", "Kait_MacBook_Savings"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

history_df = load_data()

# Sidebar App Navigation
st.sidebar.header("Navigation")
app_mode = st.sidebar.radio("Go To Section:", ["Live Budget Calculator", "Our Historical Logs"])
phase = st.sidebar.radio("Select Current Living Situation:", ["Phase 1: Living with Parents", "Phase 2: Moved Out / Renting"])

# --- SHARED INCOME INPUTS ---
st.subheader("💰 Income Input (Monthly Take-Home)")
col1, col2 = st.columns(2)
with col1:
    m_net = st.number_input("Matt's Take-Home Pay (R):", value=33880, step=100)
with col2:
    p_net = st.number_input("Kait's Take-Home Pay (R):", value=15100, step=100)

m_fixed_bills = 12120

# -------------------------------------------------------------
# MODE 1: LIVE BUDGET CALCULATOR & LOGGING
# -------------------------------------------------------------
if app_mode == "Live Budget Calculator":
    
    if phase == "Phase 1: Living with Parents":
        st.subheader("📍 Phase 1: Staying at Kait's Parents (Months 1-3)")
        parent_rent = 4000
        
        # Savings Inputs
        st.write("### Monthly Allocations")
        col3, col4, col5 = st.columns(3)
        with col3:
            m_save = st.number_input("Matt's Joint Savings Pool (Target: R12,000):", value=12000, step=500)
        with col4:
            p_save = st.number_input("Kait's Joint Savings Pool (Target: R7,500):", value=7500, step=500)
        with col5:
            macbook_save = st.number_input("Kait's MacBook Fund (Target: R4,000):", value=4000, step=500)
            
        # Calculations
        m_leftover = m_net - m_fixed_bills - parent_rent - m_save
        p_leftover = p_net - p_save - macbook_save
        total_saved_this_month = m_save + p_save
        
        st.markdown("---")
        st.subheader("🔍 Current Month Outcome")
        
        c_m, c_p, c_s = st.columns(3)
        c_m.metric("Matt's Pocket Money", f"R{m_leftover:,}")
        c_p.metric("Kait's Pocket Money", f"R{p_leftover:,}")
        c_s.metric("Joint Pool Saved", f"R{total_saved_this_month:,}")
        
    else:
        st.subheader("🔑 Phase 2: Living in Your Own Place (Months 4-12)")
        target_rent = st.slider("Test Rental Price (R):", min_value=9000, max_value=16000, value=13000, step=500)
        household_utilities = st.number_input("Estimated Shared Living Costs (Groceries, Wi-Fi, Lights) (R):", value=6500, step=200)
        
        total_household_cost = target_rent + household_utilities
        m_prop_share = int(total_household_cost * 0.69)
        p_prop_share = int(total_household_cost * 0.31)
        
        st.write("### Ongoing UK Travel Savings")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            m_uk_save = st.number_input("Matt's UK Share (R):", value=3200, step=100)
        with col_s2:
            p_uk_save = st.number_input("Kait's UK Share (R):", value=1400, step=100)
            
        m_leftover = m_net - m_fixed_bills - m_prop_share - m_uk_save
        p_leftover = p_net - p_prop_share - p_uk_save
        total_saved_this_month = m_uk_save + p_uk_save
        macbook_save = 0  # Reached target in phase 1
        
        st.markdown("---")
        st.subheader("🔍 Current Month Outcome")
        cc1, cc2, cc3 = st.columns(3)
        cc1.metric("Matt's Pocket Money", f"R{m_leftover:,}")
        cc2.metric("Kait's Pocket Money", f"R{p_phase2_leftover if 'p_phase2_leftover' in locals() else p_leftover:,}")
        cc3.metric("Holiday Savings Added", f"R{total_saved_this_month:,}")

    # --- SAVE TO DATABASE BUTTON ---
    st.markdown("### 💾 Lock in this Month's Numbers")
    month_select = st.selectbox("Select Month to Log:", ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6", "Month 7", "Month 8", "Month 9", "Month 10", "Month 11", "Month 12"])
    
    if st.button("Save this Month into History"):
        # Drop older log for same month if it exists to avoid duplication
        history_df = history_df[history_df["Month"] != month_select]
        
        new_row = {
            "Month": month_select,
            "Situation": phase,
            "Matt_Pocket_Money": m_leftover,
            "Kait_Pocket_Money": p_leftover,
            "Joint_Savings_Logged": total_saved_this_month,
            "Kait_MacBook_Savings": macbook_save
        }
        
        history_df = pd.concat([history_df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(history_df)
        st.success(f"🎉 Successfully saved data for {month_select}!")

# -------------------------------------------------------------
# MODE 2: HISTORICAL OVERVIEW & RUNNING TALLIES
# ----------------
