import streamlit as st
import pandas as pd
import os

# --- VIBRANT & CUTE DESIGN SYSTEM ---
st.set_page_config(page_title="Matt & Kait's Runway", layout="centered")

# Injecting the bright, playful aesthetic with custom CSS
st.markdown("""
    <style>
    /* Gradient Background & Soft Fonts */
    .main { 
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
    }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 480px !important; }
    
    /* Playful Header Banner */
    .header-box {
        background: linear-gradient(135deg, #FF758C 0%, #FF7EB3 100%);
        padding: 24px; border-radius: 24px; text-align: center;
        box-shadow: 0px 10px 25px rgba(255, 117, 140, 0.3); margin-bottom: 25px;
    }
    .app-title { color: #FFFFFF; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 5px; }
    .app-subtitle { color: #FFE4E8; font-size: 13px; font-weight: 500; }
    
    /* Cute Rounded Cards */
    .section-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 20px;
        border: none; box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.04); margin-bottom: 20px;
    }
    
    /* Custom Metric Badges */
    div[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 800 !important; color: #1E293B !important; }
    div[data-testid="stMetricLabel"] { font-size: 12px !important; font-weight: 700 !important; color: #64748B !important; }
    .stMetric {
        background-color: #FFFFFF !important; padding: 16px !important; border-radius: 18px !important;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.03) !important; border-top: 4px solid #FF758C !important;
    }
    
    /* Big Happy Interactive Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF758C 0%, #FF7EB3 100%); color: white; 
        border-radius: 16px; padding: 12px; font-weight: 700; border: none; width: 100%;
        box-shadow: 0px 6px 15px rgba(255, 117, 140, 0.4); font-size: 15px; margin-top: 10px;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover { transform: translateY(-2px); box-shadow: 0px 8px 20px rgba(255, 117, 140, 0.5); }
    
    /* Cute slider look modification */
    .stSlider > div [data-baseweb="slider"] { background-color: #FFE4E8; }
    </style>
""", unsafe_allow_html=True)

# App Branding Banner Block
st.markdown("""
    <div class='header-box'>
        <div class='app-title'>✨ Matt & Kait's Runway ✨</div>
        <div class='app-subtitle'>💖 Tracking our dreams & pocket money together 💖</div>
    </div>
""", unsafe_allow_html=True)

# --- LOCAL STORAGE FILES ---
BUDGET_FILE = "budget_history.csv"
EXPENSE_FILE = "expense_logs.csv"

def load_data(file, columns):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame(columns=columns)

history_df = load_data(BUDGET_FILE, ["Month", "Situation", "Matt_Pocket", "Kait_Pocket", "Joint_Savings", "MacBook_Savings"])
expense_df = load_data(EXPENSE_FILE, ["Who", "What", "Amount", "Category"])

# --- SIDEBAR CONTROL CENTER ---
st.sidebar.markdown("### 🗺️ App Navigation")
app_mode = st.sidebar.radio("Jump To View:", ["💖 Live App Dashboard", "🛍️ Log a New Purchase", "📊 Our Monthly Logs"])
phase = st.sidebar.radio("Living Setup:", ["📍 Phase 1: At Parents", "🔑 Phase 2: Our Own Flat"])

# Base Salaries
m_net, p_net, m_fixed_bills = 33880, 15100, 12120

# Calculate Live Baselines depending on the active phase setup
if phase == "📍 Phase 1: At Parents":
    parent_rent = 4000
    m_save_base, p_save_base, mac_save_base = 12000, 7500, 4000
    m_calc_pocket = m_net - m_fixed_bills - parent_rent - m_save_base
    p_calc_pocket = p_net - p_save_base - mac_save_base
    total_saved_this_month = m_save_base + p_save_base
else:
    target_rent, household_utilities = 13000, 6500
    total_household = target_rent + household_utilities
    m_share, p_share = int(total_household * 0.69), int(total_household * 0.31)
    m_uk, p_uk = 3200, 1400
    m_calc_pocket = m_net - m_fixed_bills - m_share - m_uk
    p_calc_pocket = p_net - p_share - p_uk
    total_saved_this_month = m_uk + p_uk
    mac_save_base = 0

# Deduct cumulative daily items from running pocket balances
matt_total_spent = expense_df[expense_df["Who"] == "Matt"]["Amount"].sum()
kait_total_spent = expense_df[expense_df["Who"] == "Kait"]["Amount"].sum()

m_final_pocket = m_calc_pocket - matt_total_spent
p_final_pocket = p_calc_pocket - kait_total_spent

