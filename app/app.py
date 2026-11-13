
import sys
import math
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Worldwide Smart Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. PROJECT PATHS
# Supports app.py in either the root folder or src folder.
# ============================================================

APP_DIR = Path(__file__).resolve().parent

if APP_DIR.name.lower() == "src":
    PROJECT_DIR = APP_DIR.parent
    SRC_DIR = APP_DIR
else:
    PROJECT_DIR = APP_DIR
    SRC_DIR = PROJECT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ============================================================
# 3. IMPORT EXISTING PROJECT FUNCTIONS
# ============================================================
import sys
from pathlib import Path

# Locate the main project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_DIR / "src"

# Allow Python to find modules inside the src folder
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
    
from live_data import (
    search_destination,
    get_destination_weather,
    get_travel_advice,
)

from recommendation_model import (
    load_destinations,
    build_recommendation_model,
    recommend_destinations,
)

import importlib
import budget_benchmarks
import trip_planner
importlib.reload(budget_benchmarks)
importlib.reload(trip_planner)
from trip_planner import create_detailed_itinerary

from budget_benchmarks import (
    calculate_real_trip_budget,
    analyze_budget_feasibility,
    get_alternative_destinations,
    get_international_vs_domestic_comparison,
    get_country_benchmark,
    get_transport_options,
    get_own_vehicle_feasibility,
    check_is_domestic,
)


# ============================================================
# 4. DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */

    .stApp {
        background-color: #10141c;
        color: #f1f5f9;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Headings */

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4 {
        color: #f8fafc;
    }

    /* General text */

    .stApp p,
    .stApp li,
    .stApp label {
        color: #dbe4ee;
    }

    /* Sidebar */

    [data-testid="stSidebar"] {
        background-color: #1b2432;
        border-right: 1px solid #334155;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #f1f5f9;
    }

    /* Hero section */

    .hero {
        padding: 1.6rem;
        border-radius: 18px;
        background: linear-gradient(
            120deg,
            #173c32,
            #172d46
        );
        border: 1px solid #334155;
        margin-bottom: 1.2rem;
    }

    .hero h1 {
        color: #ffffff !important;
        margin: 0;
        font-size: 2.2rem;
    }

    .hero p {
        color: #dbeafe !important;
        margin-top: 0.6rem;
        margin-bottom: 0;
        font-size: 1rem;
    }

    /* Input fields */

    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        background-color: #f8fafc !important;
        color: #111827 !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 8px;
    }

    .stTextInput input::placeholder,
    .stNumberInput input::placeholder {
        color: #64748b !important;
        opacity: 0.9 !important;
    }

    /* Select boxes */

    [data-baseweb="select"] > div {
        background-color: #f8fafc;
        color: #111827;
        border-radius: 8px;
    }

    [data-baseweb="select"] input {
        color: #111827 !important;
    }

    /* Dropdown menu */

    [data-baseweb="popover"],
    [data-baseweb="menu"] {
        background-color: #ffffff;
    }

    [role="option"] {
        color: #111827 !important;
        background-color: #ffffff;
    }

    /* Buttons */

    .stButton > button,
    .stFormSubmitButton > button {
        background-color: #ff4b4b;
        color: #ffffff !important;
        border: none;
        border-radius: 9px;
        padding: 0.55rem 1rem;
        font-weight: 600;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #e63946;
        color: #ffffff !important;
        border: none;
    }

    /* Metric cards */

    [data-testid="stMetric"] {
        background-color: #1b2432;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #334155;
    }

    [data-testid="stMetricLabel"] {
        color: #cbd5e1;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
    }

    /* Expanders */

    [data-testid="stExpander"] {
        background-color: #17202d;
        border: 1px solid #334155;
        border-radius: 12px;
    }

    /* Tabs */

    [data-testid="stTabs"] button {
        color: #e2e8f0;
    }

    /* Tables */

    [data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 8px;
    }

    /* Horizontal separator */

    hr {
        border-color: #475569;
    }

    /* Links */

    .stApp a {
        color: #7dd3fc;
    }

    /* Alerts */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 5. HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🌍 Worldwide Smart Travel Planner</h1>
        <p>
            Discover destinations, build your trip package,
            check the weather, and plan your budget in one place.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Weather is live when available. "
    "Budgets and itineraries are estimates, not confirmed bookings."
)


# ============================================================
# 6. HELPER FUNCTIONS
# ============================================================

@st.cache_resource
def load_india_model():
    df = load_destinations()

    df, vectorizer, feature_matrix = (
        build_recommendation_model(df)
    )

    return df, vectorizer, feature_matrix


def money(value):
    return f"₹{value:,.0f}"


def build_budget_breakdown(total_budget):
    """Fallback naive percentage breakdown for backwards compatibility."""
    allocations = {
        "Accommodation": 0.30,
        "Food": 0.25,
        "Transport": 0.30,
        "Activities & sightseeing": 0.10,
        "Emergency reserve": 0.05,
    }

    return pd.DataFrame({
        "Expense": list(allocations.keys()),
        "Share": [
            f"{share:.0%}"
            for share in allocations.values()
        ],
        "Estimated amount (INR)": [
            round(total_budget * share)
            for share in allocations.values()
        ],
    })


def get_real_budget_dataframe(real_plan):
    """Create a structured DataFrame from authentic real-world benchmark plan."""
    rows = []
    for item in real_plan["items"]:
        rows.append({
            "Expense Item": item["Expense"],
            "Category": item["Category"],
            "Market Unit Rate": item["Rate / Unit"],
            "Estimated Amount (INR)": item.get("Estimated Amount (INR)", item.get("Estimated amount (INR)", 0)),
            "Share of Total": item["Share"],
            "Notes": item["Notes"],
        })
    return pd.DataFrame(rows)


def get_budget_comparison_dataframe(user_budget, real_plan):
    """
    Compare the user's allocated budget with the real-world market costs
    to illustrate why naive allocations fail for international travel.
    """
    user_budget = float(user_budget)
    real_total = float(real_plan["estimated_total_cost"])
    is_domestic = real_plan["is_domestic"]

    # Calculate what a naive percentage would allocate vs what is actually required
    comparisons = [
        {
            "Expense Category": "Flights & Intercity Travel",
            "Naive Flat Allocation (30%)": round(user_budget * 0.30),
            "Realistic Market Need (INR)": real_plan["total_flights"],
            "Difference": round(user_budget * 0.30 - real_plan["total_flights"]),
            "Reality Assessment": (
                "🚨 Flights alone exceed your transport share!"
                if real_plan["total_flights"] > user_budget * 0.30
                else "✅ Sufficient for domestic transit"
            )
        },
        {
            "Expense Category": "Accommodation",
            "Naive Flat Allocation (30%)": round(user_budget * 0.30),
            "Realistic Market Need (INR)": real_plan["total_accommodation"],
            "Difference": round(user_budget * 0.30 - real_plan["total_accommodation"]),
            "Reality Assessment": (
                "⚠️ Insufficient for foreign hotel rates"
                if real_plan["total_accommodation"] > user_budget * 0.30
                else "✅ Adequate for comfortable stay"
            )
        },
        {
            "Expense Category": "Food & Dining",
            "Naive Flat Allocation (25%)": round(user_budget * 0.25),
            "Realistic Market Need (INR)": real_plan["total_food"],
            "Difference": round(user_budget * 0.25 - real_plan["total_food"]),
            "Reality Assessment": (
                "⚠️ Foreign currency meals cost more"
                if real_plan["total_food"] > user_budget * 0.25
                else "✅ Well covered"
            )
        },
        {
            "Expense Category": "Local Transit",
            "Naive Flat Allocation (Share)": round(user_budget * 0.05),
            "Realistic Market Need (INR)": real_plan["total_local_transit"],
            "Difference": round(user_budget * 0.05 - real_plan["total_local_transit"]),
            "Reality Assessment": "Subway passes & local cabs"
        },
    ]

    if not is_domestic and real_plan["total_visa_insurance"] > 0:
        comparisons.append({
            "Expense Category": "Visa & Travel Insurance",
            "Naive Flat Allocation (Share)": 0,
            "Realistic Market Need (INR)": real_plan["total_visa_insurance"],
            "Difference": -real_plan["total_visa_insurance"],
            "Reality Assessment": "🚨 Omitted in naive domestic model; mandatory abroad"
        })

    comparisons.append({
        "Expense Category": "Activities & Sightseeing",
        "Naive Flat Allocation (10%)": round(user_budget * 0.10),
        "Realistic Market Need (INR)": real_plan["total_activities"],
        "Difference": round(user_budget * 0.10 - real_plan["total_activities"]),
        "Reality Assessment": "Museums & attraction tickets"
    })

    comparisons.append({
        "Expense Category": "TOTAL TRIP EXPENSE",
        "Naive Flat Allocation (Total)": round(user_budget),
        "Realistic Market Need (INR)": round(real_total),
        "Difference": round(user_budget - real_total),
        "Reality Assessment": (
            f"Deficit of ₹{abs(user_budget - real_total):,.0f}"
            if user_budget < real_total
            else f"Surplus of ₹{(user_budget - real_total):,.0f}"
        )
    })

    return pd.DataFrame(comparisons)



