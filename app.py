import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from PIL import Image
import base64
from traceback import format_exc

# ===== Africa Logo (Gold SVG) =====
AFRICA_LOGO = """
<svg viewBox="0 0 100 100" width="50" xmlns="http://www.w3.org/2000/svg">
  <path fill="#FFD700" d="M50,10 L60,30 L70,25 L75,40 L85,35 L80,50 L90,60 L75,70 L65,65 L55,75 L45,65 L35,75 L25,65 L15,70 L5,50 L15,30 Z"/>
</svg>
"""

# ===== Dark Theme Setup =====
st.set_page_config(
    page_title="AfriMarkets AI",
    page_icon="🌍",
    layout="wide"
)

st.markdown(f"""
<style>
    :root {{
        --gold: #FFD700;
        --dark: #0E1117;
        --darker: #0A0C10;
    }}
    .stApp {{
        background: var(--dark);
        color: white;
    }}
    h1, h2, h3 {{ color: var(--gold) !important; }}
    .stSelectbox, .stSlider label {{ color: white !important; }}
    .stButton>button {{
        background: var(--darker);
        color: var(--gold);
        border: 1px solid var(--gold);
        border-radius: 5px;
    }}
    .stButton>button:hover {{
        background: var(--gold) !important;
        color: var(--dark) !important;
    }}
    .market-card {{
        background: var(--darker);
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid var(--gold);
    }}
    .stMetric {{
        border-bottom: 2px solid var(--gold);
    }}
</style>
""", unsafe_allow_html=True)

# ===== App Header with Logo =====
col_logo, col_title = st.columns([0.1, 0.9])
with col_logo:
    st.markdown(AFRICA_LOGO, unsafe_allow_html=True)
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
        "Kenya": "NSE20",
        "Egypt": "EGX30",
        "Morocco": "MSI20"
    }

    # Cached Data Fetch
    @st.cache_data(ttl=3600)  # Cache for 1 hour
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
    with st.container():
        st.markdown('<div class="market-card">', unsafe_allow_html=True)
        st.write(f"### 📈 {country} Market Performance")
        
        data = get_market_data(tickers[country])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            line=dict(color="#FFD700", width=3),
            name="Closing Price"
        ))
        
        fig.update_layout(
            plot_bgcolor="#0A0C10",
            paper_bgcolor="#0A0C10",
            font=dict(color="white"),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # AI Analysis Section
    with st.expander("🔍 AI Market Insights", expanded=True):
        st.write("""
        **📈 Top Performing Sectors**  
        ▸ Financial Services (+12% YTD)  
        ▸ Telecommunications (+8% YTD)  
        
        **💎 Recommended Stocks**  
        1. MTN Nigeria (MTNN)  
        2. Safaricom (SCOM)  
        """)

except Exception as e:
    st.error(f"""
    **⚠️ Application Error**  
    ```python
    {format_exc()}
    ```
    """)
    st.stop()

# Footer
st.markdown("---")
st.caption("© 2024 AfriMarkets AI | Data from Yahoo Finance")
