import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from trip_planner import (
    create_budget_breakdown,
    create_itinerary,
    estimate_trip_expenses
)

# Find the project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Load the cleaned dataset
DATA_PATH = PROJECT_DIR / "data" / "destinations_cleaned.csv"


def load_destinations():
    """Load the cleaned destination dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Cleaned dataset not found. "
            "Run data_preprocessing.py first."
        )

    return pd.read_csv(DATA_PATH)


def build_recommendation_model(df):
    """Create a content-based recommendation model."""

    df = df.copy()

    # Combine destination characteristics
    df["features"] = (
        df["category"].fillna("").astype(str) + " "
        + df["ideal_for"].fillna("").astype(str) + " "
        + df["state"].fillna("").astype(str) + " "
        + df["description"].fillna("").astype(str)
    )

    # Convert text into numerical feature vectors
    vectorizer = TfidfVectorizer(stop_words="english")

    feature_matrix = vectorizer.fit_transform(df["features"])

    return df, vectorizer, feature_matrix



def recommend_destinations(
    df,
    vectorizer,
    feature_matrix,
    budget,
    days,
    travellers,
    travel_type,
    preferred_category,
    top_n=5,
):
    """Recommend affordable destinations using trip preferences."""

    # 1. Validate inputs
    if budget <= 0 or days <= 0 or travellers <= 0:
        raise ValueError(
            "Budget, days, and travellers must be greater than zero."
        )

    travel_type = str(travel_type).strip().casefold()
    preferred_category = str(
        preferred_category or "any"
    ).strip().casefold()

    valid_travel_types = {
        "solo", "family", "couple", "friends"
    }

    if travel_type not in valid_travel_types:
        raise ValueError(
            "Travel type must be Solo, Family, Couple, or Friends."
        )

    # 2. Prepare destination data
    results = df.copy()

    daily_budget = pd.to_numeric(
        results["estimated_daily_budget"],
        errors="coerce",
    )

    minimum_days = pd.to_numeric(
        results["minimum_days"],
        errors="coerce",
    )

    results["estimated_daily_budget"] = daily_budget
    results["minimum_days"] = minimum_days

    # Assumes estimated_daily_budget is the estimated cost
    # per person per day. Confirm this matches your dataset.
    results["estimated_total_cost"] = (
        daily_budget * days * travellers
    )

    # 3. Check budget and duration
    results["budget_suitable"] = (
        results["estimated_total_cost"] <= budget
    )

    results["duration_suitable"] = (
        minimum_days <= days
    )

    # 4. Match categories
    results["category_match"] = (
        results["category"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
        .eq(preferred_category)
    )

    # "Any" means the user has no category preference.
    if preferred_category == "any":
        results["category_match"] = True

    # 5. Match traveller type
    ideal_for = (
        results["ideal_for"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
    )

    if travel_type == "solo":
        # Solo is supported, but the dataset does not yet
        # contain a dedicated solo-travel suitability field.
        results["travel_type_match"] = True

    else:
        results["travel_type_match"] = ideal_for.apply(
            lambda value: (
                travel_type in {
                    part.strip()
                    for part in value.replace("&", ",").split(",")
                }
            )
        )

    # 6. Keep affordable destinations with sufficient duration
    eligible = results[
        results["budget_suitable"]
        & results["duration_suitable"]
    ].copy()

    if eligible.empty:
        return eligible

    # 7. Calculate content-based similarity
    user_preferences = (
        f"{preferred_category} {travel_type}"
    )

    user_vector = vectorizer.transform(
        [user_preferences]
    )

    similarities = cosine_similarity(
        user_vector,
        feature_matrix,
    ).flatten()

    similarity_by_index = pd.Series(
        similarities,
        index=df.index,
    )

    eligible["similarity_score"] = similarity_by_index.loc[
        eligible.index
    ]

    # 8. Score destinations
    eligible["recommendation_score"] = (
        0.40 * eligible["similarity_score"]
        + 0.35 * eligible["category_match"].astype(float)
        + 0.25 * eligible["travel_type_match"].astype(float)
    )

    # 9. Rank suitable destinations
    eligible = eligible.sort_values(
        by=[
            "recommendation_score",
            "similarity_score",
            "estimated_total_cost",
        ],
        ascending=[False, False, True],
    )

    return eligible.head(top_n)

def main():
    # Load data
    destinations = load_destinations()

    # Build the model
    df, vectorizer, feature_matrix = (
        build_recommendation_model(destinations)
    )

    print("\nWelcome to Smart Travel Recommendation System!")
    print("Explore destinations across India.\n")

    # Get user inputs
    budget = float(input("Enter your total budget (INR): "))
    days = int(input("Enter the number of travel days: "))
    travellers = int(input("Enter the number of travellers: "))

    travel_type = input(
        "Travel type (Family/Couple/Friends): "
    ).strip()

    preferred_category = input(
        "Preferred category (e.g., Hills and Nature, Beach, "
        "City and Culture): "
    ).strip()
    preferred_category = preferred_category.strip().casefold()

    if preferred_category in ["hill and nature", "hills and nature"]:
     preferred_category = "hills and nature"
    elif preferred_category == "beach":
     preferred_category = "beach"
    elif preferred_category == "city and culture":
     preferred_category = "city and culture"

    # Generate recommendations
    recommendations = recommend_destinations(
        df=df,
        vectorizer=vectorizer,
        feature_matrix=feature_matrix,
        budget=budget,
        days=days,
        travellers=travellers,
        travel_type=travel_type,
        preferred_category=preferred_category,
    )
    if recommendations.empty:
        return
    
    # Display results
    print("\nRecommended Destinations")
    print("=" * 75)

    for _, row in recommendations.iterrows():
        print(f"\nDestination: {row['destination']}")
        print(f"State: {row['state']}")
        print(f"Category: {row['category']}")
        print(f"Description: {row['description']}")

        print(
            "Estimated total cost: "
            f"₹{row['estimated_total_cost']:,.0f}"
        )

        print(
            "Budget suitable: "
            f"{'Yes' if row['budget_suitable'] else 'No'}"
        )

        print(
            "Duration suitable: "
            f"{'Yes' if row['duration_suitable'] else 'No'}"
        )

        print(
            f"Preference similarity: "
            f"{row['similarity_score']:.2f}"
        )
        print(
    f"Recommendation score: "
    f"{row['recommendation_score']:.4f}"
)

        print(
    "Travel group match: "
    f"{'Yes' if row['travel_type_match'] else 'No'}"
)

        print(f"Best season: {row['best_season']}")


    # Let the user choose a recommended destination
    print("\nCHOOSE YOUR DESTINATION")
    print("=" * 40)

    destination_list = recommendations["destination"].tolist()

    for index, destination in enumerate(destination_list, start=1):
        print(f"{index}. {destination}")

    try:
        choice = int(input("\nEnter destination number: "))

        if choice < 1 or choice > len(destination_list):
            print("Invalid destination number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    selected_destination = destination_list[choice - 1]

    print(f"\nYou selected: {selected_destination}")

    # Show the budget allocation
    create_budget_breakdown(budget, days, travellers)

    # Estimate destination-specific expenses
    estimated_cost = estimate_trip_expenses(
        selected_destination,
        days,
        travellers
    )

    # Check whether estimated expenses fit the budget
    print("\nBUDGET CHECK")
    print("-" * 40)

    if estimated_cost <= budget:
        print("The estimated trip cost is within your budget.")
        print(f"Remaining budget: ₹{budget - estimated_cost:,.0f}")
    else:
        print("Warning: The estimated trip cost exceeds your budget.")
        print(f"Additional budget needed: ₹{estimated_cost - budget:,.0f}")

    # Generate the itinerary
    create_itinerary(selected_destination, days)

if __name__ == "__main__":
    main()