def make_basic_itinerary(destination, days, preference):

    ideas = {
        "Beach": [
            "Explore a popular beach and nearby coastal attractions.",
            "Enjoy a coastal walk and explore local food.",
            "Visit another beach or choose a suitable local activity.",
        ],

        "Hills and Nature": [
            "Explore a scenic viewpoint or nature attraction.",
            "Plan a nature walk or a guided outdoor activity.",
            "Visit a garden, waterfall, or another nearby attraction.",
        ],

        "Historical": [
            "Visit a historical monument or cultural attraction.",
            "Explore a museum, heritage area, or guided tour.",
            "Visit another cultural landmark and a local market.",
        ],

        "Adventure": [
            "Explore an outdoor attraction suitable for the season.",
            "Consider a reputable guided activity after checking safety conditions.",
            "Visit a nearby attraction or plan a relaxed day.",
        ],

        "City and Culture": [
            "Explore the city centre and a cultural attraction.",
            "Visit a museum or neighbourhood and try local cuisine.",
            "Explore a local market and another city attraction.",
        ],

        "Any": [
            "Explore a popular local attraction.",
            "Visit a cultural site, nature spot, or guided tour.",
            "Explore a local market and another attraction.",
        ],
    }

    options = ideas.get(preference, ideas["Any"])

    itinerary = []

    for day in range(1, int(days) + 1):
        itinerary.append({
            "Day": f"Day {day}",
            "Destination": destination,
            "Suggested plan": options[
                (day - 1) % len(options)
            ],
        })

    return pd.DataFrame(itinerary)


def save_package(destination, country, description=""):
    if check_is_domestic(destination, country):
        country = "India"

    st.session_state["package_destination"] = destination
    st.session_state["package_country"] = country
    st.session_state["package_description"] = description

    # A new selection should not display old weather.
    st.session_state.pop("package_weather", None)
    st.session_state.pop("package_weather_error", None)

    # Clear the previous generated package profile.
    st.session_state.pop("active_package_profile", None)

    st.session_state["active_package_destination"] = destination
    st.session_state["active_package_country"] = country


# ============================================================
# 7. SIDEBAR: TRIP PREFERENCES
# ============================================================

st.sidebar.header("🧭 Your Trip Preferences")

starting_location = st.sidebar.selectbox(
    "Starting location",
    [
        "Malappuram, Kerala",
        "Kozhikode, Kerala",
    ],
)

scope = st.sidebar.radio(
    "Destination scope",
    ["India", "Worldwide"],
    horizontal=True,
)


# Country options for worldwide searches.

COUNTRY_DEFAULTS = {
    "Thailand": "Bangkok",
    "Japan": "Tokyo",
    "United Arab Emirates": "Dubai",
    "Singapore": "Singapore",
    "Malaysia": "Kuala Lumpur",
    "Indonesia": "Bali",
    "France": "Paris",
    "Italy": "Rome",
    "United Kingdom": "London",
    "Switzerland": "Zurich",
    "Australia": "Sydney",
    "Canada": "Toronto",
    "United States": "New York",
    "Germany": "Berlin",
    "Spain": "Barcelona",
    "Sri Lanka": "Colombo",
    "Nepal": "Kathmandu",
    "Maldives": "Male",
    "Vietnam": "Hanoi",
    "Turkey": "Istanbul",
}

countries = list(COUNTRY_DEFAULTS.keys())

