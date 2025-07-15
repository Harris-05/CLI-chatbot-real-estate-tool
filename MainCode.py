import pandas as p
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

p.set_option('display.float_format', lambda x: '%.2f' % x)
def chatbot_interface(df, aggregates):
    print("Welcome to the Real Estate CLI Assistant! ")
    print("Ask me things like:\n"
          "- cheapest city\n"
          "- most expensive areas in Lahore\n"
          "- average price of property in Islamabad\n"
          "- avg area in Karachi\n"
          "- exit\n")

    while True:
        user_input = input("You: ").lower().strip()

        if user_input in ["exit", "quit", "bye"]:
            print("Bot: Goodbye! ")
            break

        elif "cheapest" in user_input and "city" in user_input:
            print("\nBot: Cheapest Cities by Price Per Marla:")
            print(aggregates["cheapest_cities"])
            print("\nBot: Do you want a graph:(y/n)")
            choice=input().lower().strip()
            if choice in ["y", "yes"]:
                plot_cheapest_cities(aggregates["cheapest_cities"])

        elif "expensive" in user_input and "cities" in user_input:
            print("\nBot: Most Expensive Cities by Price Per Marla:")
            print(aggregates["avg_ppm_city"].head(10))
            print("\nBot: Do you want a graph:(y/n)")
            choice=input().lower().strip()
            if choice in ["y", "yes"]:
                plot_avg_ppm(aggregates["avg_ppm_city"].head(10))

        elif "expensive" in user_input and "area" in user_input:
            for city in df["location_city"].unique():
                if city.lower() in user_input:
                    filtered = df[df["location_city"].str.lower() == city.lower()]
                    top_areas = (
                        filtered.groupby("location")["PPM"]
                        .mean().sort_values(ascending=False)
                        .head(5).round(2)
                    )
                    print(f"\nBot: Top expensive areas in {city.title()}:")
                    print(top_areas)
                    print("\nBot: Do you want a graph:(y/n)")
                    choice=input().lower().strip()
                    if choice in ["y", "yes"]:
                        top_areas.plot(kind="bar", title=f"Top Expensive Areas in {city.title()}", figsize=(10, 6))
                        plt.ylabel("Price Per Marla")
                        plt.xlabel("Area")
                        plt.tight_layout()
                        plt.show()
                    break
            else:
                print("Bot: Please mention a valid city name.")

        elif "average price" in user_input or "avg price" in user_input:
            for city in aggregates["avg_price_city"].index:
                if city.lower() in user_input:
                    avg_price = aggregates["avg_price_city"][city]
                    print(f"Bot: Average price in {city} is PKR {avg_price:,.0f}")
                    print("\nBot: Do you want a graph:(y/n)")
                    choice=input().lower().strip()
                    if choice in ["y", "yes"]:
                        plot_avg_price(aggregates["avg_price_city"].head(10))
                    break
            else:
                print("Bot: Couldn't find that city.")

        elif "average area" in user_input or "avg area" in user_input:
            for city in aggregates["avg_area_per_city"].index:
                if city.lower() in user_input:
                    avg_area = aggregates["avg_area_per_city"][city]
                    print(f"Bot: Average area in {city} is {avg_area} Marla")
                    print("\nBot: Do you want a graph:(y/n)")
                    choice=input().lower().strip()
                    if choice in ["y", "yes"]:
                        aggregates["avg_area_per_city"].head(10).plot(kind="bar", title="Avg Area per City", figsize=(10, 6))
                        plt.ylabel("Marla")
                        plt.xlabel("City")
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        plt.show()
                    break
            else:
                print("Bot: Couldn't find that city.")

        elif "trend" in user_input or "listing" in user_input:
            print("\nBot: Listings over time:")
            print(aggregates["listing_trend"].tail(10))
            print("\nBot: Do you want a graph:(y/n)")
            choice=input().lower().strip()
            if choice in ["y", "yes"]:
                aggregates["listing_trend"].plot(kind="line", title="Listing Trend", figsize=(10,6))
                plt.ylabel("Listings")
                plt.xlabel("Date")
                plt.tight_layout()
                plt.show()

        else:
            print("Bot: Sorry, I didn't understand that. Try asking about cheapest city, average price, etc.")


def convert_date(text):
    try:
        referencedate = datetime(2025, 7, 15)
        text = str(text).lower().strip()
        if text.startswith("added"):
            text = text.replace("added", "").strip()

        if "today" in text or "hour" in text or "hours" in text:
            return referencedate
        elif "yesterday" in text:
            return referencedate - timedelta(days=1)
        elif "day" in text or "days" in text:
            days = int(text.split()[0])
            return referencedate - timedelta(days=days)
        elif "week" in text or "weeks" in text:
            weeks = int(text.split()[0])
            return referencedate - timedelta(weeks=weeks)
        elif "month" in text or "months" in text:
            months = int(text.split()[0])
            return referencedate - timedelta(days=months * 30)
        elif "year" in text or "years" in text:
            years = int(text.split()[0])
            return referencedate - timedelta(days=years * 365)
        else:
            return np.nan
    except:
        return np.nan

