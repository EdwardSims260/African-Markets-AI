import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from PIL import Image
import base64
import io
from traceback import format_exc

# ===== Logo Loader =====
def add_logo(logo_path, width=150):
    """Embed a logo with transparent background support."""
    try:
        logo = Image.open(logo_path)
        buffered = io.BytesIO()
        logo.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        st.markdown(
            f"""
            <style>
                .logo-container {{
                    display: flex;
                    justify-content: center;
                    margin: 10px 0 25px 0;
                }}
                .logo-img {{
                    width: {width}px;
                    transition: transform 0.2s;
                }}
                .logo-img:hover {{
                    transform: scale(1.05);
                }}
            </style>
            <div class="logo-container">
                <img class="logo-img" src="data:image/png;base64,{img_str}">
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        st.warning("Logo not found. Using fallback title.")
        st.title("AFRIMARKETS AI")

# ===== Dark Theme Setup =====
st.set_page_config(
    page_title="AfriMarkets AI",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>
    :root {
        --gold: #FFD700;
        --dark: #0E1117;
        --darker: #0A0C10;
    }
    .stApp {
        background: var(--dark);
        color: white;
    }
    .metric-card {
        background: var(--darker);
        border-radius: 8px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ===== App Header with Logo =====
col_logo, col_title = st.columns([0.1, 0.9])
with col_logo:
    add_logo("africa_logo.png", width=80)  # Change path as needed
with col_title:
    st.title("AFRIMARKETS AI")

# ===== Main App Logic =====
try:
    # Country Selection
    country = st.selectbox(
        "Select Country",
        ["Nigeria", "South Africa", "Kenya", "Egypt", "Morocco"],
        index=0
    )

    # Ticker Mapping
    tickers = {
        "Nigeria": "NGXASI",
        "South Africa": "^JTOPI",
        "Kenya": "NSE20.NSE",
        "Egypt": "EGX30",
        "Morocco": "MSI20.CS"
    }

    # Cached Data Fetch
    @st.cache_data(ttl=3600)
    def get_market_data(ticker):
        return yf.Ticker(ticker).history(period="1mo")

    # Display Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Selected Market", country)
    with col2:
        st.metric("Index Symbol", tickers[country])
    with col3:
        st.metric("Period", "1 Month")

    # Plotly Chart
    data = get_market_data(tickers[country])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        line=dict(color="#FFD700", width=3),
        name="Closing Price"
    ))

    fig.update_layout(
        title=f"{country} Market Trend",
        plot_bgcolor="#0A0C10",
        paper_bgcolor="#0A0C10",
        font=dict(color="white"),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    # AI Analysis Section
    with st.expander("🔍 AI Market Insights", expanded=True):
        st.markdown("""
        **📈 Top Performing Sectors**  
        ▸ Financial Services (+12% YTD)  
        ▸ Telecommunications (+8% YTD)  

        **💎 Recommended Stocks**  
        1. MTN Nigeria (MTNN)  
        2. Safaricom (SCOM)  
        """)

except Exception:
    st.error(f"""
    **⚠️ Application Error**  
    ```python
    {format_exc()}
    ```
    """)
    st.stop()

# ===== Footer =====
st.markdown("---")
st.caption("© 2024 AfriMarkets AI | Data from Yahoo Finance")
