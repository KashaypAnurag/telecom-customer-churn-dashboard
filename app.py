import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. PIPELINE CONFIGURATION: CACHED SYSTEM INGESTION FRAMEWORK
# ==============================================================================
@st.cache_data
def load_production_dataframe():
    """Reads the verified data freeze CSV matrix from local directory storage."""
    file_path = "data/master_customer_churn.csv"
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Critical Ingestion Failure: Unable to locate source data matrix at '{file_path}'")
        st.stop()

# Initialize data framework loading block
master_df = load_production_dataframe()

# Standardize data types, remove trailing white spaces, and handle null vectors defensively
master_df['Monthly Charges'] = pd.to_numeric(master_df['Monthly Charges'], errors='coerce').fillna(0.0)
master_df['Satisfaction Score'] = pd.to_numeric(master_df['Satisfaction Score'], errors='coerce').fillna(3.0)
master_df['Customer Status'] = master_df['Customer Status'].astype(str).str.strip()

# Isolate active subscriber footprint base (strips out historical churn noise)
active_mask_app = master_df['Customer Status'].isin(['Stayed', 'Joined'])
active_df_app = master_df[active_mask_app].copy()

# Programmatically reconstruct the 4-Quadrant Risk Matrix inside memory
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

# ==============================================================================
# 2. INTERACTIVE SIDEBAR CONTROL PANEL SELECTION ENGINE
# ==============================================================================
st.sidebar.markdown("## Operational Control Panel")
st.sidebar.markdown("Use the dropdown below to dynamically filter your active portfolio base records.")

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
# 3. BASELINE FRONT-END EXECUTIVE TOP BANNER LAYOUT
# ==============================================================================
st.title("Master Corporate Telecom Attrition Audit Dashboard")
st.caption("Data Pipeline Verification Status: Active. Ingesting footprint tracking 7,043 customer profiles containing 45 feature attributes from local drive memory.")
st.markdown("---")

# ==============================================================================
# 4. GLOBAL ACTIVE PORTFOLIO OVERVIEW PANEL (ANTI-TRUNCATION ARCHITECTURE)
# ==============================================================================
st.markdown("### Active Portfolio Performance Overview")

total_active_count = len(active_df_app)
total_monthly_revenue = active_df_app['Monthly Charges'].sum()

# Compute total frontline exposure cash (Satisfaction Score == 3)
at_risk_mask_app = active_df_app['Satisfaction Score'] == 3
at_risk_revenue = active_df_app[at_risk_mask_app]['Monthly Charges'].sum()

# Two-row matrix metrics container prevents narrow text column clipping
with st.container(border=True):
    col_top1, col_top2 = st.columns(2)
    with col_top1:
        st.metric(label="Active Customer Base Total", value=f"{total_active_count:,} accounts")
    with col_top2:
        st.metric(label="Monthly Revenue Run-Rate", value=f"${total_monthly_revenue:,.2f}")
        
    st.markdown("---")
    st.metric(label="At-Risk Frontline Monthly Revenue Exposure", value=f"${at_risk_revenue:,.2f}", delta=f"-${at_risk_revenue:,.2f}", delta_color="inverse")

st.markdown("---")

# ==============================================================================
# 5. DYNAMIC TARGET COHORT PROFILE PERFORMANCE LAYER
# ==============================================================================
st.markdown("### Dynamic Segment Profile Dashboard")
st.caption(f"Active Selection View: {selected_cohort}")

current_segment_count = len(filtered_data_view)
current_segment_revenue = filtered_data_view['Monthly Charges'].sum()
current_segment_percentage = (current_segment_count / total_active_count) * 100 if total_active_count > 0 else 0.0

# Wrap dynamic cohort metrics inside native card boxes
with st.container(border=True):
    col_metric_1, col_metric_2 = st.columns(2)
    with col_metric_1:
        st.metric(label="Segment Subscriber Account Volume", value=f"{current_segment_count:,} profiles", delta=f"{current_segment_percentage:.2f}% of active base")
    with col_metric_2:
        st.metric(label="Segment Monthly Revenue Contribution", value=f"${current_segment_revenue:,.2f}")

st.markdown("---")

# ==============================================================================
# 6. DYNAMIC PRODUCT BUNDLE ATTACHMENT ANALYTICS ENGINE (NATIVE CHARTS RESTORED)
# ==============================================================================
st.markdown("### Ecosystem Product Cross-Sell Attachment Matrix")
st.caption("Monitors percentage activation rates of digital add-on services across the currently selected customer cohort to isolate cross-selling drop-offs.")

if len(filtered_data_view) > 0:
    core_services_list = ['Online Security', 'Online Backup', 'Device Protection', 'Tech Support', 'Streaming TV', 'Streaming Movies']
    service_percentages = {}
    
    for service_name in core_services_list:
        if service_name in filtered_data_view.columns:
            clean_series = filtered_data_view[service_name].astype(str).str.strip().str.capitalize()
            yes_count = (clean_series == 'Yes').sum()
            percentage_share = (yes_count / len(filtered_data_view)) * 100
            service_percentages[service_name] = round(percentage_share, 2)
        else:
            service_percentages[service_name] = 0.0
            
    chart_source_df = pd.DataFrame(list(service_percentages.items()), columns=['Digital Ecosystem Product', 'Activation Rate (%)']).set_index('Digital Ecosystem Product')
    
    # Restores fast native horizontal charting framework
    st.bar_chart(chart_source_df, horizontal=True, use_container_width=True)