def convert_area(area):
    try:
        if not isinstance(area, str):
            return np.nan
        area = area.lower().strip()
        parts = area.split()
        unit = parts[1]
        number = float(parts[0])

        if "kanal" in unit:
            return number * 20
        elif "sq." in unit:
            return number / 30.25
        elif "sqft" in unit:
            return number / 272.25
        else:
            return number
    except:
        return np.nan

def convert_price(price):
    try:
        if not isinstance(price, str):
            return np.nan

        price_str = price.lower().replace("pkr", "").strip()
        if any(keyword in price_str for keyword in ["contact", "n/a", "call", "ask", "coming soon"]):
            return np.nan

        parts = price_str.split()
        number = float(parts[0])
        unit = parts[1] if len(parts) > 1 else ""

        if "arab" in unit:
            return number * 1_000_000_000
        elif "crore" in unit:
            return number * 10_000_000
        elif "lakh" in unit:
            return number * 100_000
        elif "thousand" in unit:
            return number * 1_000
        else:
            return number
    except:
        return np.nan

# ----------------------------
# Data Processing
# ----------------------------
def preprocess_data(file_path):
    df = p.read_csv(file_path)
    df["NumPrice"] = df["price"].apply(convert_price)
    df["PostedDate"] = df["added"].apply(convert_date)
    df["area"] = df["area"].apply(convert_area).round(2)
    df["location"] = df["location"].str.title().str.strip()
    df["location_city"] = df["location_city"].str.title().str.strip()
    df["PPM"] = (df["NumPrice"] / df["area"]).round(3)

    # Remove outliers
    upper_limit = df["PPM"].quantile(0.99)
    lower_limit = df["PPM"].quantile(0.01)
    df = df[(df["PPM"] < upper_limit) & (df["PPM"] > lower_limit)]

    return df

def get_aggregates(df):
    return {
        "top_locations": df["location"].value_counts().head(10),
        "top_cities": df["location_city"].value_counts().head(10),
        "avg_ppm_city": df.groupby("location_city")["PPM"].mean().sort_values(ascending=False).round(3),
        "avg_price_city": df.groupby("location_city")["NumPrice"].mean().sort_values(ascending=False).round(2),
        "avg_ppm_location": df.groupby("location")["PPM"].mean().sort_values(ascending=False).round(2),
        "avg_price_location": df.groupby("location")["NumPrice"].mean().sort_values(ascending=False).round(2),
        "cheapest_cities": df.groupby("location_city")["PPM"].mean().sort_values().head(10),
        "avg_area_per_city": df.groupby("location_city")["area"].mean().sort_values(ascending=False).round(2),
        "listing_trend": df["PostedDate"].value_counts().sort_index()
    }


def plot_top_cities(top_cities):
    top_cities.plot(kind="bar", figsize=(10, 6), title="Top 10 Cities by Listings")
    plt.xlabel("Cities")
    plt.ylabel("No Of Listings")
    plt.tight_layout()
    plt.show()

def plot_avg_price(avg_price):
    avg_price.plot(kind="bar", figsize=(10, 6), title="Average Property Price per City")
    plt.ylabel("Avg Price")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_avg_ppm(avg_ppm):
    avg_ppm.plot(kind="bar", figsize=(10, 6), title="Avg Price per Marla by City")
    plt.ylabel("Price per Marla")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_cheapest_cities(cheapest):
    cheapest.plot(kind="bar", title="Cheapest Cities", figsize=(10, 6))
    plt.xlabel("Cities")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_scatter_price_vs_area(df):
    plt.scatter(df["area"], df["NumPrice"], alpha=0.5)
    plt.title("Area vs. Price")
    plt.xlabel("Area (Marla)")
    plt.ylabel("Price (PKR)")
    plt.tight_layout()
    plt.show()

def plot_histogram_ppm(df):
    df["PPM"].hist(bins=50, figsize=(10, 6))
    plt.title("Distribution of Price per Marla")
    plt.xlabel("PPM")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

def plot_multi_city_comparison(df):
    top_10_cities = df["location_city"].value_counts().head(10).index
    top_data = df[df["location_city"].isin(top_10_cities)]

    avg_price = top_data.groupby("location_city")["NumPrice"].mean().sort_values(ascending=False)
    avg_area = top_data.groupby("location_city")["area"].mean().sort_values(ascending=False)
    listing_counts = top_data["location_city"].value_counts()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    avg_price.plot(kind="barh", ax=axes[0], color="skyblue", title="Avg Price per City")
    avg_area.plot(kind="barh", ax=axes[1], color="salmon", title="Avg Area per City")
    listing_counts.sort_values(ascending=False).plot(kind="barh", ax=axes[2], color="lightgreen", title="No. of Listings")
    for ax in axes: ax.invert_yaxis()
    plt.tight_layout()
    plt.show()

data= preprocess_data("C:/Users/EliteSeries/Downloads/archive/property_data.csv")
aggregates=(get_aggregates(data))
chatbot_interface(data, aggregates)
