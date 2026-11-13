"""
Real-world travel budget benchmarking data and calculation engine.
Provides authentic cost benchmarks for Indian domestic travel and international destinations,
including flight estimates from India (Kerala/major airports), visa fees, accommodation,
food, local transport, and budget feasibility analysis.
"""

import math
from typing import Dict, Any, Optional, Tuple


# Benchmark data for International Countries & Indian Domestic Travel
# All monetary figures are in Indian Rupees (INR).
# Flight prices are roundtrip estimates departing from Kerala / South India / India.
BENCHMARK_DATA: Dict[str, Dict[str, Any]] = {
    # ----------------------------------------------------
    # INDIA (DOMESTIC)
    # ----------------------------------------------------
    "India": {
        "currency_code": "INR",
        "currency_symbol": "₹",
        "country_name": "India",
        "is_international": False,
        "flight_roundtrip_default": 6500,       # Domestic flight (e.g. Kerala to Delhi/Goa)
        "surface_roundtrip_default": 2200,      # Train / intercity bus / car
        "visa_fee": 0,
        "travel_insurance": 0,
        "hotel_standard_per_night": 2500,       # 3-star private room
        "hotel_budget_per_night": 1000,         # Budget guesthouse / hostel dorm
        "food_daily_per_person": 600,           # Breakfast, lunch, dinner + tea
        "local_transport_daily_per_person": 500,# Auto, metro, local taxis
        "activities_daily_per_person": 400,     # Monument entry, boat rides, sightseeing
        "daily_cost_tier": "Domestic Economical",
        "description": "No international flights or visas required. Highly affordable daily living and transit costs.",
        # City overrides
        "destinations": {
            "Munnar": {"hotel_standard": 2500, "hotel_budget": 1200, "food": 500, "transport": 600, "activities": 300, "transit_from_kerala": 1200},
            "Alleppey": {"hotel_standard": 2800, "hotel_budget": 1200, "food": 550, "transport": 500, "activities": 600, "transit_from_kerala": 1000},
            "Wayanad": {"hotel_standard": 2400, "hotel_budget": 1100, "food": 450, "transport": 600, "activities": 350, "transit_from_kerala": 800},
            "Kochi": {"hotel_standard": 2500, "hotel_budget": 1000, "food": 550, "transport": 500, "activities": 400, "transit_from_kerala": 800},
            "Varkala": {"hotel_standard": 2200, "hotel_budget": 900, "food": 500, "transport": 450, "activities": 350, "transit_from_kerala": 900},
            "Goa": {"hotel_standard": 3200, "hotel_budget": 1200, "food": 700, "transport": 700, "activities": 600, "transit_from_kerala": 3500},
            "Gokarna": {"hotel_standard": 2200, "hotel_budget": 900, "food": 450, "transport": 500, "activities": 350, "transit_from_kerala": 2200},
            "Ooty": {"hotel_standard": 2600, "hotel_budget": 1100, "food": 500, "transport": 550, "activities": 400, "transit_from_kerala": 1200},
            "Jaipur": {"hotel_standard": 3000, "hotel_budget": 1000, "food": 600, "transport": 600, "activities": 500, "transit_from_kerala": 7500},
            "Manali": {"hotel_standard": 3500, "hotel_budget": 1200, "food": 700, "transport": 800, "activities": 600, "transit_from_kerala": 9500},
            "Delhi": {"hotel_standard": 3200, "hotel_budget": 1100, "food": 650, "transport": 600, "activities": 500, "transit_from_kerala": 7000},
            "Mumbai": {"hotel_standard": 4200, "hotel_budget": 1500, "food": 750, "transport": 700, "activities": 500, "transit_from_kerala": 6000},
        }
    },

    # ----------------------------------------------------
    # INTERNATIONAL DESTINATIONS
    # ----------------------------------------------------
    "Japan": {
        "currency_code": "JPY",
        "currency_symbol": "¥",
        "country_name": "Japan",
        "is_international": True,
        "flight_roundtrip_default": 52000,      # Roundtrip economy from CCJ/COK/BLR/BOM to NRT/HND
        "visa_fee": 1500,                       # Japan tourist eVisa / Embassy fee
        "travel_insurance": 1200,               # Mandatory medical/travel insurance (5-7 days)
        "hotel_standard_per_night": 8500,       # 3-star business hotel (e.g. APA, Sotetsu Fresa Inn)
        "hotel_budget_per_night": 3800,         # Capsule hotel or hostel bed
        "food_daily_per_person": 2400,          # Convenience store breakfast + ramen/curry lunch + dinner
        "local_transport_daily_per_person": 1300,# Tokyo Metro 24/72h pass + JR Yamanote line
        "activities_daily_per_person": 1600,    # Temples, Shibuya Sky, teamLab, Tokyo Skytree
        "daily_cost_tier": "High",
        "description": "High living costs and long-haul flights. Tokyo hotels and meals are priced in Japanese Yen.",
        "destinations": {
            "Tokyo": {"hotel_standard": 9200, "hotel_budget": 4200, "food": 2600, "transport": 1400, "activities": 1800, "flight": 52000},
            "Kyoto": {"hotel_standard": 8500, "hotel_budget": 3600, "food": 2400, "transport": 1200, "activities": 1600, "flight": 54000},
            "Osaka": {"hotel_standard": 7800, "hotel_budget": 3400, "food": 2200, "transport": 1200, "activities": 1500, "flight": 51000},
        }
    },

    "Thailand": {
        "currency_code": "THB",
        "currency_symbol": "฿",
        "country_name": "Thailand",
        "is_international": True,
        "flight_roundtrip_default": 18500,      # AirAsia / IndiGo / Thai Lion from South India
        "visa_fee": 2500,                       # VoA / eVisa (sometimes fee-exempt for India promotions)
        "travel_insurance": 900,
        "hotel_standard_per_night": 2800,       # Good 3-star hotel with pool/breakfast
        "hotel_budget_per_night": 1100,         # Backpacker hostel dorm
        "food_daily_per_person": 950,           # Thai street food, pad thai, local cafes
        "local_transport_daily_per_person": 600,# BTS Skytrain, MRT, Grab rides
        "activities_daily_per_person": 900,     # Grand Palace, island boat tour, temples
        "daily_cost_tier": "Budget International",
        "description": "One of the most affordable international destinations from India.",
        "destinations": {
            "Bangkok": {"hotel_standard": 2800, "hotel_budget": 1100, "food": 950, "transport": 650, "activities": 850, "flight": 18000},
            "Phuket": {"hotel_standard": 3400, "hotel_budget": 1300, "food": 1100, "transport": 800, "activities": 1200, "flight": 20000},
            "Chiang Mai": {"hotel_standard": 2400, "hotel_budget": 900, "food": 800, "transport": 500, "activities": 750, "flight": 19500},
            "Pattaya": {"hotel_standard": 2600, "hotel_budget": 1000, "food": 850, "transport": 500, "activities": 800, "flight": 18000},
            "Krabi": {"hotel_standard": 3200, "hotel_budget": 1200, "food": 1000, "transport": 700, "activities": 1100, "flight": 21000},
            "Koh Samui": {"hotel_standard": 4200, "hotel_budget": 1500, "food": 1200, "transport": 800, "activities": 1300, "flight": 24000},
        }
    },

    "United Arab Emirates": {
        "currency_code": "AED",
        "currency_symbol": "د.إ",
        "country_name": "United Arab Emirates",
        "is_international": True,
        "flight_roundtrip_default": 21000,      # Direct Air India Express / Indigo from Calicut/Kochi
        "visa_fee": 6800,                       # 30-day tourist visa via agency / airline
        "travel_insurance": 1000,
        "hotel_standard_per_night": 6200,       # 3-star hotel in Deira / Al Barsha
        "hotel_budget_per_night": 2800,         # Budget hotel or shared dorm
        "food_daily_per_person": 1800,          # Shawarma, food court, casual Indian/Arabic dining
        "local_transport_daily_per_person": 1100,# Dubai Metro Nol card + occasional taxi
        "activities_daily_per_person": 2400,    # Burj Khalifa, Desert Safari, Museum of the Future
        "daily_cost_tier": "Medium-High",
        "description": "Frequent direct flights from Kerala. Visa and popular attractions constitute significant expenses.",
        "destinations": {
            "Dubai": {"hotel_standard": 6800, "hotel_budget": 3000, "food": 1900, "transport": 1200, "activities": 2600, "flight": 21000},
            "Abu Dhabi": {"hotel_standard": 5800, "hotel_budget": 2600, "food": 1700, "transport": 1000, "activities": 2200, "flight": 20000},
            "Sharjah": {"hotel_standard": 4500, "hotel_budget": 2200, "food": 1400, "transport": 900, "activities": 1400, "flight": 19000},
        }
    },

    "Singapore": {
        "currency_code": "SGD",
        "currency_symbol": "S$",
        "country_name": "Singapore",
        "is_international": True,
        "flight_roundtrip_default": 22000,
        "visa_fee": 2500,
        "travel_insurance": 1000,
        "hotel_standard_per_night": 8800,       # Compact standard hotel (Ibis, Hotel 81, etc.)
        "hotel_budget_per_night": 3200,         # Pod hostel dorm
        "food_daily_per_person": 1700,          # Hawker centres (Maxwell, Chinatown, Lau Pa Sat)
        "local_transport_daily_per_person": 850,# SMRT trains & buses
        "activities_daily_per_person": 1800,    # Gardens by the Bay, Marina Bay Sands SkyPark
        "daily_cost_tier": "High",
        "description": "Very safe and modern, but accommodation prices are among the highest in Asia.",
    },

    "Malaysia": {
        "currency_code": "MYR",
        "currency_symbol": "RM",
        "country_name": "Malaysia",
        "is_international": True,
        "flight_roundtrip_default": 17500,
        "visa_fee": 1500,                       # MDAC registration / fee
        "travel_insurance": 900,
        "hotel_standard_per_night": 3200,
        "hotel_budget_per_night": 1200,
        "food_daily_per_person": 950,           # Mamak stalls, Nasi Lemak, street food
        "local_transport_daily_per_person": 600,# RapidKL MRT / Monorail / Grab
        "activities_daily_per_person": 900,     # Petronas Towers, Batu Caves, theme parks
        "daily_cost_tier": "Budget International",
        "description": "Affordable entry into international travel with excellent flight links from Kerala.",
    },

    "Vietnam": {
        "currency_code": "VND",
        "currency_symbol": "₫",
        "country_name": "Vietnam",
        "is_international": True,
        "flight_roundtrip_default": 19500,
        "visa_fee": 2600,                       # Official Vietnam eVisa ($25)
        "travel_insurance": 900,
        "hotel_standard_per_night": 2400,
        "hotel_budget_per_night": 900,
        "food_daily_per_person": 850,           # Pho, Banh Mi, egg coffee, local eateries
        "local_transport_daily_per_person": 500,# Grab bike/car
        "activities_daily_per_person": 950,     # Ha Long Bay cruise, Cu Chi tunnels
        "daily_cost_tier": "Budget International",
        "description": "Exceptional value for money. Daily hotel and food costs are comparable to tier-1 Indian cities.",
    },

    "Sri Lanka": {
        "currency_code": "LKR",
        "currency_symbol": "Rs",
        "country_name": "Sri Lanka",
        "is_international": True,
        "flight_roundtrip_default": 15000,      # Short direct hop from South India
        "visa_fee": 2500,                       # ETA tourist fee
        "travel_insurance": 850,
        "hotel_standard_per_night": 2600,
        "hotel_budget_per_night": 1000,
        "food_daily_per_person": 850,
        "local_transport_daily_per_person": 550,
        "activities_daily_per_person": 900,     # Sigiriya, tea estates, temple entry
        "daily_cost_tier": "Budget International",
        "description": "Very close to South India with budget-friendly flights and scenic rail routes.",
    },

    "Nepal": {
        "currency_code": "NPR",
        "currency_symbol": "रू",
        "country_name": "Nepal",
        "is_international": True,
        "flight_roundtrip_default": 16500,
        "visa_fee": 0,                          # Visa-free for Indian citizens (Passport/Voter ID)
        "travel_insurance": 800,
        "hotel_standard_per_night": 2200,
        "hotel_budget_per_night": 900,
        "food_daily_per_person": 750,
        "local_transport_daily_per_person": 450,
        "activities_daily_per_person": 700,
        "daily_cost_tier": "Budget International",
        "description": "No visa required for Indian citizens. Very economical for mountain and temple travel.",
    },

    "Maldives": {
        "currency_code": "MVR",
        "currency_symbol": "Rf",
        "country_name": "Maldives",
        "is_international": True,
        "flight_roundtrip_default": 18000,      # Short flight from Kochi/Bengaluru
        "visa_fee": 0,                          # Free 30-day visa on arrival for Indians
        "travel_insurance": 900,
        "hotel_standard_per_night": 5800,       # Local island guesthouse (Maafushi, etc.)
        "hotel_budget_per_night": 2800,
        "food_daily_per_person": 1800,          # Island restaurants
        "local_transport_daily_per_person": 800,# Speedboat/ferry transfers amortized
        "activities_daily_per_person": 2200,    # Snorkeling, sandbank tour, dolphin cruise
        "daily_cost_tier": "Medium-High",
        "description": "Affordable on inhabited local islands; luxury private water villas cost ₹40k+ per night.",
    },

    "Indonesia": {
        "currency_code": "IDR",
        "currency_symbol": "Rp",
        "country_name": "Indonesia",
        "is_international": True,
        "flight_roundtrip_default": 28000,      # Flights to Bali (DPS)
        "visa_fee": 3200,                       # e-VoA IDR 500,000 + tourist levy
        "travel_insurance": 1000,
        "hotel_standard_per_night": 3000,       # Bali boutique villa / 3-star hotel
        "hotel_budget_per_night": 1200,
        "food_daily_per_person": 1000,          # Local warungs, smoothie bowls, cafes
        "local_transport_daily_per_person": 700,# Scooter rental or Gojek/Grab
        "activities_daily_per_person": 1100,    # Waterfall entries, temple tickets, beach clubs
        "daily_cost_tier": "Medium",
        "description": "Bali offers affordable luxury on-ground, but airfares from India represent the main cost.",
    },

    "France": {
        "currency_code": "EUR",
        "currency_symbol": "€",
        "country_name": "France",
        "is_international": True,
        "flight_roundtrip_default": 58000,
        "visa_fee": 12500,                      # Schengen visa fee €90 + VFS fees + courier
        "travel_insurance": 1500,
        "hotel_standard_per_night": 11000,      # Paris 3-star standard hotel
        "hotel_budget_per_night": 4500,         # Hostel dorm
        "food_daily_per_person": 3200,          # Bakery, bistros, supermarket meals
        "local_transport_daily_per_person": 1500,# Metro & RER passes
        "activities_daily_per_person": 2200,    # Louvre, Eiffel Tower, Versailles
        "daily_cost_tier": "Very High",
        "description": "High living costs in Euros. Strict Schengen visa requirements and proof of funds.",
    },

    "Switzerland": {
        "currency_code": "CHF",
        "currency_symbol": "CHF",
        "country_name": "Switzerland",
        "is_international": True,
        "flight_roundtrip_default": 64000,
        "visa_fee": 12500,                      # Schengen visa + VFS
        "travel_insurance": 1500,
        "hotel_standard_per_night": 16500,      # Swiss hotel room (Zurich / Lucerne / Interlaken)
        "hotel_budget_per_night": 6500,         # Youth hostel dorm
        "food_daily_per_person": 4500,          # Fondue, supermarket, budget cafes
        "local_transport_daily_per_person": 3200,# Swiss Travel Pass / mountain trains
        "activities_daily_per_person": 3500,    # Jungfraujoch, cable cars, Lake cruises
        "daily_cost_tier": "Ultra High",
        "description": "One of the most expensive destinations in the world. Requires substantial budget.",
    },

    "Italy": {
        "currency_code": "EUR",
        "currency_symbol": "€",
        "country_name": "Italy",
        "is_international": True,
        "flight_roundtrip_default": 59000,
        "visa_fee": 12500,
        "travel_insurance": 1500,
        "hotel_standard_per_night": 10500,
        "hotel_budget_per_night": 4200,
        "food_daily_per_person": 3000,          # Pizza, pasta, gelato, espresso
        "local_transport_daily_per_person": 1400,
        "activities_daily_per_person": 2200,    # Colosseum, Vatican museums, Venice water bus
        "daily_cost_tier": "Very High",
        "description": "Schengen country with rich historical attractions and European pricing.",
    },

    "United Kingdom": {
        "currency_code": "GBP",
        "currency_symbol": "£",
        "country_name": "United Kingdom",
        "is_international": True,
        "flight_roundtrip_default": 62000,
        "visa_fee": 13500,                      # UK standard visitor visa (£115) + biometrics
        "travel_insurance": 1500,
        "hotel_standard_per_night": 12500,      # London zone 2-3 standard hotel
        "hotel_budget_per_night": 4500,         # Hostel dorm
        "food_daily_per_person": 3200,          # Pub dining, meal deals (Tesco/M&S), cafes
        "local_transport_daily_per_person": 1600,# London Underground daily cap
        "activities_daily_per_person": 2000,    # Tower of London, London Eye (many museums free)
        "daily_cost_tier": "Very High",
        "description": "High visa fee and currency valuation (£1 ≈ ₹108+).",
    },

    "United States": {
        "currency_code": "USD",
        "currency_symbol": "$",
        "country_name": "United States",
        "is_international": True,
        "flight_roundtrip_default": 86000,      # Long-haul flights from India
        "visa_fee": 18500,                      # US B1/B2 visa ($185)
        "travel_insurance": 2500,               # US healthcare requires solid medical insurance
        "hotel_standard_per_night": 14000,      # NYC/SF/LA standard 3-star
        "hotel_budget_per_night": 5000,
        "food_daily_per_person": 3800,          # Diners, casual dining + 18-20% tips
        "local_transport_daily_per_person": 1800,# Subway + rideshare
        "activities_daily_per_person": 2500,    # Observation decks, national parks, museums
        "daily_cost_tier": "Ultra High",
        "description": "Very long flight distance, expensive healthcare/hotels, and US visa interview backlogs.",
    },

    "Turkey": {
        "currency_code": "TRY",
        "currency_symbol": "₺",
        "country_name": "Turkey",
        "is_international": True,
        "flight_roundtrip_default": 42000,
        "visa_fee": 6500,                       # Turkey visa fee + agency
        "travel_insurance": 1100,
        "hotel_standard_per_night": 4800,
        "hotel_budget_per_night": 1800,
        "food_daily_per_person": 1400,          # Turkish kebabs, baklava, breakfast
        "local_transport_daily_per_person": 800,# Istanbulkart metro/trams/ferry
        "activities_daily_per_person": 1600,    # Hagia Sophia, Topkapi, Cappadocia
        "daily_cost_tier": "Medium",
        "description": "Bridging Europe and Asia; highly scenic with moderate daily expenses.",
    },

    "Germany": {
        "currency_code": "EUR",
        "currency_symbol": "€",
        "country_name": "Germany",
        "is_international": True,
        "flight_roundtrip_default": 57000,
        "visa_fee": 12500,
        "travel_insurance": 1500,
        "hotel_standard_per_night": 9800,
        "hotel_budget_per_night": 3800,
        "food_daily_per_person": 2800,
        "local_transport_daily_per_person": 1400,
        "activities_daily_per_person": 1800,
        "daily_cost_tier": "Very High",
        "description": "Efficient public transit, high living standards, Schengen entry requirements.",
    },

    "Spain": {
        "currency_code": "EUR",
        "currency_symbol": "€",
        "country_name": "Spain",
        "is_international": True,
        "flight_roundtrip_default": 58000,
        "visa_fee": 12500,
        "travel_insurance": 1500,
        "hotel_standard_per_night": 9500,
        "hotel_budget_per_night": 3600,
        "food_daily_per_person": 2600,          # Tapas, paella, cafe con leche
        "local_transport_daily_per_person": 1200,
        "activities_daily_per_person": 2000,    # Sagrada Familia, Park Guell, museums
        "daily_cost_tier": "High",
        "description": "Slightly more affordable than northern Europe, with famous cultural landmarks.",
    },

    "Australia": {
        "currency_code": "AUD",
        "currency_symbol": "A$",
        "country_name": "Australia",
        "is_international": True,
        "flight_roundtrip_default": 72000,
        "visa_fee": 13000,                      # Subclass 600 tourist visa (AUD 190)
        "travel_insurance": 1800,
        "hotel_standard_per_night": 12000,
        "hotel_budget_per_night": 4500,
        "food_daily_per_person": 3400,
        "local_transport_daily_per_person": 1600,
        "activities_daily_per_person": 2500,    # Opera House, Great Barrier Reef, wildlife parks
        "daily_cost_tier": "Very High",
        "description": "Long flight from India, strict border controls, and high Australian dollar costs.",
    },

    "Canada": {
        "currency_code": "CAD",
        "currency_symbol": "C$",
        "country_name": "Canada",
        "is_international": True,
        "flight_roundtrip_default": 89000,
        "visa_fee": 14000,                      # Visitor visa + biometrics fee
        "travel_insurance": 2200,
        "hotel_standard_per_night": 13000,
        "hotel_budget_per_night": 4600,
        "food_daily_per_person": 3500,
        "local_transport_daily_per_person": 1600,
        "activities_daily_per_person": 2400,    # CN Tower, Banff entry, museums
        "daily_cost_tier": "Ultra High",
        "description": "Transatlantic flight times, strict visa vetting, and North American hotel rates.",
    },
}



