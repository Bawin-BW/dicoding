import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from PIL import Image

def create_product_sell_df(df):
    product_sell_df = df.groupby('product_category_name_english')['customer_id'].nunique().reset_index().sort_values(by='customer_id', ascending=False)
    return product_sell_df

orders_dataset = pd.read_csv("../data/order_dataset.csv")
accepted_time = pd.read_csv("../data/accepted_time.csv")
delivery_time = pd.read_csv("../data/delivery_time.csv")
geo_customers = pd.read_csv("../data/geo_customers.csv")
geo_sellers = pd.read_csv("../data/geo_sellers.csv")
name_product = pd.read_csv("../data/name_product.csv")
order_payments_dataset = pd.read_csv("../data/order_payments_dataset.csv")
orders_customers = pd.read_csv("../data/orders_customers.csv")
product_revenue_df = pd.read_csv("../data/product_revenue_df.csv")
product_revenue_name = pd.read_csv("../data/product_revenue_name.csv")
product_revenue = pd.read_csv("../data/product_revenue.csv")
product_sell = pd.read_csv("../data/product_sell.csv")

st.header('Garuda Toserba :sparkles:')

with st.sidebar:

    st.title("Bagas Winerang")
    
    st.image("../data/toko.png")\


##### Sales Analysis #####
st.header("Sales Analysis of Product Categories")

# Group by product category and count unique customers
product_counts = product_sell.groupby('product_category_name_english')['customer_id'].nunique().sort_values(ascending=False)

# Select top 5 and bottom 5 products
top_5_products = product_counts.head(5).reset_index()
bottom_5_products = product_counts.tail(5).reset_index()

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

# Plot top 5 products on the left (horizontal bar plot)
sns.barplot(x=top_5_products['customer_id'], y=top_5_products['product_category_name_english'], ax=ax1, color='blue')
ax1.set_xlabel('Number of Products Sold')
ax1.set_ylabel('Product Category')
ax1.set_title('Top 5 Best-Selling Products')

# Plot bottom 5 products on the right (horizontal bar plot)
sns.barplot(x=bottom_5_products['customer_id'], y=bottom_5_products['product_category_name_english'], ax=ax2, color='red')
ax2.set_xlabel('Number of Products Sold')
ax2.set_ylabel('Product Category')
ax2.set_title('Bottom 5 Least-Selling Products')

# Adjust the layout with space between the plots
plt.subplots_adjust(wspace=0.8)  # Adjust the space between the subplots

# Display the plot in Streamlit
st.pyplot(fig)

###### Acceptance and Delivery ######

st.header("Order Acceptance and Delivery Analysis")

#orders_dataset is already defined and contains the necessary data
accepted_times = orders_dataset['accepted_time']
delivery_times = orders_dataset['delivery_time']

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Create a figure with two subplots
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Plot for accepted times
sns.histplot(accepted_times, bins=7, color=colors[0], ax=axs[0])
axs[0].set_xlabel('Order Acceptance Time (days)')
axs[0].set_ylabel('Frequency')
axs[0].set_title('Distribution of Order Acceptance Time')

# Plot for delivery times
sns.histplot(delivery_times, bins=20, color=colors[0], ax=axs[1])
axs[1].set_xlabel('Order Delivery Time (days)')
axs[1].set_ylabel('Frequency')
axs[1].set_title('Distribution of Order Delivery Time')

# Adjust layout and add space between subplots
plt.tight_layout()
plt.subplots_adjust(wspace=0.3)  # Adjust the width space between the subplots

# Display the plot in Streamlit
st.pyplot(fig)

####### Payment Type #######

# Add a header in Streamlit
st.header("Analysis of Payment Methods Used by Customers")

# Assuming order_payments_dataset is already defined and contains the necessary data
payment_type_counts = order_payments_dataset['payment_type'].value_counts()

# Create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x=payment_type_counts.index, y=payment_type_counts.values, palette="viridis")
plt.xlabel('Payment Method')
plt.ylabel('Number of Transactions')
plt.title('Payment Methods Used by Customers')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)

####### Geographical ########

# Set header for the Streamlit app
st.header("Geographical Distribution of Sellers and Customers")

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # Set figure size

# Scatter plot for Customers
ax1.scatter(
    geo_customers["geolocation_lng"],
    geo_customers["geolocation_lat"],
    s=0.5,  # Adjust marker size as needed
    alpha=0.25,
    color="blue",  # Color for customers
)
ax1.set_xlabel("Longitude")
ax1.set_ylabel("Latitude")
ax1.set_title("Geographical Distribution of Customers")
ax1.grid(True)

# Scatter plot for Sellers
ax2.scatter(
    geo_sellers["geolocation_lng"],
    geo_sellers["geolocation_lat"],
    s=0.5,  # Adjust marker size as needed
    alpha=0.25,
    color="red",  # Color for sellers
)
ax2.set_xlabel("Longitude")
ax2.set_ylabel("Latitude")
ax2.set_title("Geographical Distribution of Sellers")
ax2.grid(True)

# Adjust layout for better spacing
plt.tight_layout()
plt.subplots_adjust(wspace=0.3)  # Increase space between subplots

# Display the combined plot in Streamlit
st.pyplot(fig)

# Streamlit layout for combined distribution
st.subheader("Geographical Distribution of Customers and Sellers")

# Create the combined plot
fig, ax = plt.subplots(figsize=(10, 6))

# Scatter plot for sellers
ax.scatter(
    geo_sellers['geolocation_lng'],
    geo_sellers['geolocation_lat'],
    s=10,
    alpha=0.5,
    label='Seller',
    color='red'
)

# Scatter plot for customers
ax.scatter(
    geo_customers['geolocation_lng'],
    geo_customers['geolocation_lat'],
    s=1,
    alpha=0.25,
    label='Customer',
    color='blue'
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Geographical Distribution of Customers and Sellers")
ax.grid(True)
ax.legend()

# Display the combined plot in Streamlit
st.pyplot(fig)

# Path to the image
img_path = '../data/gambar_geo.png'  # Update this path
img = Image.open(img_path)

# Streamlit layout for the geographical distribution
st.subheader("Global Geographical Distribution of Sellers and Customers")

# Create the figure and axis
fig, ax = plt.subplots(figsize=(13, 6))

# Display the image
ax.imshow(img, extent=[-180, 180, -90, 90])

# Scatter plot for sellers
ax.scatter(geo_sellers['geolocation_lng'], geo_sellers['geolocation_lat'],
           s=10, c='red', marker='o', label='Sellers')

# Scatter plot for customers
ax.scatter(geo_customers['geolocation_lng'], geo_customers['geolocation_lat'],
           s=5, c='blue', marker='x', label='Customers')

# Set labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Distribution of Sellers and Customers')
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)