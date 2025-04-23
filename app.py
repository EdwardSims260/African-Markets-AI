import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from PIL import Image
import base64
import io
from traceback import format_exc

# Try to import feedparser with fallback
try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False
    st.warning("News feed functionality is limited because feedparser package is not installed.")

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
        st.title("AFRI-INVEST AI")

# Rest of your code remains the same until the news section...

    # ===== News Feed Section =====
    st.markdown("### 📰 Latest Market News")
    
    if FEEDPARSER_AVAILABLE:
        # Country-specific news feeds
        news_feeds = {
            "Nigeria": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=MTNN.LG&region=US&lang=en-US",
            "South Africa": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^JN0U.JO&region=US&lang=en-US",
            "Kenya": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=SCOM.NR&region=US&lang=en-US",
            "Egypt": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=COMI.CA&region=US&lang=en-US",
            "Morocco": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=IAM.CS&region=US&lang=en-US"
        }
        
        try:
            feed = feedparser.parse(news_feeds[country])
            if not feed.entries:
                st.warning("No news articles found for this market.")
            else:
                for entry in feed.entries[:5]:
                    st.markdown(f"🔹 [{entry.title}]({entry.link})")
        except Exception as e:
            st.warning(f"⚠️ Could not load news feed: {str(e)}")
    else:
        st.info("To enable news feeds, please install feedparser package:")
        st.code("pip install feedparser")
        # Show static news items as fallback
        st.markdown("""
        🔹 [African Markets Show Resilience Amid Global Volatility](#)
        🔹 [Nigeria's NGX Index Gains 1.5% in Week](#)
        🔹 [South Africa's Inflation Eases to 5.2%](#)
        🔹 [Kenya's Central Bank Holds Rates Steady](#)
        🔹 [Egypt Signs $1.5B Renewable Energy Deal](#)
        """)

# Rest of your original code continues...
    
    try:
        feed = feedparser.parse(news_feeds[country])
        if not feed.entries:
            st.warning("No news articles found for this market.")
        else:
            for entry in feed.entries[:5]:
                st.markdown(f"🔹 [{entry.title}]({entry.link})")
    except Exception as e:
        st.warning(f"⚠️ Could not load news feed: {str(e)}")

    # Plotly Chart with more data
    data = get_market_data(tickers[country])
    if data.empty:
        st.warning("No data available for this market index. Please try another country.")
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            line=dict(color="#FFD700", width=3),
            name="Closing Price",
            fill='tozeroy',
            fillcolor='rgba(255, 215, 0, 0.1)'
        ))

        fig.update_layout(
            title=f"{country} Market Trend (6 Months)",
            plot_bgcolor="#0A0C10",
            paper_bgcolor="#0A0C10",
            font=dict(color="white"),
            hovermode="x unified",
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="date"
            ),
            yaxis=dict(title="Index Value")
        )

        st.plotly_chart(fig, use_container_width=True)

    # AI Insights
    with st.expander("🔍 AI Market Insights", expanded=True):
        st.markdown(f"""
        **📈 Top Performing Sectors in {country}**  
        ▸ Financial Services (+12% YTD)  
        ▸ Telecommunications (+8% YTD)  

        **💎 Recommended Stocks**  
        1. {get_recommended_stocks(country)[0]}  
        2. {get_recommended_stocks(country)[1]}  
        """)

    with st.expander("📘 Learn: Investing in African Markets", expanded=False):
        st.markdown("""
        **🌍 What is the NGXASI?**  
        The Nigerian Exchange All-Share Index (NGXASI) tracks the general performance of listed stocks on the Nigerian Exchange.

        **📈 How to Invest in African Stocks**  
        ▸ Use local brokerage platforms like **Chaka**, **Bamboo**, or **Hisa**  
        ▸ Understand each country's market rules  
        ▸ Consider ETFs or Pan-African investment options

        **💡 Smart Tips for Beginners**  
        - Start with blue-chip or dividend-paying stocks  
        - Follow macroeconomic trends (e.g., inflation, FX rates)  
        - Diversify across sectors and countries
        """)

    st.markdown("### 🧠 Market Sentiment")

    sentiment = st.radio("How do you feel about the African market this week?", ["📈 Bullish", "📉 Bearish", "😐 Neutral"])
    st.success(f"Your view: {sentiment}")

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
st.caption("© 2024 AFRI-INVEST AI | Data from Yahoo Finance")

def get_recommended_stocks(country):
    """Helper function to return recommended stocks by country"""
    recommendations = {
        "Nigeria": ("MTN Nigeria (MTNN.LG)", "Dangote Cement (DANGCEM.LG)"),
        "South Africa": ("Naspers (NPN.JO)", "MTN Group (MTN.JO)"),
        "Kenya": ("Safaricom (SCOM.NR)", "Equity Group (EQTY.NR)"),
        "Egypt": ("Commercial International Bank (COMI.CA)", "EFG Hermes (HRHO.CA)"),
        "Morocco": ("Maroc Telecom (IAM.CS)", "Attijariwafa Bank (ATW.CS)")
    }
    return recommendations.get(country, ("Not available", "Not available"))
