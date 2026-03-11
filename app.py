import streamlit as st
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh  # type: ignore
from data_loader import get_stock_data  # type: ignore
from prediction import predict_price  # type: ignore
from portfolio import add_stock, get_portfolio  # type: ignore
from news import get_news  # type: ignore

st.set_page_config(page_title="Dashboard", layout="wide")

# ---------------- STYLE ----------------

st.markdown("""
<style>
.block-container{
padding-top:2rem;
padding-left:2rem;
padding-right:2rem;
max-width:100%;
}

/* Main background */

.stApp{
background: linear-gradient(135deg,#0f172a,#1e293b);
color:white;
}

/* Sidebar */

section[data-testid="stSidebar"]{
background:#020617;
}

section[data-testid="stSidebar"] *{
color:white !important;
}

/* Input labels */

label{
color:#38bdf8 !important;
font-weight:bold;
}

/* Text input */

.stTextInput input{
background:#0f172a !important;
color:white !important;
border:1px solid #38bdf8 !important;
border-radius:8px;
}

/* Number input */

.stNumberInput input{
background:#0f172a !important;
color:white !important;
border:1px solid #38bdf8 !important;
border-radius:8px;
}

/* Buttons */

.stButton button{
background:#38bdf8;
color:black;
border-radius:8px;
font-weight:bold;
}

.stButton button:hover{
background:#0ea5e9;
color:white;
}

/* Cards */

.card{
background:#1e293b;
padding:20px;
border-radius:12px;
margin-bottom:15px;
}

/* Metric numbers */

.metric-value{
font-size:36px;
font-weight:bold;
color:#38bdf8;
}

/* Dataframe */

div[data-testid="stDataFrame"]{
background:#1e293b !important;
color:white !important;
}

div[data-testid="stDataFrame"] *{
color:white !important;
}

/* News card */

.news-card{
background:#1e293b;
padding:18px;
border-radius:10px;
margin-bottom:10px;
}

/* Profile */

.profile-card{
background:#1e293b;
padding:30px;
border-radius:15px;
text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.title("📊 Dashboard")

menu = st.sidebar.radio(
"Menu",
["Overview","Portfolio","News","Profile"]
)

symbol = st.sidebar.text_input("Stock Symbol","AAPL")

# ---------------- OVERVIEW ----------------

if menu == "Overview":

    st.title("📈 Market Overview")

    data = get_stock_data(symbol)

    if data is None or data.empty:
        st.error("Stock data not available")

    else:

        col1,col2,col3 = st.columns(3)

        latest = round(data["Close"].iloc[-1],2)
        high = round(data["High"].max(),2)
        low = round(data["Low"].min(),2)

        col1.markdown(f"""
        <div class="card">
        <h4>Latest Price</h4>
        <div class="metric-value">${latest}</div>
        </div>
        """,unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="card">
        <h4>Highest Price</h4>
        <div class="metric-value">${high}</div>
        </div>
        """,unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="card">
        <h4>Lowest Price</h4>
        <div class="metric-value">${low}</div>
        </div>
        """,unsafe_allow_html=True)

        st.subheader("Stock Trend")

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=data["Date"],
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            increasing_line_color="#22c55e",
            decreasing_line_color="#ef4444"
        ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(fig,use_container_width=True)

        pred = predict_price(data)

        st.success(f"Predicted Next Price: ${pred}")

# ---------------- PORTFOLIO ----------------

elif menu == "Portfolio":

    st.title("💼 Portfolio Tracker")

    col1,col2 = st.columns(2)

    sym = col1.text_input("Stock Symbol", placeholder="Example: AAPL")
    shares = col2.number_input("Shares", min_value=1, max_value=1000)

    price = None

    if sym != "":
        data = get_stock_data(sym)

        if data is not None and not data.empty:
            price = round(data["Close"].iloc[-1],2)
            st.info(f"Current Price: ${price}")
        else:
            st.warning("Stock symbol not found")

    if st.button("Add Stock"):

        if sym == "":
            st.error("Enter stock symbol")

        elif price is None:
            st.error("Price data not available")

        else:
            add_stock(sym,shares,price)
            st.success("Stock added successfully")

    st.subheader("📊 Portfolio Overview")

    portfolio_data = get_portfolio()

    if portfolio_data is not None and not portfolio_data.empty:

        st.markdown('<div class="card">',unsafe_allow_html=True)

        st.dataframe(portfolio_data,use_container_width=True)

        st.markdown('</div>',unsafe_allow_html=True)

    else:
        st.info("No stocks added yet.")

# ---------------- NEWS ----------------

elif menu == "News":

    st.title("📰 Market News")

    news = get_news()

    for article in news:

        st.markdown(f"""
        <div class="news-card">
        <h4 style="color:#38bdf8;">{article['title']}</h4>
        <p style="color:#e2e8f0;">{article['description']}</p>
        <a href="{article['url']}" target="_blank" style="color:#22c55e;">
        Read full article
        </a>
        </div>
        """, unsafe_allow_html=True)

# ---------------- PROFILE ----------------

elif menu == "Profile":

    st.title("👤 User Profile")

    st.markdown("""
    <div class="profile-card">

    <img src="https://cdn-icons-png.flaticon.com/512/149/149071.png" width="120">

    <h2 style="color:#38bdf8;">Srushti</h2>

    <p style="color:#e2e8f0;">Student</p>

    <hr>

    <p style="color:#e2e8f0;">
    Course: Data Analytics <br>
    Project: Stock Market Dashboard <br>
    Country: India
    </p>

    </div>
    """, unsafe_allow_html=True)