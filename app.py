import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# PIPELINE CONFIGURATION: CACHED SYSTEM INGESTION FRAMEWORK
# ==============================================================================
@st.cache_data
def load_production_dataframe():
    """Reads the verified data freeze CSV matrix from local directory storage."""
    file_path = "data/master_customer_churn.csv"
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"[CRITICAL FILE FAULT] Unable to ingest dataset file at path: '{file_path}'")
        st.stop()

# Initialize data framework loading block
master_df = load_production_dataframe()

# ==============================================================================
# BASELINE FRONT-END TEXT BANNERS LAYOUT
# ==============================================================================
st.title("📊 Master Corporate Telecom Attrition Audit Dashboard")
st.markdown("---")

st.success(
    f"**[STAGE 5.1 SUCCESS]** Data Pipeline Verified. "
    f"Successfully ingested a stable footprint tracking **{len(master_df):,} total customer profiles** "
    f"containing **{len(master_df.columns)} feature attributes** directly from local drive memory."
)

# ==============================================================================
# STAGE 5.2: METRICS RUN-RATE COMPUTATION ENGINE (LIVE SUBSETS ONLY)
# ==============================================================================
# Clean data type alignments and handle potential empty entries safely
master_df['Monthly Charges'] = pd.to_numeric(master_df['Monthly Charges'], errors='coerce').fillna(0.0)
master_df['Satisfaction Score'] = pd.to_numeric(master_df['Satisfaction Score'], errors='coerce').fillna(3.0)
master_df['Customer Status'] = master_df['Customer Status'].astype(str).str.strip()

# Isolate the live active customer base (exclusively 'Stayed' and 'Joined')
active_mask_app = master_df['Customer Status'].isin(['Stayed', 'Joined'])
active_df_app = master_df[active_mask_app].copy()

# Dynamic Matrix Matrix Assembly (Calculates 4-Quadrant tags in real-time memory)
active_charges_median = active_df_app['Monthly Charges'].median()

quadrant_conditions = [
    (active_df_app['Satisfaction Score'] == 3) & (active_df_app['Monthly Charges'] > active_charges_median),
    (active_df_app['Satisfaction Score'] == 3) & (active_df_app['Monthly Charges'] <= active_charges_median),
    (active_df_app['Satisfaction Score'] >= 4) & (active_df_app['Monthly Charges'] > active_charges_median),
    (active_df_app['Satisfaction Score'] >= 4) & (active_df_app['Monthly Charges'] <= active_charges_median)
]

quadrant_labels = [
    'Quadrant I: High Risk / High Value (Critical Action Target)',
    'Quadrant II: High Risk / Low Value (Cost-Managed Flight)',
    'Quadrant III: Low Risk / High Value (VIP Anchor Base)',
    'Quadrant IV: Low Risk / Low Value (Standard Maintenance)'
]

active_df_app['Risk_Matrix_Quadrant'] = np.select(quadrant_conditions, quadrant_labels, default='Unknown Base')

# Calculate the global business health indicators for overview panels
total_active_count = len(active_df_app)
total_monthly_revenue = active_df_app['Monthly Charges'].sum()

# Calculate baseline front-line revenue exposure (Satisfaction Score == 3)
at_risk_mask_app = active_df_app['Satisfaction Score'] == 3
at_risk_revenue = active_df_app[at_risk_mask_app]['Monthly Charges'].sum()

st.write("### 📌 Active Portfolio Performance Overview")

# Initialize a clean horizontal grid layout inside Streamlit
kpi_column_1, kpi_column_2, kpi_column_3 = st.columns(3)

with kpi_column_1:
    st.metric(label="Active Customer Base", value=f"{total_active_count:,} accounts")
with kpi_column_2:
    st.metric(label="Monthly Revenue Run-Rate", value=f"${total_monthly_revenue:,.2f}")
with kpi_column_3:
    st.metric(label="At-Risk Monthly Revenue", value=f"${at_risk_revenue:,.2f}", delta=f"-${at_risk_revenue:,.2f}", delta_color="inverse")

st.markdown("---")

# ==============================================================================
# STAGE 5.3: INTERACTIVE SIDEBAR CONTROL PANEL SELECTION ENGINE
# ==============================================================================
st.sidebar.header("⚙️ Operational Control Panel")
st.sidebar.markdown("Use the dropdown below to dynamically filter your active portfolio base.")

dropdown_options_list = [
    "All Active Subscribers (Complete Base View)",
    "Quadrant I: High Risk / High Value (Critical Action Target)",
    "Quadrant II: High Risk / Low Value (Cost-Managed Flight)",
    "Quadrant III: Low Risk / High Value (VIP Anchor Base)",
    "Quadrant IV: Low Risk / Low Value (Standard Maintenance)"
]

selected_cohort = st.sidebar.selectbox(label="Select Portfolio Risk Segment Group:", options=dropdown_options_list)