# -------------------------------------------------------------
# VIEW 1: LIVE APP DASHBOARD
# -------------------------------------------------------------
if app_mode == "💖 Live App Dashboard":
    
    if phase == "📍 Phase 1: At Parents":
        st.markdown("### 🏡 Phase 1: Parent Basecamp")
        st.write("✨ Max savings mode for UK tickets & Kait's MacBook Air!")
        
        st.markdown("### 🎛️ Adjust Allocations for This Month")
        m_save = st.slider("Matt's Joint Savings Target (R):", 5000, 15000, 12000, 500)
        p_save = st.slider("Kait's Joint Savings Target (R):", 3000, 10000, 7500, 500)
        macbook_save = st.slider("Kait's MacBook Air Target (R):", 1000, 6000, 4000, 500)
        
        # Recalculate with slider changes
        m_calc_pocket = m_net - m_fixed_bills - 4000 - m_save
        p_calc_pocket = p_net - p_save - macbook_save
        m_final_pocket = m_calc_pocket - matt_total_spent
        p_final_pocket = p_calc_pocket - kait_total_spent
        total_saved_this_month = m_save + p_save
    else:
        st.markdown("### 🔑 Phase 2: Our Own Apartment")
        st.write("✨ Living beautifully in Bellville/Durbanville with a fair proportional split.")
        
        st.markdown(f"""
        <div class='section-card'>
            <span style='color:#FF758C; font-size:12px; font-weight:700;'>🏡 OUR ESTIMATED BILLS SPLIT</span><br>
            <span style='font-size:15px; color:#1E293B;'>• Matt Pays (69% Share): <b>R{int((13000+6500)*0.69):,}</b></span><br>
            <span style='font-size:15px; color:#1E293B;'>• Kait Pays (31% Share): <b>R{int((13000+6500)*0.31):,}</b></span>
        </div>
        """, unsafe_allow_html=True)

    # SHOW ACCUMULATED BALANCES
    st.markdown("### 🍉 Available Running Pocket Money")
    st.caption("This factors in all your individual daily fun purchases logged below!")
    cm1, cm2 = st.columns(2)
    with cm1: st.metric(label="Matt's Cash Remaining", value=f"R{m_final_pocket:,}")
    with cm2: st.metric(label="Kait's Cash Remaining", value=f"R{p_final_pocket:,}")
        
    st.markdown("---")
    st.markdown("### 🎯 Core Target Progress")
    st.write(f"**✈️ Shared UK Ticket Pot:** R{total_saved_this_month:,} / R19,500 target")
    st.progress(min(1.0, total_saved_this_month / 19500))
    
    if phase == "📍 Phase 1: At Parents":
        st.write(f"**💻 Kait's MacBook Fund:** R{macbook_save:,} / R4,000 target")
        st.progress(min(1.0, macbook_save / 4000))

    # LOCK MONTH BUTTON
    st.markdown("---")
    st.markdown("### 🔒 Lock This Month")
    month_select = st.selectbox("Which Month are we closing?", [f"Month {i}" for i in range(1, 13)])
    if st.button("Commit This Month to History"):
        history_df = history_df[history_df["Month"] != month_select]
        new_row = {"Month": month_select, "Situation": phase, "Matt_Pocket": m_final_pocket, "Kait_Pocket": p_final_pocket, "Joint_Savings": total_saved_this_month, "MacBook_Savings": macbook_save_base}
        history_df = pd.concat([history_df, pd.DataFrame([new_row])], ignore_index=True)
        history_df.to_csv(BUDGET_FILE, index=False)
        st.balloons()
        st.success(f"Log metrics for {month_select} locked down!")

# -------------------------------------------------------------
# VIEW 2: CUTE EXPENSE LOGGER
# -------------------------------------------------------------
elif app_mode == "🛍️ Log a New Purchase":
    st.markdown("### 🧁 Fun Expense Logger & Piggy Bank")
    st.write("Did you buy a coffee, go on a date, or shop? Drop it here to instantly slice it from your pocket cash balance!")
    
    with st.form("expense_form", clear_on_submit=True):
        who_spent = st.radio("Who spent the money? 🤔", ["Matt", "Kait"])
        item_name = st.text_input("What did you buy? ☕🛍️", placeholder="e.g., Starbucks, Woolies, Fuel")
        spent_amount = st.number_input("Amount (Rands):", min_value=0, value=150, step=10)
        item_cat = st.selectbox("Category Group:", ["Date Night & Food", "Fuel & Petrol", "Shopping & Fun", "Other Stuff"])
        
        submit_expense = st.form_submit_form_button = st.form_submit_button("Add to My Daily Logs 💸")
        
        if submit_expense and item_name:
            new_exp = {"Who": who_spent, "What": item_name, "Amount": spent_amount, "Category": item_cat}
            expense_df = pd.concat([expense_df, pd.DataFrame([new_exp])], ignore_index=True)
            expense_df.to_csv(EXPENSE_FILE, index=False)
            st.success(f"Logged R{spent_amount} for '{item_name}' under {who_spent}'s account!")
            st.rerun()

    st.markdown("---")
    st.markdown("### 📜 Running Purchases This Month")
    if expense_df.empty:
        st.caption("No custom shopping logged yet! Everything spent so far is clear.")
    else:
        st.dataframe(expense_df, use_container_width=True)
        if st.sidebar.button("🧹 Clear All Daily Purchases"):
            if os.path.exists(EXPENSE_FILE): os.remove(EXPENSE_FILE)
            st.rerun()

# -------------------------------------------------------------
# VIEW 3: MONTHLY HISTORY LOGS
# -------------------------------------------------------------
else:
    st.markdown("### 📊 Our Shared History Ledger")
    
    if history_df.empty:
        st.warning("No month entries logged yet! Head to the dashboard view to close out your first month.")
    else:
        total_joint_pool = history_df["Joint_Savings"].sum()
        total_macbook_pool = history_df["MacBook_Savings"].sum() + 10000
        
        tc1, tc2 = st.columns(2)
        with tc1: st.metric("Total Travel Cash Saved", f"R{total_joint_pool:,}")
        with tc2: st.metric("Kait's Laptop Fund", f"R{total_macbook_pool:,} / R22,000")
            
        if total_macbook_pool >= 22000:
            st.snow()
            st.success("💻 MacBook Air fully unlocked! iStore run time! 🎉")
            
        st.markdown("---")
        st.dataframe(history_df.set_index("Month"), use_container_width=True)
        
        if st.sidebar.button("⚠️ Reset All Records"):
            if os.path.exists(BUDGET_FILE): os.remove(BUDGET_FILE)
            st.rerun()