INDIAN_STATES = {
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Puducherry", "Chandigarh", "Andaman and Nicobar"
}

KNOWN_INDIAN_DESTINATIONS = {
    "Wayanad", "Munnar", "Alleppey", "Kochi", "Varkala", "Kozhikode", "Malappuram",
    "Goa", "Gokarna", "Ooty", "Coorg", "Mysuru", "Bengaluru", "Kodaikanal", "Chennai",
    "Hyderabad", "Jaipur", "Udaipur", "Manali", "Shimla", "Delhi", "Mumbai", "Agra",
    "Varanasi", "Kolkata", "Darjeeling", "Rishikesh", "Amritsar", "Pondicherry", "Puri",
    "Hampi", "Jodhpur", "Jaisalmer", "Nainital", "Mussoorie", "Dharamshala", "Leh"
}

def check_is_domestic(destination: str = "", country: str = "") -> bool:
    """Robustly verify if destination or country is inside India."""
    c_norm = (country or "").strip().title()
    d_norm = (destination or "").strip().title()

    if not c_norm or c_norm in {"India", "Domestic"}:
        return True
    
    if c_norm in INDIAN_STATES or any(s.casefold() == c_norm.casefold() for s in INDIAN_STATES):
        return True

    if d_norm in KNOWN_INDIAN_DESTINATIONS or any(k.casefold() == d_norm.casefold() for k in KNOWN_INDIAN_DESTINATIONS):
        return True

    india_dests = BENCHMARK_DATA.get("India", {}).get("destinations", {})
    if d_norm in india_dests or any(k.casefold() == d_norm.casefold() for k in india_dests):
        return True

    return False


