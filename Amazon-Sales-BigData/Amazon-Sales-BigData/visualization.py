from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, desc, year, month
import matplotlib.pyplot as plt
import os

# ==========================================
# CREATE SPARK SESSION
# ==========================================

spark = SparkSession.builder \
    .appName("Amazon Sales Visualization") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# ==========================================
# CREATE OUTPUT FOLDER
# ==========================================

os.makedirs("output", exist_ok=True)

# ==========================================
# LOAD DATA
# ==========================================

df = spark.read.csv(
    "data/Amazon.csv",
    header=True,
    inferSchema=True
)

# ==========================================
# DATA CLEANING
# ==========================================

clean_df = df.dropDuplicates(["OrderID"])

clean_df = clean_df.filter(
    (col("Quantity") > 0) &
    (col("UnitPrice") > 0)
)

# ==========================================
# 1. CATEGORY-WISE SALES
# ==========================================

category_sales = clean_df.groupBy(
    "Category"
).agg(
    sum("TotalAmount").alias("TotalSales")
).orderBy(
    desc("TotalSales")
)

category_pd = category_sales.toPandas()

plt.figure(figsize=(10, 6))

plt.bar(
    category_pd["Category"],
    category_pd["TotalSales"]
)

plt.title("Category-wise Sales")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("output/category_sales.png")
plt.close()

# ==========================================
# 2. TOP 10 PRODUCTS
# ==========================================

top_products = clean_df.groupBy(
    "ProductName"
).agg(
    sum("Quantity").alias("TotalQuantity")
).orderBy(
    desc("TotalQuantity")
).limit(10)

products_pd = top_products.toPandas()

plt.figure(figsize=(10, 6))

plt.barh(
    products_pd["ProductName"],
    products_pd["TotalQuantity"]
)

plt.title("Top 10 Products by Quantity Sold")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig("output/top_products.png")
plt.close()

# ==========================================
# 3. PAYMENT METHOD ANALYSIS
# ==========================================

payment_data = clean_df.groupBy(
    "PaymentMethod"
).agg(
    count("*").alias("Orders")
).orderBy(
    desc("Orders")
)

payment_pd = payment_data.toPandas()

plt.figure(figsize=(8, 6))

plt.pie(
    payment_pd["Orders"],
    labels=payment_pd["PaymentMethod"],
    autopct="%1.1f%%"
)

plt.title("Orders by Payment Method")

plt.tight_layout()

plt.savefig("output/payment_methods.png")
plt.close()

# ==========================================
# 4. COUNTRY-WISE SALES
# ==========================================

country_sales = clean_df.groupBy(
    "Country"
).agg(
    sum("TotalAmount").alias("TotalSales")
).orderBy(
    desc("TotalSales")
)

country_pd = country_sales.toPandas()

plt.figure(figsize=(9, 6))

plt.bar(
    country_pd["Country"],
    country_pd["TotalSales"]
)

plt.title("Country-wise Sales")
plt.xlabel("Country")
plt.ylabel("Total Sales")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig("output/country_sales.png")
plt.close()

# ==========================================
# 5. ORDER STATUS
# ==========================================

status_data = clean_df.groupBy(
    "OrderStatus"
).agg(
    count("*").alias("Orders")
).orderBy(
    desc("Orders")
)

status_pd = status_data.toPandas()

plt.figure(figsize=(9, 6))

plt.bar(
    status_pd["OrderStatus"],
    status_pd["Orders"]
)

plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

plt.tight_layout()

plt.savefig("output/order_status.png")
plt.close()

# ==========================================
# 6. MONTHLY SALES TREND
# ==========================================

monthly_sales = clean_df.groupBy(
    year("OrderDate").alias("Year"),
    month("OrderDate").alias("Month")
).agg(
    sum("TotalAmount").alias("TotalSales")
).orderBy(
    "Year",
    "Month"
)

monthly_pd = monthly_sales.toPandas()

monthly_pd["Period"] = (
    monthly_pd["Year"].astype(str)
    + "-"
    + monthly_pd["Month"].astype(str).str.zfill(2)
)

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_pd["Period"],
    monthly_pd["TotalSales"],
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Year-Month")
plt.ylabel("Total Sales")

plt.xticks(rotation=90)

plt.tight_layout()

plt.savefig("output/monthly_sales.png")
plt.close()

# ==========================================
# FINISH
# ==========================================

print("\n===================================")
print("ALL CHARTS GENERATED SUCCESSFULLY")
print("===================================")

print("\nCharts saved inside the output folder:")
print("1. category_sales.png")
print("2. top_products.png")
print("3. payment_methods.png")
print("4. country_sales.png")
print("5. order_status.png")
print("6. monthly_sales.png")

spark.stop()