POPULAR_WORLDWIDE_DESTINATIONS = {
    "Thailand": [
        {
            "name": "Bangkok",
            "experience": "City and Culture",
            "tagline": "Vibrant capital known for ornate shrines, floating markets, street food & bustling nightlife.",
            "best_season": "Nov to Feb (Cool & dry)",
            "highlights": "Grand Palace, Wat Arun, Chatuchak Weekend Market, Chao Phraya river cruises",
        },
        {
            "name": "Phuket",
            "experience": "Beach",
            "tagline": "Thailand's largest tropical island with white sand beaches, coral reefs, and vibrant beach clubs.",
            "best_season": "Nov to Apr",
            "highlights": "Patong Beach, Phi Phi Islands day tours, Big Buddha, scuba diving",
        },
        {
            "name": "Chiang Mai",
            "experience": "Hills and Nature",
            "tagline": "Historic mountainous northern hub with 300+ Buddhist temples and ethical elephant sanctuaries.",
            "best_season": "Oct to Feb",
            "highlights": "Doi Suthep, Old City temples, Sunday Night Market, Elephant Nature Park",
        },
        {
            "name": "Pattaya",
            "experience": "Beach",
            "tagline": "Lively coastal resort town famed for water sports, coral island tours, and nightlife.",
            "best_season": "Nov to Mar",
            "highlights": "Coral Island (Koh Larn), Sanctuary of Truth, Walking Street, water parks",
        },
        {
            "name": "Krabi",
            "experience": "Adventure",
            "tagline": "Dramatic sheer limestone cliffs, turquoise lagoons, and world-class rock climbing.",
            "best_season": "Nov to Apr",
            "highlights": "Railay Beach, Four Islands boat tour, Emerald Pool, Tiger Cave Temple",
        },
        {
            "name": "Koh Samui",
            "experience": "Beach",
            "tagline": "Palm-fringed island with luxury beachfront resorts, coconut groves, and vibrant nightlife.",
            "best_season": "Dec to Apr",
            "highlights": "Chaweng Beach, Ang Thong Marine Park, Fisherman's Village Bophut",
        },
    ],
    "Japan": [
        {
            "name": "Tokyo",
            "experience": "City and Culture",
            "tagline": "Ultramodern neon metropolis seamlessly blending futuristic technology with historic temples.",
            "best_season": "Mar to May & Sep to Nov",
            "highlights": "Shibuya Crossing, Senso-ji, Akihabara, teamLab digital art, Shinjuku",
        },
        {
            "name": "Kyoto",
            "experience": "Historical",
            "tagline": "Ancient imperial capital with thousands of classical Buddhist temples, gardens, and geisha districts.",
            "best_season": "Mar to May & Oct to Nov",
            "highlights": "Fushimi Inari shrine, Arashiyama Bamboo Grove, Kinkaku-ji Golden Pavilion",
        },
        {
            "name": "Osaka",
            "experience": "City and Culture",
            "tagline": "Japan's lively culinary capital famous for energetic nightlife, street food, and Osaka Castle.",
            "best_season": "Mar to May & Oct to Nov",
            "highlights": "Dotonbori food district, Osaka Castle, Universal Studios Japan",
        },
        {
            "name": "Hokkaido / Sapporo",
            "experience": "Hills and Nature",
            "tagline": "Wild northern island renowned for pristine national parks, onsen hot springs, and ski resorts.",
            "best_season": "Dec to Feb (Snow) or Jul to Aug",
            "highlights": "Sapporo Snow Festival, Niseko skiing, Otaru canal, Lake Toya onsen",
        },
    ],
    "United Arab Emirates": [
        {
            "name": "Dubai",
            "experience": "City and Culture",
            "tagline": "Futuristic skyline with world-record skyscrapers, luxury shopping, and desert safari adventures.",
            "best_season": "Nov to Mar",
            "highlights": "Burj Khalifa, Dubai Mall, Desert Safari, Palm Jumeirah, Marina cruise",
        },
        {
            "name": "Abu Dhabi",
            "experience": "Historical",
            "tagline": "Magnificent capital city boasting grand Islamic architecture, world-class art, and Yas Island.",
            "best_season": "Nov to Mar",
            "highlights": "Sheikh Zayed Grand Mosque, Louvre Abu Dhabi, Ferrari World, Corniche",
        },
        {
            "name": "Sharjah",
            "experience": "City and Culture",
            "tagline": "The UNESCO Cultural Capital of the Arab World with rich heritage souks and art museums.",
            "best_season": "Nov to Mar",
            "highlights": "Heart of Sharjah, Islamic Civilization Museum, Al Majaz Waterfront",
        },
    ],
    "Singapore": [
        {
            "name": "Singapore City / Marina Bay",
            "experience": "City and Culture",
            "tagline": "Futuristic city-in-a-garden featuring iconic supertrees, world-class dining, and diverse heritage.",
            "best_season": "Year-round",
            "highlights": "Gardens by the Bay, Marina Bay Sands SkyPark, Chinatown, Sentosa Island",
        },
        {
            "name": "Sentosa Island",
            "experience": "Beach",
            "tagline": "Premier island resort getaway with golden beaches, Universal Studios, and coastal entertainment.",
            "best_season": "Year-round",
            "highlights": "Universal Studios Singapore, S.E.A. Aquarium, Siloso Beach, Cable Car",
        },
    ],
    "Malaysia": [
        {
            "name": "Kuala Lumpur",
            "experience": "City and Culture",
            "tagline": "Dynamic multicultural capital known for gleaming skyscrapers, colonial architecture, and street markets.",
            "best_season": "Year-round",
            "highlights": "Petronas Twin Towers, Batu Caves, Bukit Bintang, Jalan Alor food street",
        },
        {
            "name": "Penang (George Town)",
            "experience": "Historical",
            "tagline": "UNESCO World Heritage city famous for historic shophouses, street art murals, and Asia's best food.",
            "best_season": "Nov to Apr",
            "highlights": "Street art trail, Penang Hill, Kek Lok Si Temple, street food stalls",
        },
        {
            "name": "Langkawi",
            "experience": "Beach",
            "tagline": "Stunning tropical archipelago of 99 islands with duty-free shopping, mangroves, and sky bridges.",
            "best_season": "Nov to Apr",
            "highlights": "Langkawi Sky Bridge & Cable Car, Cenang Beach, Kilim Karst Geoforest",
        },
    ],
    "Indonesia": [
        {
            "name": "Bali (Ubud & Seminyak)",
            "experience": "Hills and Nature",
            "tagline": "Island of the Gods featuring terraced rice fields, spiritual temples, world-class surfing & yoga.",
            "best_season": "Apr to Oct",
            "highlights": "Ubud Monkey Forest, Tegallalang rice terraces, Uluwatu Temple, Seminyak beach",
        },
        {
            "name": "Jakarta",
            "experience": "City and Culture",
            "tagline": "Massive bustling capital blending modern malls, historic Dutch colonial Old Town, and vibrant nightlife.",
            "best_season": "May to Sep",
            "highlights": "Kota Tua (Old Town), National Monument (Monas), Grand Indonesia",
        },
    ],
    "France": [
        {
            "name": "Paris",
            "experience": "City and Culture",
            "tagline": "The City of Light famed for iconic monuments, legendary art museums, haute cuisine, and fashion.",
            "best_season": "Apr to Jun & Sep to Oct",
            "highlights": "Eiffel Tower, Louvre Museum, Notre-Dame, Montmartre, Seine river cruise",
        },
        {
            "name": "Nice (French Riviera)",
            "experience": "Beach",
            "tagline": "Glamorous Mediterranean coastal city with pebble beaches, seaside boulevards, and azure waters.",
            "best_season": "May to Sep",
            "highlights": "Promenade des Anglais, Castle Hill, Old Town (Vieux Nice), day trip to Monaco",
        },
    ],
    "Italy": [
        {
            "name": "Rome",
            "experience": "Historical",
            "tagline": "The Eternal City with nearly 3,000 years of globally influential art, architecture, and ruins.",
            "best_season": "Apr to Jun & Sep to Oct",
            "highlights": "Colosseum, Vatican Museums, Trevi Fountain, Pantheon, Roman Forum",
        },
        {
            "name": "Venice",
            "experience": "City and Culture",
            "tagline": "The magical floating city built on more than 100 small islands separated by canals and bridges.",
            "best_season": "Apr to Jun & Sep to Oct",
            "highlights": "St. Mark's Basilica, Grand Canal gondola ride, Rialto Bridge, Doge's Palace",
        },
        {
            "name": "Florence",
            "experience": "Historical",
            "tagline": "Cradle of the Renaissance, home to world-renowned masterpieces of art and Tuscan gastronomy.",
            "best_season": "Apr to Jun & Sep to Oct",
            "highlights": "Duomo Cathedral, Uffizi Gallery, Ponte Vecchio, Michelangelo's David",
        },
    ],
    "Switzerland": [
        {
            "name": "Zurich",
            "experience": "City and Culture",
            "tagline": "Cosmopolitan lakeside hub blending historic guild houses with contemporary culture and Swiss precision.",
            "best_season": "Jun to Aug & Dec to Feb",
            "highlights": "Lake Zurich, Old Town (Altstadt), Bahnhofstrasse, Uetliberg mountain view",
        },
        {
            "name": "Interlaken / Jungfrau",
            "experience": "Hills and Nature",
            "tagline": "Adventure capital nestled between two alpine lakes beneath towering 4,000 m alpine peaks.",
            "best_season": "May to Sep & Dec to Mar",
            "highlights": "Jungfraujoch (Top of Europe), Grindelwald, Lake Brienz cruise, Lauterbrunnen waterfalls",
        },
    ],
    "Maldives": [
        {
            "name": "Malé & Local Islands (Maafushi)",
            "experience": "Beach",
            "tagline": "Paradise atoll with crystal-clear turquoise lagoons, coral reefs, and overwater bungalows.",
            "best_season": "Nov to Apr",
            "highlights": "Snorkeling with manta rays, sandbank picnics, dolphin sunset cruises, diving",
        },
    ],
    "Vietnam": [
        {
            "name": "Hanoi & Ha Long Bay",
            "experience": "City and Culture",
            "tagline": "Charming thousand-year-old capital with French colonial architecture, vibrant street food & limestone bays.",
            "best_season": "Oct to Apr",
            "highlights": "Ha Long Bay cruise, Old Quarter, Hoan Kiem Lake, railway train street",
        },
        {
            "name": "Da Nang & Hoi An",
            "experience": "Historical",
            "tagline": "Ancient lantern-lit trading port next to modern beach resort city and the Golden Bridge.",
            "best_season": "Feb to May",
            "highlights": "Hoi An Ancient Town, Ba Na Hills Golden Bridge, Marble Mountains, My Khe Beach",
        },
    ],
    "Sri Lanka": [
        {
            "name": "Colombo & Bentota",
            "experience": "Beach",
            "tagline": "Coastal commercial capital and golden beach resorts with water sports and turtle hatcheries.",
            "best_season": "Nov to Apr",
            "highlights": "Galle Face Green, Bentota Beach, Kosgoda Turtle Conservation, Gangaramaya Temple",
        },
        {
            "name": "Kandy & Nuwara Eliya",
            "experience": "Hills and Nature",
            "tagline": "Hill country sacred heritage city, tea plantations, and the world's most scenic train ride.",
            "best_season": "Dec to Apr",
            "highlights": "Temple of the Sacred Tooth Relic, scenic blue train to Ella, tea factories",
        },
    ],
}



if scope == "India":

    country = "India"

    st.sidebar.caption("Selected country: India")

else:

    country = st.sidebar.selectbox(
        "Choose a country",
        countries,
    )

    prev_country = st.session_state.get("last_selected_country")
    if prev_country != country:
        st.session_state["last_selected_country"] = country
        default_city = COUNTRY_DEFAULTS.get(country, "")
        st.session_state["world_search_query"] = default_city
        st.session_state.pop("world_matches", None)


# Traveller type.

travel_type = st.sidebar.selectbox(
    "Who is travelling?",
    ["Solo", "Couple", "Family", "Friends"],
)


if travel_type == "Solo":

    travellers = 1

    st.sidebar.caption("Traveller count: 1 (Solo)")

elif travel_type == "Couple":

    travellers = 2

    st.sidebar.caption("Traveller count: 2 (Couple)")

else:

    travellers = st.sidebar.number_input(
        "Number of travellers",
        min_value=2,
        max_value=50,
        value=4 if travel_type == "Family" else 3,
        step=1,
    )


# Budget.

budget = st.sidebar.number_input(
    "Total group budget (INR)",
    min_value=1000,
    max_value=10000000,
    value=30000,
    step=1000,
)


# Duration.

days = st.sidebar.number_input(
    "Trip duration (days)",
    min_value=1,
    max_value=60,
    value=3,
    step=1,
)


# Experience preference.

preference = st.sidebar.selectbox(
    "Preferred experience",
    [
        "Any",
        "Beach",
        "Hills and Nature",
        "Historical",
        "Adventure",
        "City and Culture",
    ],
)


st.sidebar.divider()

st.sidebar.metric(
    "Budget per person",
    money(budget / travellers),
)

# Live Feasibility Check based on current sidebar inputs
target_country_for_sidebar = "India" if scope == "India" else country
preview_plan = calculate_real_trip_budget(
    destination="Trip",
    country=target_country_for_sidebar,
    days=int(days),
    travellers=int(travellers),
    starting_location=starting_location,
    tier="standard",
)
sidebar_feasibility = analyze_budget_feasibility(budget, preview_plan)

if sidebar_feasibility["status"] == "CRITICAL_DEFICIT":
    st.sidebar.error(
        f"🔴 **Deficit for {target_country_for_sidebar}**  \n"
        f"Realistic need: **{money(preview_plan['estimated_total_cost'])}**  \n"
        f"Shortfall: **{money(sidebar_feasibility['shortfall'])}**"
    )
elif sidebar_feasibility["status"] == "TIGHT":
    st.sidebar.warning(
        f"🟡 **Tight Budget for {target_country_for_sidebar}**  \n"
        f"Covers ~{sidebar_feasibility['coverage_pct']:.0f}% of standard costs. Hostel/backpacker mode suggested."
    )
else:
    st.sidebar.success(
        f"🟢 **Budget Feasible for {target_country_for_sidebar}**  \n"
        f"Realistic cost: ~{money(preview_plan['estimated_total_cost'])}"
    )

st.sidebar.caption(
    f"Starting from {starting_location} · {days} day(s)"
)