else:
    st.warning("Zero records available inside the selected filter parameters to map product attributes.")

st.markdown("---")

# ==============================================================================
# SECTION 2: DYNAMIC CONTRACT TYPE REVENUE DISTRIBUTION HUB (NATIVE RESTORED)
# ==============================================================================
st.markdown("### Contract Billing Revenue Distribution Analysis")
st.caption("Maps the monthly gross revenue contribution across contract terms for the selected cohort, anchoring our parametric ANCOVA findings.")

if len(filtered_data_view) > 0 and 'Contract' in filtered_data_view.columns:
    # Compute the total gross revenue distribution grouped directly by contract terms
    contract_revenue_df = filtered_data_view.groupby('Contract')['Monthly Charges'].sum().reset_index()
    contract_revenue_df = contract_revenue_df.set_index('Contract')
    
    # Render a clean, native vertical bar chart asset
    st.bar_chart(contract_revenue_df, use_container_width=True)
else:
    st.warning("Contract structural features unavailable for visualization mapping.")

st.markdown("---")

# ==============================================================================
# 7. FILTERED RECORDS REGISTRY RECORD DETAIL GRID & SECTION 3 EXPORTER WIDGET
# ==============================================================================
st.markdown("### Filtered Records Registry Preview")

target_columns_list = []
for possible_col in ['CustomerID', 'Gender', 'Contract', 'Payment Method', 'Monthly Charges', 'Satisfaction Score']:
    if possible_col in filtered_data_view.columns:
        target_columns_list.append(possible_col)

st.dataframe(filtered_data_view[target_columns_list].head(100), use_container_width=True, hide_index=True)

# SECTION 3 EXPORTER ENGINE: Generates a real-time CSV data file extraction package download trigger button
csv_data_string = filtered_data_view.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Export Filtered Cohort List to CSV File",
    data=csv_data_string,
    file_name=f"filtered_retention_list.csv",
    mime="text/csv",
    help="Downloads the currently filtered workspace customer list directly to your computer as a clean Excel CSV spreadsheet file."
)

st.markdown("---")

# ==============================================================================
# 8. TACTICAL BUSINESS RECOVERY PLAN (DETERMINISTIC MAPPING PIPELINE)
# ==============================================================================
st.markdown("### Tactical Business Recovery Plan")

# Initialize an error-proof tracking ledger dictionary using explicit string indexing
recovery_plan_dictionary = {
    "All Active Subscribers (Complete Base View)": 
    "**Overview Strategy**\n\nThe overall active subscriber portfolio is stable, but underlying revenue pockets are exposed to significant retention friction.\n\n**Action Item**\n\nUse the left-hand Operational Control Panel to slice the database by specific risk quadrants. Focus your analysis immediately on Quadrant I to review our highest-exposure cash flow liabilities.",
    
    "Quadrant I: High Risk / High Value (Critical Action Target)": 
    "**Strategic Insight**\n\nThis segment isolates premium-tier active users sitting directly on the frontline satisfaction cliff. This group represents our highest urgent revenue-at-risk exposure.\n\n**Actionable Fix (The Proactive Senior Save Campaign)**\n\nSince our statistical tests proved Senior Citizens face high price premiums ($17.97/month) and long-term contracts act as strong revenue anchors, we must intervene immediately. Proactively offer this cohort a discounted, value-packed 1-Year or 2-Year Contract VIP Bundle that includes highly valued add-on features like Online Security and Tech Support. This addresses billing anxiety while securing long-term loyalty before they hit a satisfaction cliff.",
    
    "Quadrant II: High Risk / Low Value (Cost-Managed Flight)": 
    "**Strategic Insight**\n\nLower-tier revenue contributors displaying critical satisfaction friction markers.\n\n**Actionable Fix (Automated Accounts Migrations)**\n\nThese accounts present high attrition counts but a lower financial footprint. Route these users into Automated Service Recovery Channels. Deploy automated email surveys offering tailored, low-overhead digital plan optimizations to improve baseline sentiment without increasing high-touch customer support operational costs.",
    
    "Quadrant III: Low Risk / High Value (VIP Anchor Base)": 
    "**Strategic Insight**\n\nThese are your most valuable, stable accounts paying premium rates with optimal life-cycle satisfaction. They form the financial anchor of the active portfolio.\n\n**Actionable Fix (Loyalty Stabilization)**\n\nProtect this premium core from competitor poaching. Implement a VIP Surprise & Delight Loyalty Protocol, providing proactive network speed upgrades or early access to device updates with zero price adjustments to maintain their strong brand affinity.",
    
    "Quadrant IV: Low Risk / Low Value (Standard Maintenance)": 
    "**Strategic Insight**\n\nHighly stable lower-tier accounts displaying positive lifecycle satisfaction.\n\n**Actionable Fix (Organic Growth)**\n\nThis group requires minimal immediate risk intervention. Maintain standard automated check-ins and run gentle, periodic cross-selling campaigns to introduce digital add-on values over time as their account tenure matures."
}

# Deterministically load the target text string based on the user's active dropdown index key
final_brief_output = recovery_plan_dictionary.get(selected_cohort, recovery_plan_dictionary["All Active Subscribers (Complete Base View)"])

# Render the plain markdown brief inside a uniform gray bordered block container
with st.container(border=True):
    st.markdown(final_brief_output)

st.markdown("---")