# Process interactive data subset filters smoothly in memory
filtered_data_view = active_df_app.copy()

if selected_cohort != "All Active Subscribers (Complete Base View)":
    filtered_data_view = active_df_app[active_df_app['Risk_Matrix_Quadrant'] == selected_cohort]

# ==============================================================================
# DYNAMIC MAIN CONTENT VIEWPORT MAPPER FOR SEGMENTS
# ==============================================================================
st.write(f"### 🔍 Dynamic Segment Profile: {selected_cohort}")

current_segment_count = len(filtered_data_view)
current_segment_revenue = filtered_data_view['Monthly Charges'].sum()
current_segment_percentage = (current_segment_count / total_active_count) * 100 if total_active_count > 0 else 0.0

col_metric_1, col_metric_2 = st.columns(2)
with col_metric_1:
    st.metric("Segment Subscriber Volume", f"{current_segment_count:,} accounts", f"{current_segment_percentage:.2f}% of active base")
with col_metric_2:
    st.metric("Segment Monthly Revenue Contribution", f"${current_segment_revenue:,.2f}")

# 5. Display a raw datatable preview box so the user can audit individual row details
st.markdown("#### 📋 Filtered Records Registry Preview")

# Defensive list optimization matching the exact string arrays in your CSV data keys
target_columns_list = []
for possible_col in ['CustomerID', 'Customer ID', 'Gender', 'Contract', 'Payment Method', 'Monthly Charges', 'Satisfaction Score']:
    if possible_col in filtered_data_view.columns:
        target_columns_list.append(possible_col)

st.dataframe(
    filtered_data_view[target_columns_list].head(100),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==============================================================================
# STAGE 5.4: DYNAMIC EXECUTIVES STRATEGIC RECOMMENDATIONS ENGINE
# ==============================================================================
st.write("### 💡 Tactical Business Recovery Plan")

rec_text = ""
icon_style = "info"  # Establishes default formatting container state

if "Quadrant I:" in selected_cohort:
    icon_style = "error" # Red color alert container for high-priority items
    rec_text = """
    * **The Strategic Insight:** This segment isolates premium-tier active users sitting directly on the frontline satisfaction cliff. This group represents our highest urgent revenue-at-risk exposure.
    * **The Actionable Fix (The Proactive Senior Save Campaign):** Since our statistical tests proved Senior Citizens face high price premiums ($17.97/month) and long-term contracts act as strong revenue anchors, we must intervene immediately. Proactively offer this cohort a discounted, value-packed **1-Year or 2-Year Contract VIP Bundle** that includes highly valued add-on features like **Online Security** and **Tech Support**. This addresses billing anxiety while securing long-term loyalty before they hit a satisfaction cliff.
    """
elif "Quadrant II:" in selected_cohort:
    icon_style = "warning" # Orange color alert container for cost-managed targets
    rec_text = """
    * **The Strategic Insight:** Lower-tier revenue contributors displaying critical satisfaction friction markers.
    * **The Actionable Fix (Automated Accounts Migrations):** These accounts present high attrition counts but a lower financial footprint. Route these users into **Automated Service Recovery Channels**. Deploy automated email surveys offering tailored, low-overhead digital plan optimizations to improve baseline sentiment without increasing high-touch customer support operational costs.
    """
elif "Quadrant III:" in selected_cohort:
    icon_style = "success" # Green color alert container for highly stable VIP tiers
    rec_text = """
    * **The Strategic Insight:** These are your most valuable, stable accounts paying premium rates with optimal life-cycle satisfaction. They form the financial anchor of the active portfolio.
    * **The Actionable Fix (Loyalty Stabilization):** Protect this premium core from competitor poaching. Implement a **VIP Surprise & Delight Loyalty Protocol**, providing proactive network speed upgrades or early access to device updates with zero price adjustments to maintain their strong brand affinity.
    """
elif "Quadrant IV:" in selected_cohort:
    icon_style = "success"
    rec_text = """
    * **The Strategic Insight:** Highly stable lower-tier accounts displaying positive lifecycle satisfaction.
    * **The Actionable Fix (Organic Growth):** This group requires minimal immediate risk intervention. Maintain standard automated check-ins and run gentle, periodic cross-selling campaigns to introduce digital add-on values over time as their account tenure matures.
    """
else:
    icon_style = "info" # Blue color container for general base views
    rec_text = """
    * **Overview Strategy:** The overall active subscriber portfolio is stable, but underlying revenue pockets are exposed to significant retention friction.
    * **Action Item:** Use the left-hand **Operational Control Panel** to slice the database by specific risk quadrants. Focus your analysis immediately on **Quadrant I** to review our highest-exposure cash flow liabilities.
    """

# Render the custom recommendation block inside the dynamically updating banner
if icon_style == "error":
    st.error(rec_text)
elif icon_style == "warning":
    st.warning(rec_text)
elif icon_style == "success":
    st.success(rec_text)
else:
    st.info(rec_text)

st.markdown("---")