# ============================================================
# 8. NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Navigate",
    [
        "🌍 Destination Recommendations",
        "🧳 My Trip Package",
        "💰 Budget Planner",
    ],
)


# ============================================================
# PAGE 1: DESTINATION RECOMMENDATIONS
# ============================================================

if page == "🌍 Destination Recommendations":

    st.subheader("Find Your Next Destination")

    st.write(
        f"**Trip profile:** {starting_location} → "
        f"{scope} · {travel_type} · "
        f"{travellers} traveller(s) · "
        f"{days} day(s) · {money(budget)} total"
    )


    # --------------------------------------------------------
    # INDIA RECOMMENDATIONS
    # --------------------------------------------------------

    if scope == "India":

        st.info(
            "Indian recommendations use your existing "
            "cleaned destination dataset and ML model."
        )

        if st.button(
            "✨ Recommend Indian Destinations",
            type="primary",
        ):

            try:

                with st.spinner(
                    "Finding destinations that match your trip..."
                ):

                    df, vectorizer, feature_matrix = (
                        load_india_model()
                    )

                    results = recommend_destinations(
                        df,
                        vectorizer,
                        feature_matrix,
                        budget,
                        days,
                        travellers,
                        travel_type,
                        preference,
                        top_n=10,
                    )


                if results is None or results.empty:

                    st.session_state.pop(
                        "india_recommendations",
                        None,
                    )

                    st.warning(
                        "No destinations matched your current "
                        "budget and duration. Try adjusting "
                        "your budget, duration, or preferences."
                    )

                else:

                    results = results.copy()

                    results[
                        "Estimated group cost (INR)"
                    ] = (
                        pd.to_numeric(
                            results["estimated_daily_budget"],
                            errors="coerce",
                        )
                        * days
                        * travellers
                    )

                    results[
                        "Budget remaining (INR)"
                    ] = (
                        budget
                        - results["Estimated group cost (INR)"]
                    )

                    st.session_state[
                        "india_recommendations"
                    ] = results

            except Exception as error:

                st.error(
                    "Could not generate recommendations. "
                    "Check your dataset and recommendation_model.py."
                )

                st.exception(error)


        results = st.session_state.get(
            "india_recommendations"
        )


        if isinstance(results, pd.DataFrame) and not results.empty:

            st.markdown("### Recommended Destinations")

            for index, row in results.iterrows():

                destination_name = str(
                    row.get("destination", "Destination")
                )

                state_name = str(
                    row.get("state", "India")
                )

                description = str(
                    row.get(
                        "description",
                        "Details not available.",
                    )
                )

                cost = row.get(
                    "Estimated group cost (INR)",
                    None,
                )

                remaining = row.get(
                    "Budget remaining (INR)",
                    None,
                )


                with st.container(border=True):

                    left, right = st.columns([3, 1])

                    with left:

                        st.markdown(
                            f"### 📍 {destination_name}, {state_name}"
                        )

                        st.write(description)

                        st.caption(
                            f"Category: {row.get('category', 'Not specified')} "
                            f"· Best season: {row.get('best_season', 'Not specified')} "
                            f"· Minimum suggested stay: "
                            f"{row.get('minimum_days', 'N/A')} day(s)"
                        )

                    with right:

                        if pd.notna(cost):

                            st.metric(
                                "Estimated group cost",
                                money(cost),
                            )

                        if pd.notna(remaining):

                            st.metric(
                                "Budget remaining",
                                money(remaining),
                            )

                        if st.button(
                            "Choose Destination",
                            key=f"choose_india_{index}",
                        ):

                            save_package(
                                destination_name,
                                state_name,
                                description,
                            )

                            st.success(
                                f"{destination_name} saved! "
                                "Open My Trip Package."
                            )


            st.caption(
                "These estimates use the dataset's daily budget "
                "field. Actual transport, accommodation, and "
                "booking charges may differ."
            )


    # --------------------------------------------------------
    # WORLDWIDE DESTINATIONS & POPULAR OPTIONS
    # --------------------------------------------------------

    else:
        popular_destinations = POPULAR_WORLDWIDE_DESTINATIONS.get(country, [])

        st.markdown(f"### 🌴 Top Destinations in {country}")
        st.write(
            f"Here are the top-rated travel destinations in **{country}** for "
            f"**{travellers} traveller(s)** ({days} day(s) from {starting_location}):"
        )

        if popular_destinations:
            # 1. Quick Destination Selection Pills
            pill_names = [d["name"] for d in popular_destinations]
            st.markdown("**⚡ Quick Pick a Destination:**")
            
            selected_pill = st.pills(
                "Popular destinations in " + country,
                pill_names,
                key=f"world_pill_{country}",
                label_visibility="collapsed",
            )
            
            if selected_pill:
                matching_d = next((d for d in popular_destinations if d["name"] == selected_pill), None)
                if matching_d:
                    save_package(matching_d["name"], country, matching_d["tagline"])
                    st.session_state["world_search_query"] = matching_d["name"]
                    st.info(f"✅ Selected **{matching_d['name']}, {country}**! Switch to **🧳 My Trip Package** to see the custom itinerary & budget.")

            # 2. Rich Cards for All Popular Destinations
            for idx, dest_info in enumerate(popular_destinations):
                # Calculate real budget benchmark for this destination
                dest_cost_plan = calculate_real_trip_budget(
                    destination=dest_info["name"],
                    country=country,
                    days=int(days),
                    travellers=int(travellers),
                    starting_location=starting_location,
                    tier="standard",
                )
                dest_feas = analyze_budget_feasibility(budget, dest_cost_plan)

                with st.container(border=True):
                    card_left, card_right = st.columns([3, 1])

                    with card_left:
                        st.markdown(f"### 📍 {dest_info['name']}, {country}")
                        st.write(dest_info["tagline"])
                        st.caption(
                            f"✨ **Highlights:** {dest_info.get('highlights', 'Attractions & sightseeing')}  \n"
                            f"🏷️ **Experience:** {dest_info.get('experience', 'Leisure')} · "
                            f"☀️ **Best Season:** {dest_info.get('best_season', 'Year-round')}"
                        )

                    with card_right:
                        st.metric(
                            "Realistic Trip Cost",
                            money(dest_cost_plan["estimated_total_cost"]),
                            f"{money(dest_cost_plan['cost_per_person'])}/person",
                        )
                        if dest_feas["status"] == "CRITICAL_DEFICIT":
                            st.error(f"🚨 Shortfall: {money(dest_feas['shortfall'])}")
                        elif dest_feas["status"] == "TIGHT":
                            st.warning(f"🟡 Tight: {dest_feas['coverage_pct']:.0f}% funded")
                        else:
                            st.success(f"🟢 Within Budget (Save {money(abs(dest_feas['shortfall']))})")

                        if st.button(
                            f"Choose {dest_info['name']}",
                            key=f"choose_world_{idx}",
                            type="primary",
                        ):
                            save_package(
                                dest_info["name"],
                                country,
                                dest_info["tagline"],
                            )
                            st.session_state["world_search_query"] = dest_info["name"]
                            st.success(f"Saved {dest_info['name']}! Open 🧳 My Trip Package.")
                            st.rerun()

        # ----------------------------------------------------
        # SEARCH ANY OTHER DESTINATION
        # ----------------------------------------------------
        st.markdown("---")
        st.markdown(f"### 🔍 Search Any Other City in {country}")
        st.caption("Looking for a specific offbeat town or beach? Search live worldwide geocoding data:")

        with st.form("world_destination_search_form"):

            default_query = st.session_state.get(
                "world_search_query",
                COUNTRY_DEFAULTS.get(country, "Bangkok" if country == "Thailand" else "Tokyo" if country == "Japan" else "")
            )

            world_query = st.text_input(
                "Enter a city or destination",
                value=default_query,
                placeholder=f"For example, {COUNTRY_DEFAULTS.get(country, 'Paris')}, Phuket, or Pattaya",
            )

            search_clicked = st.form_submit_button(
                "🔎 Search Destinations",
                type="primary",
            )


        if search_clicked:

            if not world_query.strip():

                st.warning(
                    "Enter a destination to search."
                )

            else:

                try:

                    with st.spinner(
                        "Searching worldwide location data..."
                    ):

                        matches = search_destination(
                            world_query.strip(),
                            country,
                        )

                    if not matches:

                        st.warning(
                            "No matching location found. "
                            "Check the spelling or try another destination."
                        )

                        st.session_state.pop(
                            "world_matches",
                            None,
                        )

                    else:

                        st.session_state["world_matches"] = matches

                        st.session_state[
                            "world_search_query"
                        ] = world_query.strip()

                except Exception as error:

                    st.error(
                        "Worldwide search failed. "
                        "Check live_data.py and your internet connection."
                    )

                    st.exception(error)


        matches = st.session_state.get(
            "world_matches",
            [],
        )


        if matches:

            st.markdown("### Matching Locations")

            labels = [
                f"{item.get('name', 'Unknown')}, "
                f"{item.get('country', country)}"
                for item in matches
            ]

            selected_label = st.selectbox(
                "Choose the correct location",
                labels,
                key="world_match_selection",
            )

            chosen = matches[
                labels.index(selected_label)
            ]


            st.caption(
                f"Coordinates: "
                f"{chosen.get('latitude', 'N/A')}, "
                f"{chosen.get('longitude', 'N/A')}"
            )


            if st.button(
                "Choose This Destination",
                type="primary",
                key="save_world_destination",
            ):

                save_package(
                    str(
                        chosen.get(
                            "name",
                            selected_label.split(",")[0],
                        )
                    ),
                    str(
                        chosen.get(
                            "country",
                            country,
                        )
                    ),
                )

                st.success(
                    "Destination saved! Open My Trip Package "
                    "to build your itinerary and check the weather."
                )


            st.caption(
                "Location search does not confirm tourist quality, "
                "live prices, opening hours, or suitability for "
                "your travel dates."
            )


