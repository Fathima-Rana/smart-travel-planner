
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def search_destination(destination, country=None):
    """Search for destinations worldwide, optionally filtering by country."""

    try:
        response = requests.get(
            GEOCODING_URL,
            params={
                "name": destination,
                "count": 10,
                "language": "en",
                "format": "json",
            },
            timeout=15,
        )

        response.raise_for_status()
        results = response.json().get("results", [])

        if country:
            results = [
                place
                for place in results
                if place.get("country", "").casefold()
                == country.casefold()
            ]

        destinations = []

        for place in results:
            destinations.append({
                "name": place.get("name"),
                "country": place.get("country", "Unknown"),
                "latitude": place.get("latitude"),
                "longitude": place.get("longitude"),
            })

        return destinations

    except (requests.RequestException, ValueError) as error:
        print(f"Destination search failed: {error}")
        return []


def get_destination_weather(destination, country=None):
    """Fetch current weather and a short forecast for a destination."""

    places = search_destination(destination, country)

    if not places:
        return {
            "destination": destination,
            "error": (
                f"No matching destination found for {destination}"
                + (f", {country}" if country else "")
                + ". Check the city and country names."
            ),
        }

    # Use the first matching destination.
    place = places[0]

    try:
        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,wind_speed_10m",
                "daily": "precipitation_probability_max",
                "forecast_days": 3,
                "timezone": "auto",
            },
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        current_data = data.get("current", {})
        daily_data = data.get("daily", {})

        return {
            "destination": f'{place["name"]}, {place["country"]}',
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current_weather": {
                "temperature_2m": current_data.get("temperature_2m"),
                "wind_speed_10m": current_data.get("wind_speed_10m"),
            },
            "daily_forecast": {
                "time": daily_data.get("time", []),
                "precipitation_probability_max": daily_data.get(
                    "precipitation_probability_max", []
                ),
            },
        }

    except (requests.RequestException, ValueError) as error:
        return {
            "destination": f'{place["name"]}, {place["country"]}',
            "error": f"Weather information is unavailable: {error}",
        }


def get_travel_advice(weather):
    """Provide simple travel advice based on available weather data."""

    if "error" in weather:
        return "Weather information is currently unavailable."

    current = weather.get("current_weather", {})
    daily = weather.get("daily_forecast", {})

    temperature = current.get("temperature_2m")
    wind = current.get("wind_speed_10m")
    rain_chance = daily.get("precipitation_probability_max", [])

    if temperature is None or wind is None:
        return "Not enough weather data to give advice."

    valid_rain_values = [
        chance for chance in rain_chance
        if isinstance(chance, (int, float))
    ]

    max_rain_chance = (
        max(valid_rain_values) if valid_rain_values else None
    )

    if temperature >= 40 or temperature <= 0 or wind >= 50:
        return (
            "Weather may be uncomfortable or challenging. "
            "Check local weather alerts before travelling."
        )

    if max_rain_chance is not None and max_rain_chance >= 70:
        return (
            "Rain may affect outdoor plans. Carry rain protection "
            "and check the forecast before travelling."
        )

    if temperature > 35 or temperature < 5 or wind >= 30:
        return (
            "Conditions may require extra preparation. "
            "Check the forecast and plan activities accordingly."
        )

    return (
        "Current conditions look generally suitable for travel. "
        "Check the forecast for your travel dates before leaving."
    )


if __name__ == "__main__":
    # Test worldwide destination search and live weather.
    destination_name = "Tokyo"
    country_name = "Japan"

    weather = get_destination_weather(
        destination_name,
        country_name,
    )

    print("\nDestination:", weather.get("destination", "Unknown"))

    if "error" in weather:
        print(weather["error"])
    else:
        current = weather.get("current_weather", {})
        daily = weather.get("daily_forecast", {})

        print(
            "Temperature:",
            current.get("temperature_2m"),
            "°C",
        )
        print(
            "Wind speed:",
            current.get("wind_speed_10m"),
            "km/h",
        )

        print("\nRain forecast:")

        dates = daily.get("time", [])
        rain_chances = daily.get("precipitation_probability_max", [])

        for date, chance in zip(dates, rain_chances):
            print(f"{date}: {chance}% chance of precipitation")

        advice = get_travel_advice(weather)
        print("\nTravel advice:", advice)
