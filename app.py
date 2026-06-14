import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Matthew & Partner Budget Tracker", layout="centered")

st.title("📊 Matthew & Partner: Budget & Relocation App")
st.write("Use this interactive tool to log expenses, check your savings goals, and adjust your budget.")

# Sidebar Navigation
phase = st.sidebar.radio("Select Current Living Situation:", ["Phase 1: Living with Parents", "Phase 2: Moved Out / Renting"])

# --- INCOME INPUTS ---
st.subheader("💰 Income Input (Monthly Take-Home)")
col1, col2 = st.columns(2)
with col1:
    m_net = st.number_input("Matthew Take-Home Pay (R):", value=33880, step=100)
with col2:
    p_net = st.number_input("Partner Take-Home Pay (R):", value=15100, step=100)

total_income = m_net + p_net
st.info(f"**Total Household Net Income Pool:** R{total_income:,}")

# --- FIXED COST DEFAULTS ---
m_fixed_bills = 12120

# --- PHASE 1 LOGIC ---
if phase == "Phase 1: Living with Parents":
    st.subheader("📍 Phase 1: Staying at Her Parents (Months 1-3)")
    st.write("Goal: Purchase UK flights/visas & build rent deposit while tracking the MacBook Air fund.")
    
    parent_rent = 4000
    
    # Savings Inputs
    st.write("### Monthly Savings Allocations")
    col3, col4, col5 = st.columns(3)
    with col3:
        m_save = st.number_input("Matthew Joint Savings (Target: R12,000):", value=12000, step=500)
    with col4:
        p_save = st.number_input("Partner Joint Savings (Target: R7,500):", value=7500, step=500)
    with col5:
        macbook_save = st.number_input("Partner MacBook Fund (Target: R4,000):", value=4000, step=500)
        
    # Final Calculations
    m_leftover = m_net - m_fixed_bills - parent_rent - m_save
    p_leftover = p_net - p_save - macbook_save
    total_saved_this_month = m_save + p_save
    
    st.markdown("---")
    st.subheader("🔍 3-Month Status & Pocket Money Outcomes")
    
    # Visual metrics
    c_m, c_p, c_s = st.columns(3)
    c_m.metric("Matthew Pocket Money", f"R{m_leftover:,}")
    c_p.metric("Partner Pocket Money", f"R{p_leftover:,}")
    c_s.metric("Monthly Joint Pool Saved", f"R{total_saved_this_month:,}")
    
    # Progress bars toward goals
    st.write("### Target Deadlines Progress (Over 3 Months)")
    st.progress(min(1.0, total_saved_this_month / 19500), text=f"Joint Moving & Holiday Savings Progress ({int((total_saved_this_month/19500)*100)}% of monthly target)")
    st.progress(min(1.0, macbook_save / 4000), text=f"Partner MacBook Air Goal Progress ({int((macbook_save/4000)*100)}% of monthly target)")

# --- PHASE 2 LOGIC ---
else:
    st.subheader("🔑 Phase 2: In Your Own Place (Months 4-12)")
    st.write("Goal: Live in Bellville/Durbanville while maintaining a fair, proportional cost split.")
    
    # Custom sliders for testing rent options
    target_rent = st.slider("Test Rental Price (R):", min_value=9000, max_value=16000, value=13000, step=500)
    household_utilities = st.number_input("Estimated Shared Living Costs (Groceries, Wi-Fi, Lights) (R):", value=6500, step=200)
    
    total_household_cost = target_rent + household_utilities
    st.warning(f"Total Shared Household Cost: R{total_household_cost:,}")
    
    # Proportional splits calculation (~69% / 31%)
    m_prop_share = int(total_household_cost * 0.69)
    p_prop_share = int(total_household_cost * 0.31)
    
    st.write("### Proportional Split Breakdown")
    st.write(f"*   **Matthew Pays (69%):** R{m_prop_share:,} toward rent & household bills")
    st.write(f"*   **Partner Pays (31%):** R{p_prop_share:,} toward rent & household bills")
    
    # Holiday Ongoing Savings
    st.write("### Ongoing UK Travel Savings")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        m_uk_save = st.number_input("Matthew UK Share (R):", value=3200, step=100)
    with col_s2:
        p_uk_save = st.number_input("Partner UK Share (R):", value=1400, step=100)
        
    # Final Leftover Outcomes
    m_phase2_leftover = m_net - m_fixed_bills - m_prop_share - m_uk_save
    p_phase2_leftover = p_net - p_prop_share - p_uk_save
    
    st.markdown("---")
    st.subheader("🔍 Remaining Monthly Pocket Money")
    cc1, cc2 = st.columns(2)
    cc1.metric("Matthew Leftover Cash", f"R{m_phase2_leftover:,}")
    cc2.metric("Partner Leftover Cash", f"R{p_phase2_leftover:,}")
    
    if m_phase2_leftover < 2000 or p_phase2_leftover < 2000:
        st.error("⚠️ Warning: Leftover spending cash is low! Consider sliding the rental price down.")
    else:
        st.success("✅ Financial Plan Healthy: Both parties maintain a comfortable pocket money safety margin!")