# ============================================================
# PAGE 2: MY TRIP PACKAGE
# ============================================================

elif page == "🧳 My Trip Package":

    st.subheader("Build Your Trip Package")


    saved_destination = st.session_state.get(
        "package_destination",
        "",
    )

    saved_country = st.session_state.get(
        "package_country",
        country,
    )


    with st.form("trip_package_form"):

        package_destination = st.text_input(
            "Destination",
            value=saved_destination,
            placeholder="Select a destination or enter one",
        )

        package_country = st.text_input(
            "Destination country",
            value=saved_country,
        )

        generate_package = st.form_submit_button(
            "🧳 Build My Trip Package",
            type="primary",
        )


    if generate_package:

        if not package_destination.strip():

            st.warning(
                "Choose a destination or enter one first."
            )

        elif not package_country.strip():

            st.warning(
                "Enter the destination country."
            )

        else:

            new_destination = package_destination.strip()
            new_country = package_country.strip()

            old_destination = st.session_state.get(
                "active_package_destination"
            )

            old_country = st.session_state.get(
                "active_package_country"
            )

            if (
                new_destination != old_destination
                or new_country != old_country
            ):

                st.session_state.pop(
                    "package_weather",
                    None,
                )

                st.session_state.pop(
                    "package_weather_error",
                    None,
                )

            if check_is_domestic(new_destination, new_country):
                new_country = "India"

            st.session_state[
                "active_package_destination"
            ] = new_destination

            st.session_state[
                "active_package_country"
            ] = new_country

            st.session_state[
                "active_package_profile"
            ] = {
                "starting_location": starting_location,
                "travellers": int(travellers),
                "travel_type": travel_type,
                "budget": float(budget),
                "days": int(days),
                "preference": preference,
            }


    active_destination = st.session_state.get(
        "active_package_destination"
    )

    active_country = st.session_state.get(
        "active_package_country",
        "",
    )
    if check_is_domestic(active_destination, active_country):
        active_country = "India" 

    profile = st.session_state.get(
        "active_package_profile"
    )


    if active_destination and profile:

        st.markdown(
            f"## 📍 {active_destination}, {active_country}"
        )

        st.write(
            f"**Route:** {profile['starting_location']} → "
            f"{active_destination}, {active_country}  \n"
            f"**Travellers:** {profile['travel_type']} "
            f"({profile['travellers']}) · "
            f"**Duration:** {profile['days']} day(s)"
        )


        # ----------------------------------------------------
        # WEATHER
        # ----------------------------------------------------

        st.markdown("### 🌦️ Destination Weather")

        if st.button(
            "Get Latest Available Weather",
            key="package_weather_btn",
        ):

            try:

                with st.spinner(
                    "Getting weather information..."
                ):

                    weather = get_destination_weather(
                        active_destination,
                        active_country,
                    )


                if (
                    not isinstance(weather, dict)
                    or weather.get("error")
                ):

                    error_message = (
                        weather.get(
                            "error",
                            "Weather data is unavailable.",
                        )
                        if isinstance(weather, dict)
                        else "Weather data is unavailable."
                    )

                    st.session_state[
                        "package_weather_error"
                    ] = error_message

                    st.session_state.pop(
                        "package_weather",
                        None,
                    )

                else:

                    st.session_state[
                        "package_weather"
                    ] = weather

                    st.session_state.pop(
                        "package_weather_error",
                        None,
                    )

            except Exception as error:

                st.session_state[
                    "package_weather_error"
                ] = str(error)


        if st.session_state.get(
            "package_weather_error"
        ):

            st.warning(
                st.session_state[
                    "package_weather_error"
                ]
            )


        weather = st.session_state.get(
            "package_weather"
        )


        if weather and not weather.get("error"):

            current = weather.get(
                "current_weather",
                {},
            )

            daily = weather.get(
                "daily_forecast",
                {},
            )

            rain_values = [
                value
                for value in daily.get(
                    "precipitation_probability_max",
                    [],
                )
                if isinstance(value, (int, float))
            ]


            m1, m2, m3 = st.columns(3)

            temp = current.get("temperature_2m")
            wind = current.get("wind_speed_10m")


            m1.metric(
                "Temperature",
                f"{temp} °C"
                if temp is not None
                else "Unavailable",
            )

            m2.metric(
                "Wind Speed",
                f"{wind} km/h"
                if wind is not None
                else "Unavailable",
            )

            m3.metric(
                "Highest Forecast Rain Chance",
                f"{max(rain_values)}%"
                if rain_values
                else "Unavailable",
            )


            dates = daily.get("time", [])

            probs = daily.get(
                "precipitation_probability_max",
                [],
            )


            if dates and probs:

                weather_df = pd.DataFrame({
                    "Date": dates[:len(probs)],
                    "Rain probability (%)": probs[:len(dates)],
                })

                st.dataframe(
                    weather_df,
                    use_container_width=True,
                    hide_index=True,
                )


            try:

                advice = get_travel_advice(weather)

                if advice:
                    st.info(advice)

            except Exception:

                st.caption(
                    "Additional travel advice is unavailable."
                )


            st.caption(
                "Weather guidance is not a guarantee of conditions "
                "on your travel dates. Check official local alerts "
                "before travelling."
            )


        else:

            st.caption(
                "Press Get Latest Available Weather to retrieve "
                "weather data for your destination."
            )


        # ----------------------------------------------------
        # REAL-WORLD BUDGET ESTIMATE & FEASIBILITY ANALYSIS
        # ----------------------------------------------------

        st.markdown("### 💰 Estimated Budget Breakdown & Feasibility Analysis")

        package_budget = float(profile["budget"])
        package_travellers = int(profile["travellers"])
        package_days = int(profile["days"])

        tier_col, trans_col = st.columns([1, 1])
        with tier_col:
            selected_tier = st.radio(
                "🏨 Travel Style & Hotel Standard:",
                ["Standard (3-Star Private Hotel)", "Backpacker (Budget Hostel / Capsule)"],
                horizontal=False,
                key="pkg_tier_select",
            )
        calc_tier = "standard" if "Standard" in selected_tier else "budget"

        # Pre-fetch multiple available transport options for this route
        pkg_avail_transport = get_transport_options(
            destination=active_destination,
            country=active_country,
            starting_location=profile.get("starting_location", "Malappuram, Kerala"),
            travellers=package_travellers,
        )
        pkg_t_labels = [
            f"{opt['name']} — ₹{opt['cost_per_person']:,.0f}/person ({opt['duration']})"
            for opt in pkg_avail_transport
        ]
        pkg_rec_idx = next((i for i, opt in enumerate(pkg_avail_transport) if opt.get("recommended")), 0)

        with trans_col:
            selected_pkg_t_idx = st.selectbox(
                "🚗 Available Transportation Options:",
                range(len(pkg_avail_transport)),
                format_func=lambda i: pkg_t_labels[i],
                index=pkg_rec_idx,
                key="pkg_transport_select",
                help="Select your preferred mode of travel to calculate accurate transit costs.",
            )
        chosen_pkg_trans_id = pkg_avail_transport[selected_pkg_t_idx]["id"]

        # Calculate authentic real-world benchmark plan with selected transport
        real_plan = calculate_real_trip_budget(
            destination=active_destination,
            country=active_country,
            days=package_days,
            travellers=package_travellers,
            starting_location=profile.get("starting_location", "Malappuram, Kerala"),
            tier=calc_tier,
            transport_mode_id=chosen_pkg_trans_id,
        )

        # Analyze feasibility of user budget vs real costs
        feasibility = analyze_budget_feasibility(package_budget, real_plan)

        # 1. Feasibility Alert Banner
        if feasibility["status"] == "CRITICAL_DEFICIT":
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.22), rgba(127, 29, 29, 0.45)); border: 1.5px solid #ef4444; border-radius: 14px; padding: 18px 22px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        <span style="font-size: 1.6rem;">🚨</span>
                        <h3 style="color: #fca5a5; margin: 0; font-size: 1.3rem;">Trip Infeasible with {money(package_budget)}: Critical Budget Deficit for {active_destination}, {active_country}</h3>
                    </div>
                    <p style="color: #fecaca; margin-bottom: 12px; font-size: 0.98rem; line-height: 1.55;">
                        {feasibility['summary']}
                    </p>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                        <span style="background: rgba(239, 68, 68, 0.35); border: 1px solid #f87171; color: #ffffff; padding: 4px 12px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">
                            ✈️ Return Flights Alone: {money(real_plan['total_flights'])} ({feasibility['flights_share_of_user_budget']:.0f}% of your budget)
                        </span>
                        <span style="background: rgba(239, 68, 68, 0.35); border: 1px solid #f87171; color: #ffffff; padding: 4px 12px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">
                            🏨 Realistic Market Total: {money(real_plan['estimated_total_cost'])}
                        </span>
                        <span style="background: rgba(239, 68, 68, 0.35); border: 1px solid #f87171; color: #ffffff; padding: 4px 12px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">
                            📉 Deficit: {money(feasibility['shortfall'])} (Covers only {feasibility['coverage_pct']:.0f}%)
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif feasibility["status"] == "TIGHT":
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.22), rgba(180, 83, 9, 0.4)); border: 1.5px solid #f59e0b; border-radius: 14px; padding: 18px 22px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        <span style="font-size: 1.6rem;">🟡</span>
                        <h3 style="color: #fde68a; margin: 0; font-size: 1.3rem;">Budget is Tight for {active_destination}, {active_country}</h3>
                    </div>
                    <p style="color: #fef3c7; margin-bottom: 12px; font-size: 0.98rem; line-height: 1.55;">
                        {feasibility['summary']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.22), rgba(4, 120, 87, 0.4)); border: 1.5px solid #10b981; border-radius: 14px; padding: 18px 22px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        <span style="font-size: 1.6rem;">🟢</span>
                        <h3 style="color: #a7f3d0; margin: 0; font-size: 1.3rem;">Budget Feasible & Well-Covered for {active_destination}, {active_country}</h3>
                    </div>
                    <p style="color: #d1fae5; margin-bottom: 12px; font-size: 0.98rem; line-height: 1.55;">
                        {feasibility['summary']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 2. Key Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(
            "Your Allocated Budget",
            money(package_budget),
            f"{money(package_budget / package_travellers)}/person",
        )
        m2.metric(
            "Realistic Market Cost",
            money(real_plan["estimated_total_cost"]),
            f"{money(real_plan['cost_per_person'])}/person",
        )
        shortfall_val = feasibility["shortfall"]
        m3.metric(
            "Budget Difference",
            f"{'-' if shortfall_val > 0 else '+'}{money(abs(shortfall_val))}",
            f"{feasibility['coverage_pct']:.0f}% funded",
            delta_color="normal" if shortfall_val <= 0 else "inverse",
        )
        m4.metric(
            "Suggested Rooms",
            f"{real_plan['rooms']} room(s)",
            f"{real_plan['nights']} night(s) stay",
        )

        # 3. Interactive Budget Explorer Tabs
        tab_real, tab_compare, tab_intl_vs_dom, tab_alternatives = st.tabs([
            "📋 Real Market Cost Breakdown",
            "⚖️ Your Budget vs Real Cost Comparison",
            "🌏 International vs India Cost Explainer",
            "💡 What ₹30,000 Can Afford Instead",
        ])

        with tab_real:
            real_df = get_real_budget_dataframe(real_plan)
            st.dataframe(
                real_df,
                use_container_width=True,
                hide_index=True,
            )

            # Chart of authentic expenses
            chart_col = "Estimated Amount (INR)" if "Estimated Amount (INR)" in real_df.columns else "Estimated amount (INR)"
            chart_data = real_df.set_index("Expense Item")[chart_col]
            st.bar_chart(chart_data)

            st.caption(
                f"📌 Real Benchmark Data: International airfares departing from Kerala/South India, "
                f"official visa & mandatory insurance fees, standard accommodations, and local living costs "
                f"denominated in {real_plan['currency_code']} ({real_plan['currency_symbol']}) and converted to INR."
            )

        with tab_compare:
            st.markdown(
                "#### How Naive Flat Percentages Fail vs Real-World Market Costs"
            )
            st.write(
                "A naive percentage formula (e.g. 30% transport, 30% accommodation) blindly allocates "
                f"{money(package_budget)} as ₹{round(package_budget * 0.30):,.0f} for transport and "
                f"₹{round(package_budget * 0.30):,.0f} for hotel. In reality, flights to {active_country} "
                f"cost **{money(real_plan['total_flights'])}** and hotels cost **{money(real_plan['total_accommodation'])}**!"
            )
            comp_df = get_budget_comparison_dataframe(package_budget, real_plan)
            st.dataframe(comp_df, use_container_width=True, hide_index=True)

        with tab_intl_vs_dom:
            st.markdown("#### 🌏 Why International Trips Cost Drastically More Than Travel in India")
            st.write(
                "You asked: *'Are accommodation, food, and transport the same for an international trip and in India?'*  \n\n"
                "**No, they are vastly different.** Look at the real-data comparison below between "
                f"a 5-day trip to **{active_destination}, {active_country}** vs **Goa, India**:"
            )
            vs_data = get_international_vs_domestic_comparison(
                days=package_days,
                travellers=package_travellers,
                intl_destination=active_destination,
                intl_country=active_country,
                domestic_destination="Goa",
            )
            st.dataframe(pd.DataFrame(vs_data["rows"]), use_container_width=True, hide_index=True)

            st.info(
                f"💡 **Key Takeaway**: A trip to {active_destination}, {active_country} costs approximately "
                f"**{vs_data['ratio']}x more** than a domestic trip in India. Roundtrip international flights, "
                "foreign currency purchasing power, higher real estate costs, and visa/insurance fees account "
                "for the vast majority of this difference."
            )

        with tab_alternatives:
            st.markdown("#### 💡 Destinations You Can Comfortably Afford with ₹30,000")
            if not real_plan["is_domestic"] and feasibility["status"] == "CRITICAL_DEFICIT":
                st.write(
                    f"While **₹30,000** cannot cover an international trip to **{active_destination}, {active_country}** "
                    "(where return flights alone exceed your budget), ₹30,000 is an **exceptional budget** for domestic travel across India!"
                )
            else:
                st.write("Top destinations matching your budget:")

            alt_list = get_alternative_destinations(package_budget, package_days, package_travellers)
            if alt_list:
                cols = st.columns(len(alt_list))
                for i, alt in enumerate(alt_list):
                    with cols[i]:
                        with st.container(border=True):
                            st.markdown(f"**📍 {alt['destination']}**")
                            st.caption(alt["region"])
                            st.write(f"Est. 5-Day Cost: **{money(alt['estimated_cost'])}**")
                            if alt["budget_surplus"] > 0:
                                st.success(f"Save {money(alt['budget_surplus'])}")
                            else:
                                st.info("Exact match")
                            if st.button(f"Choose {alt['destination']}", key=f"btn_alt_{i}"):
                                save_package(alt["destination"], "India", f"Scenic holiday in {alt['region']}")
                                st.rerun()

            st.markdown("---")
            st.markdown(f"**Thinking of travelling to {active_country} in the future?**")
            st.write(
                f"To travel comfortably to {active_country} for {package_days} days, "
                f"we recommend saving a target budget of approximately **{money(real_plan['estimated_total_cost'])}** "
                f"({money(real_plan['cost_per_person'])} per traveller)."
            )



        # ────────────────────────────────────────────────────────────────
        # DETAILED DAY-BY-DAY ITINERARY
        # ────────────────────────────────────────────────────────────────
        st.markdown("### 🗓️ Day-by-Day Itinerary")

        itinerary_days = create_detailed_itinerary(
            active_destination,
            profile["days"],
            profile["preference"],
        )

        for day_info in itinerary_days:
            with st.expander(
                f"📅 Day {day_info['day']} — {day_info['theme']}",
                expanded=(day_info["day"] == 1),
            ):
                col_m, col_a, col_e = st.columns(3)
                with col_m:
                    st.markdown("**🌅 Morning**")
                    st.write(day_info["morning"])
                with col_a:
                    st.markdown("**☀️ Afternoon**")
                    st.write(day_info["afternoon"])
                with col_e:
                    st.markdown("**🌙 Evening**")
                    st.write(day_info["evening"])
                st.markdown("---")
                info_c1, info_c2, info_c3 = st.columns(3)
                info_c1.info(f"🍽️ **Food Tip:** {day_info['food_tip']}")
                info_c2.metric("Entry Fees Est.", day_info["entry_fee_est"])
                info_c3.metric("Distance from Base", day_info["distance_from_centre"])


        # ────────────────────────────────────────────────────────────────
        # TRANSPORTATION OPTIONS (ALL MODES)
        # ────────────────────────────────────────────────────────────────
        st.markdown(f"### 🚌 How to Get to {active_destination}")
        st.caption(
            f"Available travel modes from **{profile['starting_location']}** for "
            f"**{package_travellers} traveller(s)** · Roundtrip cost estimates")

        transport_opts = real_plan.get("available_transport_options", [])
        sel_transport   = real_plan.get("selected_transport_option", {})
        own_veh         = real_plan.get("own_vehicle_feasibility", {})

        if transport_opts:
            # Show mode cards
            t_cols = st.columns(min(len(transport_opts), 4))
            for idx, opt in enumerate(transport_opts[:4]):
                with t_cols[idx]:
                    is_active = (opt["id"] == sel_transport.get("id"))
                    with st.container(border=True):
                        if is_active:
                            st.success("📌 Used in Budget Calc")
                        elif opt.get("recommended"):
                            st.info("💡 Recommended")
                        st.markdown(f"**{opt['name']}**")
                        st.markdown(f"#### ₹{opt['cost_per_person']:,.0f}")
                        st.caption(f"per person &nbsp;|&nbsp; ₹{opt['total_cost']:,.0f} group total")
                        st.write(f"⏱️ {opt['duration']}")
                        st.write(f"✅ {opt['pros']}")
                        st.caption(f"📌 {opt['notes']}")

            if len(transport_opts) > 4:
                with st.expander(f"🔽 See {len(transport_opts) - 4} more transport option(s)"):
                    for opt in transport_opts[4:]:
                        st.markdown(
                            f"**{opt['name']}** &nbsp;—&nbsp; "
                            f"₹{opt['cost_per_person']:,.0f}/person &nbsp;|&nbsp; {opt['duration']}")
                        st.caption(opt["notes"])

        # ── OWN VEHICLE PANEL ────────────────────────────────────────────
        st.markdown("#### 🏎️ Can I Use My Own Vehicle?")
        if own_veh:
            badge_color = own_veh.get("badge_color", "#6b7280")
            badge_icon  = own_veh.get("badge_icon", "ℹ️")
            verdict     = own_veh.get("verdict", "")
            summary     = own_veh.get("summary", "")

            # Coloured verdict banner
            banner_html = (
                f'<div style="background:{badge_color}22; border:1.5px solid {badge_color}; '
                f'border-radius:10px; padding:12px 16px; margin-bottom:10px;">'
                f'<span style="font-size:1.1rem; font-weight:700; color:{badge_color};">'
                f'{badge_icon} {verdict}</span><br/>'
                f'<span style="color:#e5e7eb; font-size:0.93rem;">{summary}</span>'
                f'</div>'
            )
            st.markdown(banner_html, unsafe_allow_html=True)

            if own_veh.get("possible") and own_veh.get("distance_km"):
                ov1, ov2, ov3 = st.columns(3)
                ov1.metric("📍 Distance", f"{own_veh['distance_km']} km", "Roundtrip")
                ov2.metric("⏱️ Drive Time", own_veh["duration"])
                ov3.metric("⛽ Car Fuel + Tolls",
                           f"₹{own_veh['total_car_cost']:,}",
                           f"₹{own_veh['cost_per_person_car']:,}/person")

                with st.expander("🗺️ Route & Road Tips"):
                    st.markdown(f"**🛣️ Highway Route:**  \n`{own_veh['highway']}`")
                    if own_veh.get("bike_fuel_roundtrip"):
                        st.markdown(
                            f"**🏍️ Two-Wheeler Cost:** "
                            f"₹{own_veh['bike_fuel_roundtrip']:,} fuel + ₹{round(own_veh['tolls_roundtrip'] * 0.2):,} tolls "
                            f"= **₹{own_veh['cost_per_person_bike']:,}/person** (split between 2 on bike)")
                    tips = own_veh.get("tips", "")
                    if tips:
                        st.markdown("**⚠️ Important Road Safety Tips:**")
                        for tip_line in tips.split("\\n"):
                            tip_line = tip_line.strip()
                            if tip_line:
                                st.markdown(f"• {tip_line}")
            elif not own_veh.get("possible"):
                st.markdown(
                    f"💡 **Alternative:** {own_veh.get('tips', '')}",
                )

        # ────────────────────────────────────────────────────────────────
        # TRAVEL CHECKLIST
        # ────────────────────────────────────────────────────────────────
        st.markdown("### 🧭 Before You Travel")

        col1, col2 = st.columns(2)

        with col1:
            sel_opt = sel_transport or {}
            if sel_opt:
                st.markdown("**📌 Selected Transport Mode**")
                st.write(
                    f"• **Mode:** {sel_opt['name']}  \n"
                    f"• **Cost:** ₹{sel_opt['cost_per_person']:,.0f}/person "
                    f"(Group Total: ₹{sel_opt['total_cost']:,.0f})  \n"
                    f"• **Travel Time:** {sel_opt['duration']}  \n"
                    f"• **Notes:** {sel_opt['notes']}"
                )

            st.markdown("**🏨 Accommodation**")
            suggested_rooms = real_plan.get("rooms", max(1, (package_travellers + 1) // 2))
            st.write(
                f"Plan approximately {suggested_rooms} room(s) if "
                "two travellers share each room. "
                "Actual room requirements vary."
            )


        with col2:

            st.markdown("**🍽️ Food and Local Spots**")

            st.write(
                "Research local restaurants, regional cuisine, "
                "opening hours, and dietary requirements."
            )

            st.markdown("**🎫 Sightseeing and Activities**")

            st.write(
                "Check attraction opening hours, ticket prices, "
                "weather conditions, and activity safety rules."
            )


        st.checkbox(
            "I will verify actual transport, accommodation, "
            "and activity prices before booking.",
            key="verify_prices_check",
        )

        st.checkbox(
            "I will check local alerts, entry requirements, "
            "and attraction opening hours.",
            key="verify_trip_details_check",
        )


    else:

        st.info(
            "Choose a destination on the first page or enter "
            "one above. Then click Build My Trip Package."
        )


# ============================================================
# PAGE 3: BUDGET PLANNER
# ============================================================

else:

    st.subheader("💰 Smart Travel Budget & Feasibility Planner")
    st.write(
        "Analyze realistic travel expenses, compare international vs domestic Indian travel costs, "
        "and determine whether your budget is feasible using real-world market benchmarks."
    )

    # Destination context for Budget Planner
    pkg_dest = st.session_state.get("active_package_destination") or st.session_state.get("package_destination", "Goa")
    pkg_country = st.session_state.get("active_package_country") or ("India" if scope == "India" else country)

    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        planner_country = st.selectbox(
            "Destination Country to Plan For:",
            ["India"] + [c for c in countries if c != "India"],
            index=0 if pkg_country == "India" else (countries.index(pkg_country) + 1 if pkg_country in countries else 0),
            key="bp_country_select",
        )
    with p_col2:
        planner_dest = st.text_input(
            "City / Destination Name:",
            value=pkg_dest if (pkg_country == planner_country or not pkg_dest) else ("Tokyo" if planner_country == "Japan" else "City Centre"),
            key="bp_dest_input",
        )
    bp_avail_transport = get_transport_options(
        destination=planner_dest,
        country=planner_country,
        starting_location=starting_location,
        travellers=int(travellers),
    )
    bp_t_labels = [
        f"{opt['name']} — ₹{opt['cost_per_person']:,.0f}/person ({opt['duration']})"
        for opt in bp_avail_transport
    ]
    bp_rec_idx = next((i for i, opt in enumerate(bp_avail_transport) if opt.get("recommended")), 0)

    with p_col3:
        bp_tier = st.radio(
            "Accommodation Tier:",
            ["Standard (3-Star Hotel)", "Budget / Backpacker (Hostel / Capsule)"],
            horizontal=False,
            key="bp_tier_select",
        )

    calc_bp_tier = "standard" if "Standard" in bp_tier else "budget"

    selected_bp_t_idx = st.selectbox(
        "🚗 Available Transportation Options:",
        range(len(bp_avail_transport)),
        format_func=lambda i: bp_t_labels[i],
        index=bp_rec_idx,
        key="bp_transport_select",
        help="Switch between available flights, trains, buses, and road trips to see how transport affects your budget.",
    )
    chosen_bp_trans_id = bp_avail_transport[selected_bp_t_idx]["id"]

    # Calculate real benchmark
    bp_real_plan = calculate_real_trip_budget(
        destination=planner_dest,
        country=planner_country,
        days=int(days),
        travellers=int(travellers),
        starting_location=starting_location,
        tier=calc_bp_tier,
        transport_mode_id=chosen_bp_trans_id,
    )
    bp_feasibility = analyze_budget_feasibility(budget, bp_real_plan)

    # 1. Feasibility Verdict Banner
    if bp_feasibility["status"] == "CRITICAL_DEFICIT":
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.22), rgba(127, 29, 29, 0.45)); border: 1.5px solid #ef4444; border-radius: 14px; padding: 18px 22px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                    <span style="font-size: 1.6rem;">🚨</span>
                    <h3 style="color: #fca5a5; margin: 0; font-size: 1.3rem;">Trip Infeasible with {money(budget)}: Budget Deficit of {money(bp_feasibility['shortfall'])}</h3>
                </div>
                <p style="color: #fecaca; margin-bottom: 12px; font-size: 0.98rem; line-height: 1.55;">
                    {bp_feasibility['summary']}
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                    <span style="background: rgba(239, 68, 68, 0.35); border: 1px solid #f87171; color: #ffffff; padding: 4px 12px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">
                        ✈️ Flights / Transport Alone: {money(bp_real_plan['total_flights'])}
                    </span>
                    <span style="background: rgba(239, 68, 68, 0.35); border: 1px solid #f87171; color: #ffffff; padding: 4px 12px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">
                        🏨 Realistic Cost: {money(bp_real_plan['estimated_total_cost'])}
                    </span>
                    <span style="background: rgba(239, 68, 68, 0.35); border: 1px solid #f87171; color: #ffffff; padding: 4px 12px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">
                        📉 Funded: {bp_feasibility['coverage_pct']:.0f}%
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif bp_feasibility["status"] == "TIGHT":
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.22), rgba(180, 83, 9, 0.4)); border: 1.5px solid #f59e0b; border-radius: 14px; padding: 18px 22px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                    <span style="font-size: 1.6rem;">🟡</span>
                    <h3 style="color: #fde68a; margin: 0; font-size: 1.3rem;">Budget is Tight for {planner_dest}, {planner_country}</h3>
                </div>
                <p style="color: #fef3c7; margin-bottom: 12px; font-size: 0.98rem; line-height: 1.55;">
                    {bp_feasibility['summary']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.22), rgba(4, 120, 87, 0.4)); border: 1.5px solid #10b981; border-radius: 14px; padding: 18px 22px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                    <span style="font-size: 1.6rem;">🟢</span>
                    <h3 style="color: #a7f3d0; margin: 0; font-size: 1.3rem;">Budget Feasible for {planner_dest}, {planner_country}</h3>
                </div>
                <p style="color: #d1fae5; margin-bottom: 12px; font-size: 0.98rem; line-height: 1.55;">
                    {bp_feasibility['summary']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 2. Comparative Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "Total Group Budget",
        money(budget),
        f"{money(budget / travellers)}/person",
    )
    c2.metric(
        "Realistic Market Need",
        money(bp_real_plan["estimated_total_cost"]),
        f"{money(bp_real_plan['cost_per_person'])}/person",
    )
    bp_shortfall = bp_feasibility["shortfall"]
    c3.metric(
        "Budget Difference",
        f"{'-' if bp_shortfall > 0 else '+'}{money(abs(bp_shortfall))}",
        f"{bp_feasibility['coverage_pct']:.0f}% funded",
        delta_color="normal" if bp_shortfall <= 0 else "inverse",
    )
    c4.metric(
        "Per Day Per Person",
        money(bp_real_plan["cost_per_person_day"]),
        f"{days} day(s) duration",
    )

    # 3. Tabs for Breakdown and Explanations
    bp_tab1, bp_tab2, bp_tab3 = st.tabs([
        "📊 Itemized Real Market Costs",
        "🌏 Why International Trips Cost More Than India",
        "🗺️ International Trip Feasibility Guide (Is ₹30,000 possible?)",
    ])

    with bp_tab1:
        st.markdown(f"### Real-World Expense Breakdown for {planner_dest}, {planner_country}")
        bp_df = get_real_budget_dataframe(bp_real_plan)
        st.dataframe(bp_df, use_container_width=True, hide_index=True)

        st.bar_chart(
            bp_df.set_index("Expense Item")["Estimated Amount (INR)" if "Estimated Amount (INR)" in bp_df.columns else "Estimated amount (INR)"]
        )

    with bp_tab2:
        st.markdown("### 🔍 The Real Cost Difference: International Travel vs India")
        st.write(
            "**Key Insight:** International travel and domestic Indian travel have completely different cost structures. "
            "You cannot apply the same percentages or price expectations to both:"
        )

        intl_example = planner_dest if not bp_real_plan["is_domestic"] else "Tokyo"
        intl_example_country = planner_country if not bp_real_plan["is_domestic"] else "Japan"
        vs_res = get_international_vs_domestic_comparison(
            days=int(days),
            travellers=int(travellers),
            intl_destination=intl_example,
            intl_country=intl_example_country,
            domestic_destination="Goa"
        )
        st.dataframe(pd.DataFrame(vs_res["rows"]), use_container_width=True, hide_index=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**1. The Flight Barrier (Fixed Overhead)**")
            st.write(
                "In India, intercity travel costs ₹1,500 - ₹6,000 (sleeper bus, Vande Bharat/train, or budget domestic flight). "
                f"For {intl_example_country}, international roundtrip flights from Kerala cost **{money(bp_real_plan['total_flights'] if not bp_real_plan['is_domestic'] else 52000)}**, "
                "which alone often exceeds an entire ₹30,000 budget."
            )
            st.markdown("**2. Visa & Mandatory Insurance**")
            st.write(
                "Domestic travel has **₹0** visa and insurance costs. International trips require tourist visa processing fees "
                "(up to ₹12,500 for Schengen/UK/USA, ~₹2,500 for Japan) plus mandatory medical travel insurance."
            )

        with col_b:
            st.markdown("**3. Foreign Currency Purchasing Power**")
            st.write(
                "In India, ₹600 buys 3 hearty meals and snacks. In Japan (where meals are priced in Yen) or Europe (Euros), "
                "a single casual meal costs ₹600 - ₹1,200. Daily basic dining runs ₹2,000 - ₹3,500/day."
            )
            st.markdown("**4. Real Estate & Hotel Pricing**")
            st.write(
                "A clean 3-star hotel room in India is ₹2,000 - ₹3,000/night. In Tokyo, Paris, or London, standard hotel rooms "
                "cost ₹8,000 - ₹14,000/night due to high urban land costs and exchange rates."
            )

    with bp_tab3:
        st.markdown("### ✈️ Where Can ₹30,000 Take You? (Real Data Benchmarks)")
        st.write(
            "Here is the realistic minimum 5-day solo budget required from Kerala/India for popular destinations:"
        )

        guide_rows = [
            {"Destination": "Goa, India", "Scope": "Domestic", "Return Flights/Transit": "₹2,500 - ₹4,000", "5-Day Total (Solo)": "₹18,000 - ₹22,000", "Feasible with ₹30,000?": "🟢 YES (Surplus ₹8,000+)"},
            {"Destination": "Munnar, Kerala", "Scope": "Domestic", "Return Flights/Transit": "₹1,000 - ₹1,500", "5-Day Total (Solo)": "₹14,000 - ₹17,000", "Feasible with ₹30,000?": "🟢 YES (Surplus ₹13,000+)"},
            {"Destination": "Nepal (Kathmandu)", "Scope": "International", "Return Flights/Transit": "₹15,000 - ₹18,000", "5-Day Total (Solo)": "₹28,000 - ₹34,000", "Feasible with ₹30,000?": "🟢 Borderline / Yes (Backpacker)"},
            {"Destination": "Sri Lanka (Colombo)", "Scope": "International", "Return Flights/Transit": "₹14,000 - ₹18,000", "5-Day Total (Solo)": "₹35,000 - ₹42,000", "Feasible with ₹30,000?": "🟡 Tight (Deficit ~₹5k - ₹12k)"},
            {"Destination": "Thailand (Bangkok)", "Scope": "International", "Return Flights/Transit": "₹17,000 - ₹22,000", "5-Day Total (Solo)": "₹38,000 - ₹45,000", "Feasible with ₹30,000?": "🟡 Tight (Deficit ~₹8k - ₹15k)"},
            {"Destination": "Vietnam (Hanoi)", "Scope": "International", "Return Flights/Transit": "₹18,000 - ₹24,000", "5-Day Total (Solo)": "₹40,000 - ₹48,000", "Feasible with ₹30,000?": "🟡 Tight (Deficit ~₹10k - ₹18k)"},
            {"Destination": "Dubai / UAE", "Scope": "International", "Return Flights/Transit": "₹20,000 - ₹26,000", "5-Day Total (Solo)": "₹65,000 - ₹78,000", "Feasible with ₹30,000?": "🔴 NO (Deficit ~₹35k - ₹48k)"},
            {"Destination": "Tokyo, Japan", "Scope": "International", "Return Flights/Transit": "₹48,000 - ₹60,000", "5-Day Total (Solo)": "₹1,15,000 - ₹1,35,000", "Feasible with ₹30,000?": "🔴 NO (Flights alone exceed budget)"},
            {"Destination": "Paris, France", "Scope": "International", "Return Flights/Transit": "₹55,000 - ₹70,000", "5-Day Total (Solo)": "₹1,25,000 - ₹1,50,000", "Feasible with ₹30,000?": "🔴 NO (Deficit ~₹95k+)"},
            {"Destination": "Switzerland", "Scope": "International", "Return Flights/Transit": "₹60,000 - ₹75,000", "5-Day Total (Solo)": "₹1,60,000 - ₹1,90,000", "Feasible with ₹30,000?": "🔴 NO (Deficit ~₹1,30,000+)"},
        ]
        st.dataframe(pd.DataFrame(guide_rows), use_container_width=True, hide_index=True)



# ============================================================
# 9. FOOTER
# ============================================================

st.divider()

st.caption(
    "🌍 Worldwide Smart Travel Planner · Streamlit · "
    "scikit-learn · Open-Meteo · "
    "Costs and itineraries are estimates unless verified "
    "with a provider."
)