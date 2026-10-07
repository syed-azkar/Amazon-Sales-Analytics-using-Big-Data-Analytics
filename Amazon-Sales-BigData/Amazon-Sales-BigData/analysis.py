from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    sum,
    avg,
    desc,
    month,
    year,
    round
)

# ==========================================
# CREATE SPARK SESSION
# ==========================================

spark = SparkSession.builder \
    .appName("Amazon Sales Analysis") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("\n===================================")
print("AMAZON SALES DATA ANALYSIS")
print("===================================")

# ==========================================
# LOAD DATASET
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

print("\nTotal Records:", clean_df.count())

# ==========================================
# 1. TOTAL REVENUE
# ==========================================

print("\n1. TOTAL REVENUE")

total_revenue = clean_df.select(
    round(sum("TotalAmount"), 2).alias("Total Revenue")
)

total_revenue.show()

# ==========================================
# 2. AVERAGE ORDER VALUE
# ==========================================

print("\n2. AVERAGE ORDER VALUE")

average_order = clean_df.select(
    round(avg("TotalAmount"), 2).alias("Average Order Value")
)

average_order.show()

# ==========================================
# 3. TOTAL QUANTITY SOLD
# ==========================================

print("\n3. TOTAL QUANTITY SOLD")

total_quantity = clean_df.select(
    sum("Quantity").alias("Total Quantity Sold")
)

total_quantity.show()

# ==========================================
# 4. TOP 10 PRODUCTS
# ==========================================

print("\n4. TOP 10 PRODUCTS BY QUANTITY")

top_products = clean_df.groupBy(
    "ProductName"
).agg(
    sum("Quantity").alias("Total Quantity")
).orderBy(
    desc("Total Quantity")
).limit(10)

top_products.show(truncate=False)

# ==========================================
# 5. CATEGORY-WISE SALES
# ==========================================

print("\n5. CATEGORY-WISE SALES")

category_sales = clean_df.groupBy(
    "Category"
).agg(
    round(sum("TotalAmount"), 2).alias("Total Sales")
).orderBy(
    desc("Total Sales")
)

category_sales.show(truncate=False)

# ==========================================
# 6. BRAND-WISE SALES
# ==========================================

print("\n6. TOP 10 BRANDS BY SALES")

brand_sales = clean_df.groupBy(
    "Brand"
).agg(
    round(sum("TotalAmount"), 2).alias("Total Sales")
).orderBy(
    desc("Total Sales")
).limit(10)

brand_sales.show(truncate=False)

# ==========================================
# 7. PAYMENT METHOD ANALYSIS
# ==========================================

print("\n7. PAYMENT METHOD ANALYSIS")

payment_analysis = clean_df.groupBy(
    "PaymentMethod"
).agg(
    count("*").alias("Number of Orders"),
    round(sum("TotalAmount"), 2).alias("Total Sales")
).orderBy(
    desc("Number of Orders")
)

payment_analysis.show(truncate=False)

# ==========================================
# 8. COUNTRY-WISE SALES
# ==========================================

print("\n8. COUNTRY-WISE SALES")

country_sales = clean_df.groupBy(
    "Country"
).agg(
    count("*").alias("Orders"),
    round(sum("TotalAmount"), 2).alias("Total Sales")
).orderBy(
    desc("Total Sales")
)

country_sales.show(truncate=False)

# ==========================================
# 9. MONTHLY SALES
# ==========================================

print("\n9. MONTHLY SALES")

monthly_sales = clean_df.groupBy(
    year("OrderDate").alias("Year"),
    month("OrderDate").alias("Month")
).agg(
    round(sum("TotalAmount"), 2).alias("Total Sales")
).orderBy(
    "Year",
    "Month"
)

monthly_sales.show(50)

# ==========================================
# STOP SPARK
# ==========================================

spark.stop()