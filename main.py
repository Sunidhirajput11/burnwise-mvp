import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Burnwise — Spend Intelligence",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@600;700;800&family=DM+Sans:wght@400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080f1e;
    color: #e2e8f0;
}
.stApp { background-color: #080f1e; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1200px; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── NAVBAR ── */
.bw-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 28px;
    border-bottom: 1px solid #1e2d4a;
    margin-bottom: 36px;
}
.bw-logo {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #e2e8f0;
}
.bw-logo span { color: #3b82f6; }
.bw-tagline {
    font-size: 12px;
    color: #475569;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.06em;
}
.bw-badge {
    background: rgba(59,130,246,.12);
    border: 1px solid rgba(59,130,246,.25);
    color: #93c5fd;
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    padding: 5px 14px;
    border-radius: 20px;
}

/* ── HERO ALERT BANNER ── */
.bw-alert {
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 15px;
    font-weight: 500;
}
.bw-alert.danger {
    background: #1c0f0f;
    border: 1px solid #7c2d2d;
    color: #fca5a5;
}
.bw-alert.success {
    background: #0a1f15;
    border: 1px solid #166534;
    color: #86efac;
}
.bw-alert-icon { font-size: 22px; }
.bw-alert-amt { font-family: 'DM Mono', monospace; font-weight: 500; }

/* ── KPI CARDS ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 28px;
}
.kpi-card {
    background: #0d1626;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.kpi-card.blue::before { background: #3b82f6; }
.kpi-card.red::before  { background: #f87171; }
.kpi-card.green::before{ background: #10b981; }
.kpi-card.amber::before{ background: #fbbf24; }
.kpi-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #475569;
    margin-bottom: 8px;
    font-weight: 500;
}
.kpi-value {
    font-family: 'DM Mono', monospace;
    font-size: 26px;
    font-weight: 500;
    color: #e2e8f0;
    line-height: 1;
}
.kpi-value.red   { color: #f87171; }
.kpi-value.green { color: #10b981; }
.kpi-value.amber { color: #fbbf24; }
.kpi-sub {
    font-size: 11px;
    color: #334155;
    margin-top: 6px;
    font-family: 'DM Mono', monospace;
}

/* ── SCORE RING ── */
.score-wrap {
    background: #0d1626;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 22px;
    text-align: center;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.score-title {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #475569;
    margin-bottom: 12px;
    font-weight: 500;
}

/* ── SECTION HEADERS ── */
.bw-section {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #e2e8f0;
    margin: 32px 0 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.bw-section::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e2d4a;
    margin-left: 10px;
}

/* ── INSIGHT CHIP ── */
.insight-chip {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: #1a2740;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 13px;
    color: #93c5fd;
    margin: 4px 4px 4px 0;
}

/* ── WASTE FLAG TAGS ── */
.flag {
    display: inline-block;
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 10px;
    font-family: 'DM Mono', monospace;
    font-weight: 500;
}
.flag-high   { background: #3b1515; color: #fca5a5; }
.flag-medium { background: #3b2a0a; color: #fcd34d; }
.flag-low    { background: #1a2535; color: #7dd3fc; }

/* ── UPLOAD ZONE ── */
.upload-zone {
    background: #0d1626;
    border: 1.5px dashed #1e3a5f;
    border-radius: 14px;
    padding: 48px 24px;
    text-align: center;
    margin: 16px 0 28px;
}
.upload-zone h3 {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
    color: #e2e8f0;
}
.upload-zone p {
    font-size: 13px;
    color: #475569;
    margin-bottom: 0;
}

/* ── DIVIDER ── */
.bw-divider {
    height: 1px;
    background: #1e2d4a;
    margin: 28px 0;
}

/* Plotly chart bg */
.js-plotly-plot .plotly { background: transparent !important; }

/* Streamlit overrides */
.stFileUploader > div {
    background: #0d1626 !important;
    border: 1.5px dashed #1e3a5f !important;
    border-radius: 12px !important;
}
.stFileUploader label { color: #94a3b8 !important; font-size: 13px !important; }
div[data-testid="metric-container"] { display: none; }
.stDataFrame { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ───────────────────────────────────────────────────────────────────
def fmt(val): return f"€{val:,.2f}"

def score_color(s):
    if s >= 75: return "#10b981"
    if s >= 50: return "#fbbf24"
    return "#f87171"

def score_label(s):
    if s >= 75: return "Healthy"
    if s >= 50: return "At Risk"
    return "Critical"

def make_donut(score):
    color = score_color(score)
    fig = go.Figure(go.Pie(
        values=[score, 100 - score],
        hole=0.72,
        marker_colors=[color, "#1e2d4a"],
        textinfo="none",
        hoverinfo="skip",
        showlegend=False,
    ))
    fig.add_annotation(
        text=f"<b>{score:.0f}</b>",
        font=dict(size=34, color=color, family="DM Mono"),
        showarrow=False, x=0.5, y=0.55
    )
    fig.add_annotation(
        text=score_label(score),
        font=dict(size=12, color="#64748b", family="DM Sans"),
        showarrow=False, x=0.5, y=0.35
    )
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=180,
    )
    return fig


# ─── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bw-nav">
    <div>
        <div class="bw-logo"><span>burn</span>wise</div>
        <div class="bw-tagline">SPEND INTELLIGENCE FOR STARTUPS</div>
    </div>
    <div class="bw-badge">🔴 Early Access</div>
</div>
""", unsafe_allow_html=True)


# ─── UPLOAD STATE ──────────────────────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = None

uploaded_file = st.file_uploader(
    "Drop your expense CSV here",
    type=["csv"],
    label_visibility="collapsed"
)

if uploaded_file:
    st.session_state.df = pd.read_csv(uploaded_file)

df = st.session_state.df

# ─── EMPTY STATE ───────────────────────────────────────────────────────────────
if df is None:
    st.markdown("""
    <div class="upload-zone">
        <h3>🔥 Find your hidden waste</h3>
        <p>Upload a CSV with your expense data — Burnwise will scan for waste, flag anomalies,<br>and show you exactly where your money is going.</p>
        <br>
        <p style="color:#1e3a5f;font-size:12px;font-family:'DM Mono',monospace;">
            EXPECTED COLUMNS: amount · category · description · date
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sample data button
    if st.button("▶  Load sample data", type="secondary"):
        st.session_state.df = pd.DataFrame({
            "date": ["2026-06-01","2026-06-02","2026-06-03","2026-06-04","2026-06-05",
                     "2026-06-06","2026-06-07","2026-06-08","2026-06-09","2026-06-10"],
            "description": ["Figma seats","AWS EC2","Zoom Pro","Salesforce CRM","Google Meet",
                            "Notion Team","Slack Pro","HubSpot","Datadog","Mixpanel"],
            "category": ["Design","Engineering","Communication","Sales","Communication",
                         "Productivity","Communication","Marketing","Engineering","Analytics"],
            "amount": [2100, 1870, 720, 1140, 480, 360, 240, 980, 1200, 430]
        })
        st.rerun()
    st.stop()


# ─── DATA PROCESSING ───────────────────────────────────────────────────────────
numeric_cols = df.select_dtypes(include='number').columns.tolist()

if len(numeric_cols) == 0:
    st.error("⚠️ No numeric columns found. Make sure your CSV has an amount/spend column.")
    st.stop()

amount_col = numeric_cols[0]
total_spend   = df[amount_col].sum()
avg_spend     = df[amount_col].mean()
max_spend     = df[amount_col].max()
waste_estimate = total_spend * 0.10
savings_found  = total_spend * 0.06
efficiency     = max(0, min(100, 100 - (waste_estimate / total_spend) * 100))


# ─── HERO ALERT ────────────────────────────────────────────────────────────────
if efficiency < 60:
    st.markdown(f"""
    <div class="bw-alert danger">
        <span class="bw-alert-icon">⚠️</span>
        <div>
            <strong>High spending inefficiency detected.</strong>
            Your estimated waste is <span class="bw-alert-amt">{fmt(waste_estimate)}/month</span> —
            that's {waste_estimate/total_spend*100:.0f}% of total burn going nowhere.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="bw-alert success">
        <span class="bw-alert-icon">✅</span>
        <div>
            <strong>Spending looks healthy.</strong>
            Estimated recoverable waste is <span class="bw-alert-amt">{fmt(waste_estimate)}/month</span>.
            Keep it up.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── KPI ROW + SCORE ───────────────────────────────────────────────────────────
col_kpis, col_score = st.columns([3, 1])

with col_kpis:
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="kpi-label">Total Spend</div>
            <div class="kpi-value">{fmt(total_spend)}</div>
            <div class="kpi-sub">this period</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-label">Estimated Waste</div>
            <div class="kpi-value red">{fmt(waste_estimate)}</div>
            <div class="kpi-sub">~10% of burn</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">Recoverable</div>
            <div class="kpi-value green">{fmt(savings_found)}</div>
            <div class="kpi-sub">quick wins available</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-label">Avg. Transaction</div>
            <div class="kpi-value amber">{fmt(avg_spend)}</div>
            <div class="kpi-sub">per line item</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_score:
    st.markdown('<div class="score-wrap"><div class="score-title">BurnWise Score</div>', unsafe_allow_html=True)
    st.plotly_chart(make_donut(efficiency), use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)


# ─── CHARTS ────────────────────────────────────────────────────────────────────
st.markdown('<div class="bw-section">📊 Spend Analysis</div>', unsafe_allow_html=True)

chart_l, chart_r = st.columns(2)

with chart_l:
    if "category" in df.columns:
        cat_data = df.groupby("category")[amount_col].sum().reset_index().sort_values(amount_col, ascending=True)
        fig = px.bar(
            cat_data, x=amount_col, y="category", orientation="h",
            color=amount_col,
            color_continuous_scale=[[0,"#1e3a5f"],[0.5,"#3b82f6"],[1,"#f87171"]],
            labels={amount_col: "Amount (€)", "category": ""},
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#64748b", family="DM Sans", size=12),
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
            height=280,
            xaxis=dict(gridcolor="#1e2d4a", tickfont=dict(color="#475569")),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(color="#94a3b8")),
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Add a 'category' column to see breakdown by department.")

with chart_r:
    if "category" in df.columns:
        pie_data = df.groupby("category")[amount_col].sum().reset_index()
        colors = ["#1d4ed8","#2563eb","#3b82f6","#60a5fa","#93c5fd","#bfdbfe","#1e3a5f","#172554","#f87171","#fbbf24"]
        fig2 = px.pie(
            pie_data, values=amount_col, names="category",
            hole=0.55,
            color_discrete_sequence=colors,
        )
        fig2.update_traces(textfont_size=11, textfont_color="#e2e8f0", textinfo="percent")
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#64748b", family="DM Sans"),
            legend=dict(font=dict(color="#64748b", size=11), bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=280,
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})


# ─── WASTE FLAGS ───────────────────────────────────────────────────────────────
st.markdown('<div class="bw-section">🚨 Waste Flags</div>', unsafe_allow_html=True)

top5 = df.nlargest(5, amount_col)
waste_html = ""
for _, row in top5.iterrows():
    amt = row[amount_col]
    pct = amt / total_spend * 100
    flag_cls = "flag-high" if pct > 20 else ("flag-medium" if pct > 10 else "flag-low")
    flag_lbl = "High" if pct > 20 else ("Medium" if pct > 10 else "Low")
    desc = row.get("description", row.get("category", f"Item"))
    cat  = row.get("category", "—")
    waste_html += f"""
    <div style="display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #111d33;">
        <div style="width:7px;height:7px;border-radius:50%;background:{'#f87171' if flag_lbl=='High' else '#fbbf24' if flag_lbl=='Medium' else '#60a5fa'};flex-shrink:0"></div>
        <div style="flex:1">
            <div style="font-size:13px;color:#cbd5e1;font-weight:500">{desc}</div>
            <div style="font-size:11px;color:#475569;font-family:'DM Mono',monospace">{cat}</div>
        </div>
        <div style="font-family:'DM Mono',monospace;font-size:14px;color:{'#f87171' if flag_lbl=='High' else '#fbbf24'}">€{amt:,.2f}</div>
        <span class="flag {flag_cls}">{flag_lbl} risk</span>
    </div>
    """

st.markdown(f'<div style="background:#0d1626;border:1px solid #1e2d4a;border-radius:12px;padding:4px 18px 4px">{waste_html}</div>', unsafe_allow_html=True)


# ─── KEY INSIGHTS ──────────────────────────────────────────────────────────────
st.markdown('<div class="bw-section">💡 Key Insights</div>', unsafe_allow_html=True)

insights = []
if "category" in df.columns:
    top_cat = df.groupby("category")[amount_col].sum().idxmax()
    top_cat_amt = df.groupby("category")[amount_col].sum().max()
    insights.append(f"🔥 <strong>{top_cat}</strong> is your highest spend category at {fmt(top_cat_amt)}")

insights.append(f"💸 Estimated <strong>{fmt(waste_estimate)}</strong> recoverable through seat audits & duplicate removal")
insights.append(f"📊 Your largest single expense is <strong>{fmt(max_spend)}</strong>")
insights.append(f"🎯 Cutting waste to &lt;3% would save <strong>{fmt(total_spend * 0.07)}/month</strong>")

chips_html = "".join([f'<div class="insight-chip">{i}</div>' for i in insights])
st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px">{chips_html}</div>', unsafe_allow_html=True)


# ─── RAW DATA ──────────────────────────────────────────────────────────────────
with st.expander("📂 View full expense data"):
    st.dataframe(
        df.sort_values(amount_col, ascending=False),
        use_container_width=True,
        hide_index=True
    )


# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:48px;padding-top:20px;border-top:1px solid #1e2d4a;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
    <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:800;color:#334155">
        <span style="color:#3b82f6">burn</span>wise
    </div>
    <div style="font-size:11px;color:#334155;font-family:'DM Mono',monospace">
        SPEND INTELLIGENCE FOR STARTUPS · EARLY ACCESS 2026
    </div>
</div>
""", unsafe_allow_html=True)
