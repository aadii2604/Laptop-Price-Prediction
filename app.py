import pandas as pd
import streamlit as st
from model_utils import train, CAT, NUM

# -------------------------------------------------------------------
# Page configuration
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Laptop Price Predictor | Studio",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------------
# Premium dark UI
# -------------------------------------------------------------------
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
    :root {
        --bg: #080d19;
        --panel: #101a2b;
        --panel-2: #131f33;
        --line: rgba(148, 163, 184, .16);
        --muted: #91a0b8;
        --text: #edf3ff;
        --blue: #54a5ff;
        --violet: #9b8cff;
        --cyan: #54dfd0;
    }
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 78% 0%, rgba(76, 110, 245, .16), transparent 34%),
            radial-gradient(ellipse at 8% 18%, rgba(39, 194, 210, .08), transparent 28%),
            var(--bg);
        color: var(--text);
    }
    [data-testid="stHeader"] { background: rgba(8,13,25,.72); }
    [data-testid="stToolbar"] { right: 1rem; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101a2b 0%, #0c1423 100%);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.4rem; }
    [data-testid="stSidebar"] * { color: #e8efff; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #b9c7dd; font-weight: 600; font-size: .86rem;
    }
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stNumberInput"] input {
        background: #17243a !important;
        border: 1px solid rgba(148,163,184,.22) !important;
        border-radius: 10px !important;
        color: #f4f7ff !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] { padding-top: .3rem; }
    [data-testid="stSlider"] [role="slider"] { background: #65a9ff; border-color: #65a9ff; }
    .block-container { padding-top: 2.1rem; padding-bottom: 3rem; max-width: 1500px; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: #f4f7ff !important; }
    h1 { letter-spacing: -.045em; }
    p, label, span { color: inherit; }
    [data-testid="stMarkdownContainer"] p { color: #aab8ce; }
    .hero {
        position: relative; overflow: hidden;
        padding: 1.65rem 1.8rem; margin-bottom: 1.35rem;
        border: 1px solid rgba(125,157,255,.24);
        border-radius: 22px;
        background: linear-gradient(115deg, rgba(25,43,73,.96), rgba(21,31,55,.84) 55%, rgba(40,42,87,.72));
        box-shadow: 0 18px 55px rgba(0,0,0,.22);
    }
    .hero:after {
        content: ""; position: absolute; width: 250px; height: 250px; right: -75px; top: -145px;
        border-radius: 50%; background: rgba(94,143,255,.18); filter: blur(5px);
    }
    .eyebrow {
        color: #83c8ff; text-transform: uppercase; letter-spacing: .16em;
        font-size: .72rem; font-weight: 700; margin-bottom: .55rem;
    }
    .hero-title { font: 700 clamp(1.8rem, 3vw, 2.65rem)/1.1 'Space Grotesk', sans-serif; color: #f7f9ff; }
    .hero-copy { color: #afbdd3; margin-top: .65rem; font-size: .98rem; }
    .hero-pill {
        display: inline-block; margin-top: 1.1rem; padding: .38rem .7rem;
        border-radius: 999px; color: #bce9ff; background: rgba(64,158,255,.13);
        border: 1px solid rgba(100,180,255,.24); font-size: .76rem; font-weight: 600;
    }
    .section-kicker {
        color: #91a7c8; text-transform: uppercase; letter-spacing: .13em;
        font-size: .72rem; font-weight: 700; margin: .25rem 0 .65rem;
    }
    .metric-card {
        background: linear-gradient(145deg, rgba(22,35,57,.98), rgba(15,25,42,.98));
        border: 1px solid var(--line); border-radius: 17px; padding: 1.05rem 1.15rem;
        min-height: 116px; box-shadow: 0 10px 30px rgba(0,0,0,.12);
    }
    .metric-label { color: #9babc2; font-size: .8rem; font-weight: 600; }
    .metric-value { color: #f4f7ff; font: 700 1.75rem 'Space Grotesk', sans-serif; margin-top: .35rem; }
    .metric-note { color: #68d9c5; font-size: .76rem; margin-top: .22rem; }
    .price-card {
        background: linear-gradient(130deg, rgba(37,78,145,.35), rgba(76,64,151,.27));
        border: 1px solid rgba(112,157,255,.35); border-radius: 20px;
        padding: 1.35rem 1.5rem; min-height: 180px;
        box-shadow: 0 15px 45px rgba(25,76,170,.12);
    }
    .price-label { color: #b7c8e6; font-size: .86rem; font-weight: 600; }
    .price-value {
        color: #ffffff; font: 700 clamp(2.1rem, 4vw, 3.15rem)/1.15 'Space Grotesk', sans-serif;
        letter-spacing: -.05em; margin: .45rem 0;
    }
    .price-foot { color: #a9c5f0; font-size: .8rem; }
    .side-brand { padding: .25rem .2rem 1.2rem; border-bottom: 1px solid var(--line); margin-bottom: 1.2rem; }
    .side-brand-name { font: 700 1.22rem 'Space Grotesk', sans-serif; color: #f5f8ff; }
    .side-brand-sub { color: #8ea2bf; font-size: .76rem; margin-top: .22rem; }
    .side-section { color: #78baff; text-transform: uppercase; letter-spacing: .13em; font-size: .7rem; font-weight: 700; margin: 1rem 0 .55rem; }
    .spec-chip {
        display: inline-block; padding: .42rem .62rem; margin: .2rem .18rem .2rem 0;
        border: 1px solid rgba(120,153,204,.2); border-radius: 9px;
        background: rgba(30,47,73,.72); color: #dce8fb; font-size: .78rem;
    }
    .stTabs [data-baseweb="tab-list"] { gap: .45rem; border-bottom: 1px solid var(--line); }
    .stTabs [data-baseweb="tab"] {
        background: transparent; color: #9eacc2; border-radius: 10px 10px 0 0;
        padding: .65rem 1rem; font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #d9eaff !important; background: rgba(68,130,225,.13) !important;
        border-bottom: 2px solid #65a9ff !important;
    }
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        border: 1px solid var(--line); border-radius: 12px; overflow: hidden;
    }
    .stButton button {
        border: 1px solid rgba(102,165,255,.45); border-radius: 10px;
        background: linear-gradient(100deg, #2563c9, #6657c9);
        color: white; font-weight: 700; padding: .55rem 1rem;
    }
    .stButton button:hover { border-color: #9cc9ff; color: white; filter: brightness(1.1); }
    .stDownloadButton button {
        border-radius: 10px; border: 1px solid rgba(148,163,184,.28);
        background: #17243a; color: #eaf2ff;
    }
    hr { border-color: var(--line); }
    footer { visibility: hidden; }
    @media (max-width: 800px) {
        .block-container { padding: 1rem .8rem 2rem; }
        .hero { padding: 1.2rem; }
        .price-card { min-height: 150px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------
# Load the existing training pipeline and dataset (unchanged ML logic)
# -------------------------------------------------------------------
@st.cache_resource
def load():
    return train()


try:
    model, metrics, df = load()
except Exception as exc:
    st.error(
        "The prediction model could not be loaded. Check that "
        "`data/laptops.csv` exists and that the project dependencies are installed."
    )
    st.exception(exc)
    st.stop()

cols = CAT + NUM

# -------------------------------------------------------------------
# Sidebar: laptop specifications
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="side-brand">
            <div style="font-size:1.8rem">⌘ 💻</div>
            <div class="side-brand-name">SPECIFY<span style="color:#69b5ff">.</span></div>
            <div class="side-brand-sub">Laptop intelligence studio</div>
        </div>
        <div class="side-section">Configure your laptop</div>
        """,
        unsafe_allow_html=True,
    )

    ram = st.select_slider("Memory · RAM", [4, 8, 16, 32, 64], value=8, format_func=lambda x: f"{x} GB")
    storage = st.select_slider(
        "Storage capacity", [128, 256, 512, 1024, 2048], value=512,
        format_func=lambda x: f"{x // 1024} TB" if x >= 1024 else f"{x} GB",
    )
    stype = st.selectbox("Storage technology", sorted(df.Storage_Type.dropna().unique()))
    cpu_options = sorted(df.Processor.dropna().unique())
    cpu_default = cpu_options.index("Core i5 / Ryzen 5") if "Core i5 / Ryzen 5" in cpu_options else min(1, len(cpu_options) - 1)
    cpu = st.selectbox("Processor", cpu_options, index=cpu_default)
    gpu_options = ["Integrated", "GTX 1650", "RTX 3050", "RTX 4060", "RTX 4070"]
    gpu = st.selectbox("Graphics", gpu_options, index=0)
    screen = st.select_slider("Display size", [13.3, 14.0, 15.6, 16.0, 17.3], value=15.6, format_func=lambda x: f'{x:.1f}"')
    res_options = sorted(df.Resolution.dropna().unique())
    res = st.selectbox("Screen resolution", res_options)
    brand = st.selectbox("Brand segment", ["Budget", "Mainstream", "Premium"], index=1)

    st.markdown("---")
    st.markdown('<div class="side-section">Reference controls</div>', unsafe_allow_html=True)
    set_reference = st.button("Set current price as reference", use_container_width=True)
    st.caption("Adjust any specification to update the estimated price instantly.")

spec = {
    "Brand": brand,
    "Storage_Type": stype,
    "Processor": cpu,
    "GPU": gpu,
    "Resolution": res,
    "Ram_GB": ram,
    "Storage_GB": storage,
    "Screen_Size": screen,
}


def predict(**overrides):
    row = {**spec, **overrides}
    return float(model.predict(pd.DataFrame([row])[cols])[0])


price = predict()

if "reference_price" not in st.session_state:
    st.session_state.reference_price = price
if set_reference:
    st.session_state.reference_price = price

delta = price - st.session_state.reference_price
delta_text = f"{delta:+,.0f} vs your reference"
best_model = metrics.sort_values("R2", ascending=False).iloc[0]["Model"]

# -------------------------------------------------------------------
# Main dashboard
# -------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Laptop intelligence · Price estimation</div>
        <div class="hero-title">Find the right laptop.<br>Know what it's worth.</div>
        <div class="hero-copy">Explore how hardware choices influence estimated laptop pricing, powered by your trained machine-learning models.</div>
        <div class="hero-pill">✦ &nbsp; LIVE PREDICTION WORKSPACE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-kicker">Your estimate</div>', unsafe_allow_html=True)
left, right = st.columns([1.08, 1.92], gap="large")

with left:
    sign = "+" if delta >= 0 else ""
    st.markdown(
        f"""
        <div class="price-card">
            <div class="price-label">Estimated laptop price</div>
            <div class="price-value">₹{price:,.0f}</div>
            <div class="price-foot">INR · Model-generated estimate</div>
            <div style="margin-top:1rem;color:#83e0d0;font-size:.82rem;font-weight:600">
                {sign}{delta:,.0f} <span style="color:#a9c5f0;font-weight:400">compared with reference</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Selected prediction model</div>
            <div class="metric-value" style="font-size:1.35rem">{best_model}</div>
            <div class="metric-note">Best R² score among evaluated models</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    k1, k2, k3 = st.columns(3)
    best_row = metrics.sort_values("R2", ascending=False).iloc[0]
    with k1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Model R² score</div><div class="metric-value">{best_row["R2"]:.4f}</div><div class="metric-note">Higher is better</div></div>',
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Mean absolute error</div><div class="metric-value">₹{best_row["MAE"]:,.0f}</div><div class="metric-note">Validation-set average</div></div>',
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Training records</div><div class="metric-value">{len(df):,}</div><div class="metric-note">Rows in laptop dataset</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown('<div class="section-kicker">Selected configuration</div>', unsafe_allow_html=True)
    specs = [
        ("RAM", f"{ram} GB"), ("Storage", f"{storage} GB"), ("Drive", stype),
        ("Processor", cpu), ("Graphics", gpu), ("Display", f'{screen:.1f}" · {res}'),
        ("Brand tier", brand),
    ]
    chips = "".join(f'<span class="spec-chip"><b>{name}</b> &nbsp;{value}</span>' for name, value in specs)
    st.markdown(f'<div style="padding:.35rem 0">{chips}</div>', unsafe_allow_html=True)

st.write("")
st.markdown('<div class="section-kicker">Explore price sensitivity</div>', unsafe_allow_html=True)
tab_ram, tab_storage, tab_models = st.tabs(["◈  RAM impact", "▤  Storage impact", "◎  Model performance"])

with tab_ram:
    ram_values = [4, 8, 16, 32, 64]
    ram_series = pd.Series(
        {f"{value} GB": predict(Ram_GB=value) for value in ram_values},
        name="Estimated price (₹)",
    )
    st.markdown("**How memory configuration changes the estimate**")
    st.caption("All other selected specifications are held constant.")
    st.bar_chart(ram_series, use_container_width=True, color="#579dff")
    st.dataframe(
        pd.DataFrame({"RAM": [f"{v} GB" for v in ram_values], "Estimated price (₹)": [round(float(ram_series[f"{v} GB"])) for v in ram_values]}),
        hide_index=True,
        use_container_width=True,
    )

with tab_storage:
    storage_values = [128, 256, 512, 1024, 2048]
    storage_labels = [f"{v // 1024} TB" if v >= 1024 else f"{v} GB" for v in storage_values]
    storage_prices = [predict(Storage_GB=v) for v in storage_values]
    storage_series = pd.Series(dict(zip(storage_labels, storage_prices)), name="Estimated price (₹)")
    st.markdown("**How storage capacity changes the estimate**")
    st.caption("All other selected specifications are held constant.")
    st.bar_chart(storage_series, use_container_width=True, color="#9b8cff")
    st.dataframe(
        pd.DataFrame({"Storage": storage_labels, "Estimated price (₹)": [round(v) for v in storage_prices]}),
        hide_index=True,
        use_container_width=True,
    )

with tab_models:
    st.markdown("**Validation performance comparison**")
    st.caption("Metrics are calculated by the existing training pipeline using its held-out test split.")
    display_metrics = metrics.copy()
    display_metrics["MAE"] = display_metrics["MAE"].map(lambda x: f"₹{x:,.0f}")
    display_metrics["R2"] = display_metrics["R2"].map(lambda x: f"{x:.4f}")
    st.dataframe(display_metrics, hide_index=True, use_container_width=True)
    st.markdown("**R² score by model**")
    st.bar_chart(metrics.set_index("Model")[["R2"]], use_container_width=True, color="#54dfd0")

st.write("")
with st.expander("▤  Explore sample training data"):
    st.caption("Preview of the first 50 records from the dataset used by the training pipeline.")
    st.dataframe(df.head(50), hide_index=True, use_container_width=True)

prediction_record = pd.DataFrame([{
    **spec,
    "Predicted_Price_INR": round(price, 2),
    "Prediction_Model": best_model,
}])
st.download_button(
    "↓  Download this estimate (CSV)",
    data=prediction_record.to_csv(index=False).encode("utf-8"),
    file_name="laptop_price_estimate.csv",
    mime="text/csv",
)

st.markdown(
    """
    <div style="margin-top:2.2rem;padding-top:1rem;border-top:1px solid rgba(148,163,184,.14);color:#72839d;font-size:.75rem">
        SPECIFY. &nbsp;·&nbsp; Laptop Price Predictor &nbsp;·&nbsp; Estimates are model outputs, not market quotations.
    </div>
    """,
    unsafe_allow_html=True,
)
