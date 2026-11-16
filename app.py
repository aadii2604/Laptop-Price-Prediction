import pandas as pd
import streamlit as st
from model_utils import train, CAT, NUM

st.set_page_config(page_title="Laptop Price Predictor", page_icon="💻", layout="wide")


@st.cache_resource
def load():
    return train()


model, metrics, df = load()
cols = CAT + NUM

st.title("💻 Laptop Price Predictor")
st.caption("Change RAM or storage in the sidebar and watch the predicted price update.")

# ---- sidebar inputs ----
sb = st.sidebar
sb.header("Specifications")
ram = sb.select_slider("RAM (GB)", [4, 8, 16, 32, 64], value=8)
storage = sb.select_slider("Storage (GB)", [128, 256, 512, 1024, 2048], value=512)
stype = sb.selectbox("Storage type", sorted(df.Storage_Type.unique()))
cpu = sb.selectbox("Processor", sorted(df.Processor.unique()), index=1)
gpu = sb.selectbox("Graphics", ["Integrated", "GTX 1650", "RTX 3050", "RTX 4060", "RTX 4070"])
screen = sb.select_slider("Screen size (inch)", [13.3, 14.0, 15.6, 16.0, 17.3], value=15.6)
res = sb.selectbox("Display", sorted(df.Resolution.unique()))
brand = sb.selectbox("Brand segment", ["Budget", "Mainstream", "Premium"], index=1)

spec = {"Brand": brand, "Storage_Type": stype, "Processor": cpu, "GPU": gpu, "Resolution": res,
        "Ram_GB": ram, "Storage_GB": storage, "Screen_Size": screen}


def predict(**over):
    row = {**spec, **over}
    return float(model.predict(pd.DataFrame([row])[cols])[0])


price = predict()

# ---- reference for the "change" indicator ----
if "ref" not in st.session_state:
    st.session_state.ref = price
if sb.button("Set current as reference"):
    st.session_state.ref = price
delta = price - st.session_state.ref

c1, c2 = st.columns([1, 2])
with c1:
    st.metric("Predicted price", f"₹{price:,.0f}", f"{delta:+,.0f} vs reference")
    st.write(f"**Model used:** {metrics.sort_values('R2').iloc[-1]['Model']}")
    st.dataframe(metrics, hide_index=True)
with c2:
    t1, t2 = st.tabs(["Price vs RAM", "Price vs Storage"])
    with t1:
        s = pd.Series({f"{r} GB": predict(Ram_GB=r) for r in [4, 8, 16, 32, 64]}, name="Price")
        st.bar_chart(s)
    with t2:
        s = pd.Series({(f"{g//1024} TB" if g >= 1024 else f"{g} GB"): predict(Storage_GB=g)
                       for g in [128, 256, 512, 1024, 2048]}, name="Price")
        st.bar_chart(s)

with st.expander("View training data"):
    st.dataframe(df.head(50))
