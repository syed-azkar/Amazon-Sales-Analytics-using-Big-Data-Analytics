import streamlit as st
import pandas as pd

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Amazon Sales Analytics",
    page_icon="🛒",
    layout="wide"
)

# ==========================================================
# SIMPLE CSS
# ==========================================================

st.markdown("""
<style>

/* ================================
   MAIN PAGE
   ================================ */

.stApp {
    background-color: #f5f7fb;
}


/* ================================
   SIDEBAR
   ================================ */

[data-testid="stSidebar"] {
    background-color: #131921;
}


/* Sidebar headings and labels */

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label {
    color: white !important;
}


/* Sidebar normal text */

[data-testid="stSidebar"] p {
    color: white !important;
}


/* ================================
   DROPDOWN
   ================================ */

/* White dropdown box */

[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: white !important;
    border-radius: 8px !important;
}


/* Inner dropdown */

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: white !important;
}


/* Selected dropdown text */

[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #000000 !important;
}


/* Dropdown input */

[data-testid="stSidebar"] [data-baseweb="select"] input {
    color: #000000 !important;
}


/* Dropdown arrow */

[data-testid="stSidebar"] [data-baseweb="select"] svg {
    color: #000000 !important;
    fill: #000000 !important;
}


/* Dropdown menu */

[role="listbox"] {
    background-color: white !important;
}


/* Dropdown options */

[role="option"] {
    background-color: white !important;
    color: #000000 !important;
}


/* Dropdown option hover */

[role="option"]:hover {
    background-color: #eeeeee !important;
    color: #000000 !important;
}


/* ================================
   HEADINGS
   ================================ */

h1 {
    color: #131921;
}

h2,
h3 {
    color: #232f3e;
}


/* ================================
   KPI CARDS
   ================================ */

[data-testid="stMetric"] {
    background-color: white;

    border: 1px solid #dddddd;

    border-radius: 12px;

    padding: 15px;

    box-shadow:
        0px 3px 10px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# TITLE
# ==========================================================

st.title("🛒 Amazon Sales Analytics")

st.write(
    "Interactive Big Data Analytics Dashboard using "
    "Python, Pandas, PySpark & Streamlit"
)

st.divider()


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/Amazon.csv")

    df = df.drop_duplicates(
        subset=["OrderID"]
    )

    df = df[
        (df["Quantity"] > 0) &
        (df["UnitPrice"] > 0)
    ]

    return df


try:

    df = load_data()

except Exception as e:

    st.error(
        f"Error loading data: {e}"
    )

    st.stop()


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🛒 Amazon Analytics")

st.sidebar.subheader("🔎 Filters")


# ==========================================================
# COUNTRY
# ==========================================================

countries = ["All"] + sorted(
    df["Country"]
    .dropna()
    .astype(str)
    .unique()
)

selected_country = st.sidebar.selectbox(
    "🌍 Country",
    countries
)


# ==========================================================
# CATEGORY
# ==========================================================

categories = ["All"] + sorted(
    df["Category"]
    .dropna()
    .astype(str)
    .unique()
)

selected_category = st.sidebar.selectbox(
    "📦 Category",
    categories
)


# ==========================================================
# STATUS
# ==========================================================

statuses = ["All"] + sorted(
    df["OrderStatus"]
    .dropna()
    .astype(str)
    .unique()
)

selected_status = st.sidebar.selectbox(
    "📋 Order Status",
    statuses
)


# ==========================================================
# DATASET INFORMATION
# ==========================================================

st.sidebar.divider()

st.sidebar.subheader("📊 Dataset")

st.sidebar.write(
    f"Transactions: **{len(df):,}**"
)

st.sidebar.write(
    f"Products: **{df['ProductName'].nunique():,}**"
)

st.sidebar.write(
    f"Countries: **{df['Country'].nunique():,}**"
)


# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = df.copy()


if selected_country != "All":

    filtered_df = filtered_df[
        filtered_df["Country"].astype(str)
        == selected_country
    ]


if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"].astype(str)
        == selected_category
    ]


if selected_status != "All":

    filtered_df = filtered_df[
        filtered_df["OrderStatus"].astype(str)
        == selected_status
    ]


# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_sales = filtered_df["TotalAmount"].sum()

total_orders = filtered_df["OrderID"].nunique()

total_quantity = filtered_df["Quantity"].sum()


if total_orders > 0:

    average_order = (
        total_sales / total_orders
    )

else:

    average_order = 0


# ==========================================================
# KPI
# ==========================================================

st.header("📊 Key Performance Indicators")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}"
    )


with col2:

    st.metric(
        "🛍️ Total Orders",
        f"{total_orders:,}"
    )


with col3:

    st.metric(
        "📦 Quantity Sold",
        f"{total_quantity:,}"
    )


with col4:

    st.metric(
        "💳 Average Order",
        f"${average_order:,.2f}"
    )


# ==========================================================
# FILTERED SUMMARY
# ==========================================================

st.header("📈 Filtered Sales Summary")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Filtered Sales",
        f"${filtered_df['TotalAmount'].sum():,.2f}"
    )


with col2:

    st.metric(
        "Filtered Orders",
        f"{filtered_df['OrderID'].nunique():,}"
    )


with col3:

    st.metric(
        "Filtered Quantity",
        f"{filtered_df['Quantity'].sum():,}"
    )


# ==========================================================
# SALES VISUALIZATIONS
# ==========================================================

st.header("📊 Sales Visualizations")


col1, col2 = st.columns(2)


# ==========================================================
# CATEGORY
# ==========================================================

with col1:

    st.subheader("📦 Category-wise Sales")

    category_data = (
        filtered_df
        .groupby("Category")["TotalAmount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        category_data
    )


# ==========================================================
# COUNTRY
# ==========================================================

with col2:

    st.subheader("🌍 Country-wise Sales")

    country_data = (
        filtered_df
        .groupby("Country")["TotalAmount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        country_data
    )


# ==========================================================
# PRODUCTS
# ==========================================================

st.header("🏆 Top 10 Products")


top_products = (
    filtered_df
    .groupby("ProductName")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


st.bar_chart(
    top_products
)


# ==========================================================
# PAYMENT METHOD
# ==========================================================

st.header("💳 Payment Method Analysis")


payment_data = (
    filtered_df
    .groupby("PaymentMethod")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
)


st.bar_chart(
    payment_data
)


# ==========================================================
# ORDER STATUS
# ==========================================================

st.header("📦 Order Status")


status_data = (
    filtered_df["OrderStatus"]
    .value_counts()
)


st.bar_chart(
    status_data
)


# ==========================================================
# TRANSACTION DATA
# ==========================================================

st.header("📋 Transaction Data")


st.dataframe(
    filtered_df.head(100),
    use_container_width=True,
    height=400
)


# ==========================================================
# DOWNLOAD
# ==========================================================

st.header("📥 Download Data")


csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Filtered Sales Data",
    data=csv_data,
    file_name="amazon_filtered_sales.csv",
    mime="text/csv"
)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()


st.caption(
    "Amazon Sales Data Analytics | "
    "Big Data Analytics Mini Project | "
    "Python + Pandas + PySpark + Streamlit"
)