def get_country_benchmark(country: str, destination: str = "") -> Dict[str, Any]:
    """Retrieve benchmark data for a country with fallback defaults."""
    if check_is_domestic(destination, country):
        return BENCHMARK_DATA["India"]
    """Retrieve benchmark data for a country with fallback defaults."""
    country_cleaned = (country or "").strip().title()

    # Exact or alias match
    for key, data in BENCHMARK_DATA.items():
        if key.casefold() == country_cleaned.casefold():
            return data

    # Partial match
    for key, data in BENCHMARK_DATA.items():
        if key.casefold() in country_cleaned.casefold() or country_cleaned.casefold() in key.casefold():
            return data

    # Default fallback for unknown international countries
    return {
        "currency_code": "USD",
        "currency_symbol": "$",
        "country_name": country or "International",
        "is_international": True,
        "flight_roundtrip_default": 45000,
        "visa_fee": 4000,
        "travel_insurance": 1200,
        "hotel_standard_per_night": 7000,
        "hotel_budget_per_night": 2800,
        "food_daily_per_person": 2000,
        "local_transport_daily_per_person": 1200,
        "activities_daily_per_person": 1500,
        "daily_cost_tier": "Medium-High",
        "description": "Estimated benchmark based on standard global travel metrics.",
    }


def get_own_vehicle_feasibility(
    destination: str,
    country: str,
    starting_location: str = "Malappuram, Kerala",
    travellers: int = 1
) -> dict:
    """
    Evaluate whether travelling with own vehicle (Car or Bike / Motorcycle) is possible,
    practical, and recommended from the starting location to the chosen destination.
    Provides highway routes, driving duration, fuel costs, toll fees, and road advice.
    """
    dest_key = (destination or "").strip().title()
    is_domestic = check_is_domestic(dest_key, country)
    country_norm = "India" if is_domestic else (country or "").strip().title()
    travellers = max(1, int(travellers))

    if not is_domestic:
        return {
            "possible": False,
            "status": "NOT_POSSIBLE",
            "badge_color": "#ef4444",
            "badge_icon": "❌",
            "verdict": "Not Possible with Own Vehicle (Overseas / Trans-Oceanic)",
            "summary": (
                f"Driving your own vehicle from India to {dest_key}, {country_norm} is not feasible. "
                "International borders, ocean crossings, and customs carnets make road travel impossible. "
                "Commercial international flights are required."
            ),
            "distance_km": None,
            "duration": None,
            "highway": "N/A (Trans-oceanic flight route)",
            "car_fuel_roundtrip": 0,
            "bike_fuel_roundtrip": 0,
            "tolls_roundtrip": 0,
            "total_car_cost": 0,
            "cost_per_person_car": 0,
            "cost_per_person_bike": 0,
            "tips": (
                "Book roundtrip flights from Calicut (CCJ) or Kochi (COK). "
                "Upon arrival, use local public transit (trains, metro, city buses) or rent a local vehicle with an International Driving Permit (IDP)."
            ),
        }

    # Road routes departing from Malappuram / Kozhikode, Kerala
    known_routes = {
        "Wayanad": {
            "possible": True,
            "status": "HIGHLY_FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Highly Feasible & Strongly Recommended",
            "summary": (
                "Wayanad is ideally suited for an own-vehicle road trip from Malappuram/Kozhikode. "
                "Having your own car or bike is the best way to explore Wayanad because tourist spots "
                "(Banasura Sagar Dam, Edakkal Caves, Chembra Peak, Pookode Lake, Meenmutty Waterfalls) "
                "are scattered 15 to 35 km apart across mountain ridges with very limited public buses or metered cabs."
            ),
            "distance_km": 95,
            "duration": "2.5 - 3.5 hrs one-way",
            "highway": "NH766 via Areekode / Kondotty -> Kozhikode bypass -> Thamarassery Churam (9 Hairpin Bends) -> Lakkidi -> Kalpetta",
            "car_fuel_roundtrip": 1400,
            "bike_fuel_roundtrip": 550,
            "tolls_roundtrip": 0,
            "tips": (
                "1. Drive in 2nd/3rd gear on the 9 steep hairpin bends of Thamarassery Churam; never overtake on blind turns.\n"
                "2. Check tyre pressure, brake pads, and radiator coolant level before climbing.\n"
                "3. Early morning departure (before 7:00 AM) avoids heavy lorry ghat congestion."
            ),
        },
        "Munnar": {
            "possible": True,
            "status": "HIGHLY_FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Highly Feasible & Scenic Mountain Drive",
            "summary": (
                "Munnar offers an iconic Western Ghats road trip. An own vehicle gives you total flexibility "
                "to pull over at tea plantation viewpoints, Cheeyappara and Valara waterfalls, and Spice gardens."
            ),
            "distance_km": 210,
            "duration": "5.5 - 6.5 hrs one-way",
            "highway": "NH544 / NH85 via Perinthalmanna -> Angamaly -> Muvattupuzha -> Kothamangalam -> Neriamangalam -> Adimali -> Munnar",
            "car_fuel_roundtrip": 3200,
            "bike_fuel_roundtrip": 1200,
            "tolls_roundtrip": 180,
            "tips": (
                "1. Ghat roads have sharp hairpins and foggy patches; test fog lamps and wipers before leaving.\n"
                "2. Frequent rainfall causes slippery roads; keep safe distance behind heavy tourist buses."
            ),
        },
        "Ooty": {
            "possible": True,
            "status": "HIGHLY_FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Highly Feasible & Forest Ghat Drive",
            "summary": (
                "A scenic mountain drive traversing the Nilambur teak reserve and the Nadugani mountain pass into Tamil Nadu."
            ),
            "distance_km": 135,
            "duration": "3.5 - 4.5 hrs one-way",
            "highway": "SH28 / NH181 via Manjeri -> Nilambur -> Vazhikkadavu Ghats -> Nadugani -> Gudalur -> Ooty",
            "car_fuel_roundtrip": 2200,
            "bike_fuel_roundtrip": 800,
            "tolls_roundtrip": 100,
            "tips": (
                "1. Mandatory Tamil Nadu e-Pass must be registered online prior to entering Nilgiris district.\n"
                "2. Green tax (₹50-₹100) is paid at the state border checkpost.\n"
                "3. Beware of wildlife crossings (elephants, spotted deer) along the Nilambur-Gudalur forest corridor."
            ),
        },
        "Goa": {
            "possible": True,
            "status": "FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Feasible & Rewarding Coastal Highway Road Trip",
            "summary": (
                "A wonderful long road trip hugging the Arabian Sea via the newly upgraded 4-lane NH66 coastal expressway. "
                "Having your own car or bike in Goa gives you effortless freedom to hop between North & South Goa beaches without paying expensive local tourist taxi unions."
            ),
            "distance_km": 460,
            "duration": "10 - 12 hrs one-way",
            "highway": "NH66 coastal corridor via Kozhikode -> Kannur -> Kasaragod -> Mangalore -> Udupi -> Kundapura -> Bhatkal -> Karwar -> Canacona (South Goa)",
            "car_fuel_roundtrip": 6800,
            "bike_fuel_roundtrip": 2600,
            "tolls_roundtrip": 550,
            "tips": (
                "1. Depart early by 5:00 AM to cross Kannur and Mangalore before morning city traffic.\n"
                "2. Keep FASTag recharged with at least ₹1,000 for Karnataka & Kerala toll plazas.\n"
                "3. Swap driving duties with a second driver, or plan a scenic lunch break near Maravanthe Beach / Udupi."
            ),
        },
        "Alleppey": {
            "possible": True,
            "status": "HIGHLY_FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Highly Feasible & Easy Flat Highway Drive",
            "summary": (
                "Direct flat highway route down central Kerala. Highly recommended for family trips with luggage for houseboat check-in."
            ),
            "distance_km": 195,
            "duration": "4.5 - 5.5 hrs one-way",
            "highway": "NH66 via Kuttippuram -> Edappal -> Thrissur bypass -> Ernakulam bypass -> Cherthala -> Alappuzha",
            "car_fuel_roundtrip": 3000,
            "bike_fuel_roundtrip": 1100,
            "tolls_roundtrip": 180,
            "tips": (
                "Official houseboat boarding jetties (Finishing Point & Punnamada) provide secure paid overnight car parking (₹150-₹200/night)."
            ),
        },
        "Kochi": {
            "possible": True,
            "status": "HIGHLY_FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Highly Feasible & Fast Highway Drive",
            "summary": "Straightforward 3.5 to 4-hour highway drive connecting to Kerala\'s commercial hub and heritage Fort Kochi.",
            "distance_km": 145,
            "duration": "3.5 - 4 hrs one-way",
            "highway": "NH66 / NH544 via Valanchery -> Kuttippuram -> Thrissur -> Angamaly -> Aluva -> Edappally",
            "car_fuel_roundtrip": 2200,
            "bike_fuel_roundtrip": 800,
            "tolls_roundtrip": 140,
            "tips": "Consider parking at Aluva or Edappally Metro station and taking the Kochi Metro to avoid city centre congestion.",
        },
        "Varkala": {
            "possible": True,
            "status": "HIGHLY_FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Feasible South Kerala Coastal Highway Drive",
            "summary": "Direct coastal drive connecting to Varkala\'s famous red cliffs and Papanasam beach.",
            "distance_km": 310,
            "duration": "7 - 8 hrs one-way",
            "highway": "NH66 via Ernakulam -> Alappuzha -> Kollam bypass -> Parippally -> Varkala Cliff",
            "car_fuel_roundtrip": 4800,
            "bike_fuel_roundtrip": 1700,
            "tolls_roundtrip": 250,
            "tips": "Varkala Cliff access pathways are narrow and pedestrianised; check if your hotel has verified dedicated car parking before arrival.",
        },
        "Coorg": {
            "possible": True,
            "status": "HIGHLY_FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Highly Feasible & Scenic Coffee Estate Drive",
            "summary": "Gentle winding roads through Western Ghats forests and coffee estates into Madikeri / Coorg.",
            "distance_km": 170,
            "duration": "4 - 5 hrs one-way",
            "highway": "SH30 via Kozhikode -> Thalassery -> Mattannur -> Iritty -> Virajpet -> Madikeri",
            "car_fuel_roundtrip": 2600,
            "bike_fuel_roundtrip": 950,
            "tolls_roundtrip": 60,
            "tips": "Smooth tarmac and picturesque countryside. Stop at local coffee plantation stores along the Virajpet route.",
        },
        "Mysuru": {
            "possible": True,
            "status": "HIGHLY_FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Highly Feasible (Daytime Forest Reserve Drive)",
            "summary": "Pleasant drive traversing Nilambur, Gudalur, and the scenic Bandipur Tiger Reserve into Mysuru.",
            "distance_km": 165,
            "duration": "4 - 4.5 hrs one-way",
            "highway": "NH766 / SH28 via Nilambur -> Gudalur -> Bandipur National Park -> Gundlupet -> Mysuru",
            "car_fuel_roundtrip": 2500,
            "bike_fuel_roundtrip": 900,
            "tolls_roundtrip": 100,
            "tips": "CRITICAL: Bandipur National Park forest gates strictly close for all vehicle traffic from 9:00 PM to 6:00 AM every night. Plan your drive during daylight.",
        },
        "Bengaluru": {
            "possible": True,
            "status": "FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Feasible Interstate Expressway Drive",
            "summary": "Direct interstate journey via Gundlupet, Mysore, and the new 10-lane Bangalore-Mysore Expressway.",
            "distance_km": 315,
            "duration": "7 - 8 hrs one-way",
            "highway": "NH766 via Nilambur -> Gudalur -> Gundlupet -> Mysore -> Mysore-Bengaluru Expressway",
            "car_fuel_roundtrip": 4800,
            "bike_fuel_roundtrip": 1750,
            "tolls_roundtrip": 650,
            "tips": "Motorcycles are not permitted on the main expressway carriage-way; two-wheelers must take the parallel service road.",
        },
        "Gokarna": {
            "possible": True,
            "status": "FEASIBLE",
            "badge_color": "#10b981",
            "badge_icon": "✅",
            "verdict": "Feasible Coastal Highway Drive",
            "summary": "Scenic coastal drive along North Karnataka beaches. Ideal for beach hopping and temple visits.",
            "distance_km": 350,
            "duration": "8 - 9 hrs one-way",
            "highway": "NH66 coastal corridor via Kannur -> Kasaragod -> Mangalore -> Udupi -> Murudeshwar -> Kumta -> Gokarna",
            "car_fuel_roundtrip": 5400,
            "bike_fuel_roundtrip": 1950,
            "tolls_roundtrip": 450,
            "tips": "Dedicated open parking areas are located above Om Beach and Kudle Beach trail entrances.",
        },
    }

    if dest_key in known_routes:
        route_info = dict(known_routes[dest_key])
    else:
        far_cities = {"Delhi", "Jaipur", "Manali", "Mumbai", "Agra", "Varanasi", "Kashmir", "Srinagar", "Udaipur", "Kolkata", "Shimla", "Ladakh", "Amritsar"}
        if dest_key in far_cities:
            route_info = {
                "possible": True,
                "status": "IMPRACTICAL",
                "badge_color": "#f59e0b",
                "badge_icon": "⚠️",
                "verdict": "Possible but Impractical for Short Vacations (2,000+ km)",
                "summary": (
                    f"Driving your own vehicle from Kerala to {dest_key} covers 2,000 to 2,800+ km each way across 5 to 7 Indian states. "
                    "It demands 35 to 50+ hours of continuous highway driving. Fuel and toll expenses alone will exceed ₹35,000, "
                    "which consumes your entire budget and vacation time purely on highway transit."
                ),
                "distance_km": 2400,
                "duration": "40 - 55 hrs one-way (3-4 full driving days)",
                "highway": "NH48 / NH44 cross-country Golden Quadrilateral corridors",
                "car_fuel_roundtrip": 34000,
                "bike_fuel_roundtrip": 13000,
                "tolls_roundtrip": 4500,
                "tips": "Unless planning a month-long overland expedition, take an Economy Flight (3.5 hrs) or Indian Railways 3AC/2AC train instead.",
            }
        else:
            route_info = {
                "possible": True,
                "status": "FEASIBLE",
                "badge_color": "#10b981",
                "badge_icon": "✅",
                "verdict": "Feasible Regional Highway Drive",
                "summary": f"You can drive your own vehicle to {dest_key} via regional highway networks departing from {starting_location}.",
                "distance_km": 280,
                "duration": "6 - 7 hrs one-way",
                "highway": "National & State Highway networks connecting Kerala to neighboring regions",
                "car_fuel_roundtrip": 4200,
                "bike_fuel_roundtrip": 1500,
                "tolls_roundtrip": 250,
                "tips": "Keep FASTag active, vehicle papers (RC, Insurance, PUC) handy, and observe daytime wildlife corridor rules.",
            }

    total_car_cost = route_info["car_fuel_roundtrip"] + route_info["tolls_roundtrip"]
    route_info["total_car_cost"] = total_car_cost
    route_info["cost_per_person_car"] = round(total_car_cost / travellers)
    route_info["cost_per_person_bike"] = round((route_info["bike_fuel_roundtrip"] + (route_info["tolls_roundtrip"] * 0.2)) / min(travellers, 2))

    return route_info


def get_transport_options(
    destination: str,
    country: str,
    starting_location: str = "Malappuram, Kerala",
    travellers: int = 1
) -> list:
    """
    Retrieve DISTINCT transportation modes available from the starting location to the destination:
    1. 🚗 Own Vehicle (Car / Bike Self-Drive)
    2. 🚌 Public / Interstate Bus (KSRTC / Volvo)
    3. 🚆 Indian Railways Train (Sleeper / 3AC / Vande Bharat)
    4. 🚕 Outstation Taxi / Hired Cab
    5. ✈️ Commercial Flight (Economy)
    """
    dest_key = (destination or "").strip().title()
    is_domestic = check_is_domestic(dest_key, country)
    country_norm = "India" if is_domestic else (country or "").strip().title()
    travellers = max(1, int(travellers))

    benchmark = get_country_benchmark("India" if is_domestic else country)
    city_override = benchmark.get("destinations", {}).get(dest_key, {})

    # Evaluate Own Vehicle feasibility
    own_veh = get_own_vehicle_feasibility(dest_key, country_norm, starting_location, travellers)

    options = []

    if is_domestic:
        # MODE 1: 🚗 OWN VEHICLE (CAR / BIKE SELF-DRIVE)
        if own_veh["possible"]:
            car_label = f"🚗 Own Vehicle (Self-Drive Car/Bike)"
            options.append({
                "id": "own_vehicle",
                "name": car_label,
                "mode": "🚗 Own Vehicle (Self-Drive)",
                "category": "Own Vehicle",
                "cost_per_person": own_veh["cost_per_person_car"],
                "total_cost": own_veh["total_car_cost"],
                "duration": own_veh["duration"],
                "pros": "Total freedom, no tickets needed, explore all viewpoints freely",
                "notes": f"Route: {own_veh['highway']}. Fuel + tolls ~₹{own_veh['total_car_cost']:,} total group cost.",
                "recommended": (dest_key in {"Wayanad", "Munnar", "Ooty", "Coorg"}),
                "is_own_vehicle": True,
            })

        # MODE 2: 🚌 BUS (KSRTC / INTERSTATE / SLEEPER)
        bus_cost_map = {
            "Wayanad": 350,
            "Munnar": 600,
            "Ooty": 650,
            "Goa": 2000,
            "Alleppey": 550,
            "Kochi": 450,
            "Varkala": 650,
            "Coorg": 700,
            "Mysuru": 650,
            "Bengaluru": 1400,
            "Gokarna": 1800,
        }
        bus_cost = bus_cost_map.get(dest_key, 900 if own_veh.get("distance_km", 250) < 500 else 2200)
        bus_time = "3 - 4 hrs" if dest_key == "Wayanad" else ("6 - 7.5 hrs" if dest_key == "Munnar" else ("11 - 13 hrs" if dest_key in {"Goa", "Gokarna"} else "5 - 8 hrs"))
        options.append({
            "id": "bus",
            "name": "🚌 KSRTC / Interstate Bus",
            "mode": "🚌 Bus (KSRTC / Private)",
            "category": "Bus",
            "cost_per_person": bus_cost,
            "total_cost": bus_cost * travellers,
            "duration": bus_time,
            "pros": "Most economical travel mode, direct bus stands",
            "notes": f"Regular KSRTC Swift / Superfast & private AC sleeper buses connecting from {starting_location}.",
            "recommended": False,
            "is_own_vehicle": False,
        })

        # MODE 3: 🚆 TRAIN (INDIAN RAILWAYS)
        train_cost_map = {
            "Goa": 1200,
            "Alleppey": 450,
            "Kochi": 350,
            "Varkala": 550,
            "Bengaluru": 950,
            "Gokarna": 1100,
            "Delhi": 2800,
            "Jaipur": 2900,
            "Mumbai": 2200,
            "Manali": 3200,
        }
        if dest_key in train_cost_map:
            t_cost = train_cost_map[dest_key]
            t_dur = "10 - 12 hrs" if dest_key == "Goa" else ("3.5 - 4.5 hrs" if dest_key in {"Alleppey", "Kochi"} else "30 - 40 hrs")
            options.append({
                "id": "train",
                "name": "🚆 Express Train (Indian Railways Sleeper / 3AC)",
                "mode": "🚆 Train (IRCTC Express)",
                "category": "Train",
                "cost_per_person": t_cost,
                "total_cost": t_cost * travellers,
                "duration": t_dur,
                "pros": "Punctual, comfortable berths, excellent value for long distances",
                "notes": f"Direct trains departing Kozhikode (CLT), Tirur (TIR), or Shoranur (SRR). Book early on IRCTC.",
                "recommended": (dest_key in {"Goa", "Alleppey", "Kochi", "Varkala"}),
                "is_own_vehicle": False,
            })
        elif dest_key in {"Wayanad", "Munnar", "Ooty", "Coorg"}:
            # Hill stations without direct railway tracks
            nearest_stn = "Kozhikode (CLT)" if dest_key in {"Wayanad", "Coorg"} else ("Aluva (AWY)" if dest_key == "Munnar" else "Mettupalayam (MTP)")
            options.append({
                "id": "train_connecting",
                "name": f"🚆 Train to {nearest_stn} + Connecting Road Transit",
                "mode": "🚆 Train + Bus/Cab",
                "category": "Train",
                "cost_per_person": 750,
                "total_cost": 750 * travellers,
                "duration": "5 - 7 hrs",
                "pros": "Scenic rail leg; connects to hill stations without tracks",
                "notes": f"Note: {dest_key} has no direct train station. Nearest railhead is {nearest_stn} (60-80 km away), then proceed by bus or taxi.",
                "recommended": False,
                "is_own_vehicle": False,
            })

        # MODE 4: 🚕 OUTSTATION TAXI / HIRED CAB
        cab_cost_map = {
            "Wayanad": 1800,
            "Munnar": 2200,
            "Ooty": 2200,
            "Kochi": 1400,
            "Alleppey": 1700,
            "Goa": 5500,
            "Coorg": 2400,
            "Mysuru": 2200,
        }
        cab_cost = cab_cost_map.get(dest_key, 2500)
        options.append({
            "id": "taxi_cab",
            "name": "🚕 Outstation Taxi / Hired Cab",
            "mode": "🚕 Taxi / Private Cab",
            "category": "Taxi / Cab",
            "cost_per_person": cab_cost,
            "total_cost": cab_cost * travellers,
            "duration": own_veh.get("duration", "4 - 6 hrs"),
            "pros": "Door-to-door comfort with dedicated professional driver",
            "notes": "Includes vehicle hire, fuel, driver allowance, and roundtrip pickup & drop.",
            "recommended": False,
            "is_own_vehicle": False,
        })

        # MODE 5: ✈️ FLIGHT (ECONOMY) - For Far domestic destinations
        far_destinations = {"Delhi", "Jaipur", "Manali", "Mumbai", "Agra", "Varanasi", "Kashmir", "Srinagar", "Udaipur", "Kolkata", "Shimla", "Goa"}
        if dest_key in far_destinations:
            flight_cost = city_override.get("transit_from_kerala", benchmark.get("flight_roundtrip_default", 6500))
            options.append({
                "id": "flight",
                "name": "✈️ Commercial Flight (Economy Class)",
                "mode": "✈️ Flight (Economy)",
                "category": "Flight",
                "cost_per_person": flight_cost,
                "total_cost": flight_cost * travellers,
                "duration": "2.5 - 4.5 hrs flight transit",
                "pros": "Fastest travel across India; saves 2 full days of transit",
                "notes": "Roundtrip flights departing Calicut (CCJ) or Kochi (COK) to destination airport.",
                "recommended": (dest_key not in {"Goa"}),
                "is_own_vehicle": False,
            })

    else:
        # International Destination: Flight is the only realistic overseas mode
        intl_flight_cost = city_override.get("flight", benchmark.get("flight_roundtrip_default", 32000))
        options = [
            {
                "id": "flight",
                "name": f"✈️ Commercial Return Flight (Calicut/Kochi -> {dest_key})",
                "mode": "✈️ International Flight",
                "category": "Flight",
                "cost_per_person": intl_flight_cost,
                "total_cost": intl_flight_cost * travellers,
                "duration": "4 - 14 hrs flight transit",
                "pros": "The only practical and legal mode of transport for international travel",
                "notes": f"Departing CCJ / COK to {dest_key}, {country_norm}. Includes mandatory cabin/checked baggage.",
                "recommended": True,
                "is_own_vehicle": False,
            }
        ]

    return options


def calculate_real_trip_budget(
    destination: str,
    country: str,
    days: int,
    travellers: int,
    starting_location: str = "Malappuram, Kerala",
    tier: str = "standard",  # "standard" or "budget"
    transport_mode_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Calculate realistic travel expenses using authentic market benchmarks.
    Distinguishes deeply between Domestic Indian travel and International travel.
    Allows interactive selection across multiple available transportation options.
    """
    days = max(int(days), 1)
    travellers = max(int(travellers), 1)
    nights = max(days - 1, 1)

    dest_key = (destination or "").strip().title()
    is_domestic = check_is_domestic(dest_key, country)
    country_norm = "India" if is_domestic else (country or "").strip().title()

    benchmark = get_country_benchmark("India" if is_domestic else country, destination=dest_key)

    # Check for city-level overrides
    dest_key = (destination or "").strip().title()
    city_override = benchmark.get("destinations", {}).get(dest_key, {})

    # 1. Available Transport Options & Mode Selection
    transport_options = get_transport_options(
        destination=dest_key,
        country=country_norm,
        starting_location=starting_location,
        travellers=travellers,
    )

    chosen_transport = None
    if transport_mode_id:
        chosen_transport = next((opt for opt in transport_options if opt["id"] == transport_mode_id), None)
    if not chosen_transport:
        chosen_transport = next((opt for opt in transport_options if opt.get("recommended")), transport_options[0])

    flight_or_transit_per_person = chosen_transport["cost_per_person"]
    transport_mode = chosen_transport["name"]
    total_flights_or_transit = flight_or_transit_per_person * travellers

    # 2. Visa and Mandatory Travel Insurance
    visa_fee_per_person = 0 if is_domestic else benchmark["visa_fee"]
    insurance_per_person = 0 if is_domestic else benchmark["travel_insurance"]
    total_visa_insurance = (visa_fee_per_person + insurance_per_person) * travellers

    # 3. Accommodation calculation
    # Rooms required: 1 per solo traveller, or ceil(travellers / 2) for groups/couples
    rooms = travellers if travellers == 1 else math.ceil(travellers / 2)

    hotel_rate_key = "hotel_standard" if tier == "standard" else "hotel_budget"
    default_hotel = benchmark["hotel_standard_per_night"] if tier == "standard" else benchmark["hotel_budget_per_night"]
    room_per_night = city_override.get(hotel_rate_key, default_hotel)
    total_accommodation = room_per_night * rooms * nights

    # 4. Daily Food & Dining
    food_per_person_day = city_override.get("food", benchmark["food_daily_per_person"])
    total_food = food_per_person_day * travellers * days

    # 5. Local Commute & Transit in Destination
    local_transit_per_person_day = city_override.get("transport", benchmark["local_transport_daily_per_person"])
    total_local_transit = local_transit_per_person_day * travellers * days

    # 6. Activities & Sightseeing
    activities_per_person_day = city_override.get("activities", benchmark["activities_daily_per_person"])
    total_activities = activities_per_person_day * travellers * days

    # 7. Subtotal & Emergency Reserve (5% - 8%)
    subtotal = (
        total_flights_or_transit
        + total_visa_insurance
        + total_accommodation
        + total_food
        + total_local_transit
        + total_activities
    )
    emergency_rate = 0.05 if is_domestic else 0.07  # higher reserve for forex / abroad
    total_emergency_reserve = round(subtotal * emergency_rate)
    estimated_total = subtotal + total_emergency_reserve

    # Per person & per day metrics
    cost_per_person = round(estimated_total / travellers)
    cost_per_person_day = round(cost_per_person / days)

    # Detailed itemized list
    items = [
        {
            "Expense": transport_mode,
            "Category": "Flights & Long-distance Travel",
            "Rate / Unit": f"₹{flight_or_transit_per_person:,.0f} / person roundtrip",
            "Estimated amount (INR)": round(total_flights_or_transit),
            "Share": f"{(total_flights_or_transit / estimated_total):.0%}",
            "Mandatory": True,
            "Notes": chosen_transport.get("notes", "Fixed cost required to reach destination"),
        },
        {
            "Expense": f"Accommodation ({nights} night{'s' if nights > 1 else ''}, {rooms} room{'s' if rooms > 1 else ''})",
            "Category": "Hotel & Stay",
            "Rate / Unit": f"₹{room_per_night:,.0f} / room / night",
            "Estimated amount (INR)": round(total_accommodation),
            "Share": f"{(total_accommodation / estimated_total):.0%}",
            "Mandatory": True,
            "Notes": f"{'Standard 3-star private room' if tier == 'standard' else 'Budget hotel / hostel'}",
        },
        {
            "Expense": f"Food & Dining ({days} days)",
            "Category": "Food & Dining",
            "Rate / Unit": f"₹{food_per_person_day:,.0f} / person / day",
            "Estimated amount (INR)": round(total_food),
            "Share": f"{(total_food / estimated_total):.0%}",
            "Mandatory": True,
            "Notes": "Daily meals, drinks, and casual dining",
        },
        {
            "Expense": f"Local Transit & Commute ({days} days)",
            "Category": "Local Commute",
            "Rate / Unit": f"₹{local_transit_per_person_day:,.0f} / person / day",
            "Estimated amount (INR)": round(total_local_transit),
            "Share": f"{(total_local_transit / estimated_total):.0%}",
            "Mandatory": True,
            "Notes": "City metro passes, local trains, and cabs",
        },
    ]

    if not is_domestic and total_visa_insurance > 0:
        items.append({
            "Expense": f"Visa & Mandatory Travel Insurance ({travellers} traveller{'s' if travellers > 1 else ''})",
            "Category": "Visa & Documentation",
            "Rate / Unit": f"₹{(visa_fee_per_person + insurance_per_person):,.0f} / person",
            "Estimated amount (INR)": round(total_visa_insurance),
            "Share": f"{(total_visa_insurance / estimated_total):.0%}",
            "Mandatory": True,
            "Notes": f"Visa: ₹{visa_fee_per_person:,.0f} + Medical Insurance: ₹{insurance_per_person:,.0f}",
        })

    items.extend([
        {
            "Expense": f"Sightseeing & Attractions ({days} days)",
            "Category": "Activities",
            "Rate / Unit": f"₹{activities_per_person_day:,.0f} / person / day",
            "Estimated amount (INR)": round(total_activities),
            "Share": f"{(total_activities / estimated_total):.0%}",
            "Mandatory": False,
            "Notes": "Museums, entry tickets, and viewpoints",
        },
        {
            "Expense": "Emergency & Forex Buffer",
            "Category": "Contingency",
            "Rate / Unit": f"{emergency_rate:.0%} of total trip cost",
            "Estimated amount (INR)": round(total_emergency_reserve),
            "Share": f"{(total_emergency_reserve / estimated_total):.0%}",
            "Mandatory": True,
            "Notes": "Forex markup, card fees, unexpected expenses",
        },
    ])

    return {
        "destination": dest_key,
        "country": country_norm if not is_domestic else "India",
        "is_domestic": is_domestic,
        "currency_code": benchmark.get("currency_code", "INR"),
        "currency_symbol": benchmark.get("currency_symbol", "₹"),
        "days": days,
        "nights": nights,
        "travellers": travellers,
        "rooms": rooms,
        "tier": tier,
        "estimated_total_cost": estimated_total,
        "cost_per_person": cost_per_person,
        "cost_per_person_day": cost_per_person_day,
        "flight_or_transit_per_person": flight_or_transit_per_person,
        "total_flights": total_flights_or_transit,
        "total_visa_insurance": total_visa_insurance,
        "total_accommodation": total_accommodation,
        "total_food": total_food,
        "total_local_transit": total_local_transit,
        "total_activities": total_activities,
        "total_emergency_reserve": total_emergency_reserve,
        "items": items,
        "benchmark": benchmark,
        "available_transport_options": transport_options,
        "own_vehicle_feasibility": get_own_vehicle_feasibility(dest_key, country_norm, starting_location, travellers),
        "selected_transport_option": chosen_transport,
    }


def analyze_budget_feasibility(user_budget: float, real_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare the user's allocated budget with the realistic market cost.
    Generates comprehensive feasibility diagnosis, deficit/surplus analysis,
    and helpful real-world guidance.
    """
    user_budget = float(user_budget)
    estimated_cost = float(real_plan["estimated_total_cost"])
    travellers = int(real_plan["travellers"])
    days = int(real_plan["days"])
    destination = real_plan["destination"]
    country = real_plan["country"]
    is_domestic = real_plan["is_domestic"]
    total_flights = real_plan["total_flights"]

    shortfall = estimated_cost - user_budget
    coverage_pct = (user_budget / estimated_cost) * 100 if estimated_cost > 0 else 100

    # Flight comparison
    flights_exceed_budget = total_flights > user_budget
    flights_share_of_user_budget = (total_flights / user_budget) * 100 if user_budget > 0 else 0

    if coverage_pct >= 95:
        status = "FEASIBLE"
        badge_label = "🟢 Budget Feasible & Well-Covered"
        color = "success"
        headline = f"Your ₹{user_budget:,.0f} budget is fully sufficient for {destination}, {country}!"
        summary = (
            f"A realistic trip for {travellers} traveller{'s' if travellers > 1 else ''} "
            f"for {days} day(s) costs approximately ₹{estimated_cost:,.0f}. "
            f"You have a comfortable buffer of ₹{abs(shortfall):,.0f} for upgrades or special dining."
            if shortfall <= 0 else
            f"A realistic trip costs approx ₹{estimated_cost:,.0f}. Your budget is very close and fully manageable."
        )
    elif coverage_pct >= 70:
        status = "TIGHT"
        badge_label = "🟡 Tight Budget / Backpacker Mode Required"
        color = "warning"
        headline = f"Your ₹{user_budget:,.0f} budget is tight for {destination}, {country} (Deficit: ₹{shortfall:,.0f})"
        summary = (
            f"Standard market rates estimate ₹{estimated_cost:,.0f} for this itinerary. "
            f"Your budget covers {coverage_pct:.0f}% of standard expenses. "
            f"This trip is feasible ONLY if you choose budget hostel dorms, street food, "
            f"and book flight discounts well in advance."
        )
    else:
        status = "CRITICAL_DEFICIT"
        badge_label = "🔴 Infeasible / Insufficient Budget"
        color = "error"
        headline = f"Trip Infeasible with ₹{user_budget:,.0f}: Severe Budget Deficit of ₹{shortfall:,.0f}"

        if not is_domestic and flights_exceed_budget:
            summary = (
                f"Roundtrip international flights alone from India to {country} cost approximately "
                f"₹{total_flights:,.0f}, which exceeds your ENTIRE budget of ₹{user_budget:,.0f} by "
                f"₹{(total_flights - user_budget):,.0f} before spending anything on hotels, food, local transport, or visa! "
                f"Your budget covers only {coverage_pct:.0f}% of the realistic trip cost (₹{estimated_cost:,.0f})."
            )
        elif not is_domestic:
            summary = (
                f"An international trip to {destination}, {country} for {days} days requires at least "
                f"₹{estimated_cost:,.0f}. Your budget of ₹{user_budget:,.0f} covers only {coverage_pct:.0f}% "
                f"of realistic expenses, leaving a deficit of ₹{shortfall:,.0f}."
            )
        else:
            summary = (
                f"A {days}-day trip to {destination} for {travellers} traveller{'s' if travellers > 1 else ''} "
                f"typically requires ₹{estimated_cost:,.0f}. You have a shortfall of ₹{shortfall:,.0f}."
            )

    return {
        "status": status,
        "badge_label": badge_label,
        "color": color,
        "headline": headline,
        "summary": summary,
        "user_budget": user_budget,
        "estimated_cost": estimated_cost,
        "shortfall": shortfall,
        "coverage_pct": round(coverage_pct, 1),
        "flights_exceed_budget": flights_exceed_budget,
        "total_flights": total_flights,
        "flights_share_of_user_budget": round(flights_share_of_user_budget, 1),
    }


def get_alternative_destinations(user_budget: float, days: int, travellers: int) -> list:
    """
    Find authentic destinations that can be comfortably afforded with the user's budget.
    """
    suggestions = []
    candidates = [
        ("Munnar", "Kerala", "India"),
        ("Wayanad", "Kerala", "India"),
        ("Varkala", "Kerala", "India"),
        ("Kochi", "Kerala", "India"),
        ("Alleppey", "Kerala", "India"),
        ("Goa", "Goa", "India"),
        ("Gokarna", "Karnataka", "India"),
        ("Ooty", "Tamil Nadu", "India"),
        ("Jaipur", "Rajasthan", "India"),
    ]

    for dest, state, ctry in candidates:
        plan = calculate_real_trip_budget(dest, ctry, days, travellers, tier="standard")
        cost = plan["estimated_total_cost"]
        if cost <= user_budget * 1.05:
            suggestions.append({
                "destination": dest,
                "region": f"{state}, India",
                "estimated_cost": cost,
                "budget_surplus": user_budget - cost,
                "savings_pct": round(((user_budget - cost) / user_budget) * 100) if user_budget > cost else 0
            })

    suggestions.sort(key=lambda x: x["estimated_cost"])
    return suggestions[:4]


def get_international_vs_domestic_comparison(
    days: int,
    travellers: int,
    intl_destination: str = "Tokyo",
    intl_country: str = "Japan",
    domestic_destination: str = "Goa"
) -> Dict[str, Any]:
    """
    Generate a direct side-by-side comparison explaining why an international trip
    costs drastically more than a domestic trip in India.
    """
    intl_plan = calculate_real_trip_budget(intl_destination, intl_country, days, travellers, tier="standard")
    dom_plan = calculate_real_trip_budget(domestic_destination, "India", days, travellers, tier="standard")

    comparison_rows = [
        {
            "Expense Category": "Intercity Transport / Flights",
            f"Domestic ({domestic_destination}, India)": f"₹{dom_plan['total_flights']:,.0f} (Train / Dom. Flight)",
            f"International ({intl_destination}, {intl_country})": f"₹{intl_plan['total_flights']:,.0f} (Intl. Flight)",
            "Why it differs": "Cross-continental jet fuel, airport international fees, airline taxes."
        },
        {
            "Expense Category": "Accommodation",
            f"Domestic ({domestic_destination}, India)": f"₹{dom_plan['total_accommodation']:,.0f} ({dom_plan['nights']} nights)",
            f"International ({intl_destination}, {intl_country})": f"₹{intl_plan['total_accommodation']:,.0f} ({intl_plan['nights']} nights)",
            "Why it differs": f"Real estate costs in {intl_country} and currency exchange rates."
        },
        {
            "Expense Category": "Food & Dining",
            f"Domestic ({domestic_destination}, India)": f"₹{dom_plan['total_food']:,.0f} ({days} days)",
            f"International ({intl_destination}, {intl_country})": f"₹{intl_plan['total_food']:,.0f} ({days} days)",
            "Why it differs": f"Local purchasing power and cost of meals in foreign currency."
        },
        {
            "Expense Category": "Local Commute",
            f"Domestic ({domestic_destination}, India)": f"₹{dom_plan['total_local_transit']:,.0f}",
            f"International ({intl_destination}, {intl_country})": f"₹{intl_plan['total_local_transit']:,.0f}",
            "Why it differs": "Foreign metro systems, train tariffs, and taxi base fares."
        },
        {
            "Expense Category": "Visa & Insurance",
            f"Domestic ({domestic_destination}, India)": "₹0 (Free / No Visa)",
            f"International ({intl_destination}, {intl_country})": f"₹{intl_plan['total_visa_insurance']:,.0f}",
            "Why it differs": "Mandatory visa processing and international travel medical cover."
        },
        {
            "Expense Category": "Total Estimated Trip Cost",
            f"Domestic ({domestic_destination}, India)": f"₹{dom_plan['estimated_total_cost']:,.0f}",
            f"International ({intl_destination}, {intl_country})": f"₹{intl_plan['estimated_total_cost']:,.0f}",
            "Why it differs": f"International trip requires {intl_plan['estimated_total_cost'] / dom_plan['estimated_total_cost']:.1f}x higher budget!"
        }
    ]

    return {
        "intl_destination": intl_destination,
        "intl_country": intl_country,
        "domestic_destination": domestic_destination,
        "intl_total": intl_plan["estimated_total_cost"],
        "dom_total": dom_plan["estimated_total_cost"],
        "ratio": round(intl_plan["estimated_total_cost"] / dom_plan["estimated_total_cost"], 1),
        "rows": comparison_rows
    }
