import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from datetime import datetime


# Open-Meteo is free and requires no API key
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}

WEATHER_ICONS = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️",
    51: "🌦️", 53: "🌦️", 55: "🌧️",
    56: "🌨️", 57: "🌨️",
    61: "🌧️", 63: "🌧️", 65: "⛈️",
    66: "🌨️", 67: "🌨️",
    71: "🌨️", 73: "❄️", 75: "❄️", 77: "❄️",
    80: "🌦️", 81: "🌧️", 82: "⛈️",
    85: "🌨️", 86: "🌨️",
    95: "⛈️", 96: "⛈️", 99: "⛈️",
}

WIND_DIRS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
             "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


def fetch_json(url):
    req = Request(url, headers={"User-Agent": "WeatherApp/1.0"})
    with urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def geocode(city, count=5):
    url = f"{GEOCODE_URL}?" + urlencode({
        "name": city,
        "count": count,
        "language": "en",
        "format": "json"
    })

    data = fetch_json(url)
    results = data.get("results", [])

    locations = []
    for r in results:
        locations.append({
            "name": r.get("name", ""),
            "country": r.get("country", ""),
            "admin1": r.get("admin1", ""),
            "lat": r.get("latitude"),
            "lon": r.get("longitude"),
            "timezone": r.get("timezone", "auto"),
            "population": r.get("population", 0)
        })

    return locations


def get_weather(lat, lon, days=3, units="metric"):
    temp_unit = "celsius" if units == "metric" else "fahrenheit"
    wind_unit = "kmh" if units == "metric" else "mph"
    precip_unit = "mm" if units == "metric" else "inch"

    url = f"{FORECAST_URL}?" + urlencode({
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m,pressure_msl",
        "hourly": "temperature_2m,precipitation_probability,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,precipitation_probability_max,wind_speed_10m_max",
        "timezone": "auto",
        "forecast_days": days,
        "temperature_unit": temp_unit,
        "wind_speed_unit": wind_unit,
        "precipitation_unit": precip_unit
    })

    return fetch_json(url)


def wind_dir_name(degrees):
    if degrees is None:
        return ""
    idx = int((degrees + 11.25) / 22.5) % 16
    return WIND_DIRS[idx]


def format_current(data, units="metric"):
    current = data.get("current", {})
    if not current:
        return "No current data."

    temp_unit = "°C" if units == "metric" else "°F"
    wind_unit = "km/h" if units == "metric" else "mph"

    code = current.get("weather_code", 0)
    condition = WEATHER_CODES.get(code, "Unknown")
    icon = WEATHER_ICONS.get(code, "")

    lines = []
    lines.append(f"  {icon}  {condition}")
    lines.append("")
    lines.append(f"  Temperature:    {current.get('temperature_2m')}{temp_unit}")
    lines.append(f"  Feels like:     {current.get('apparent_temperature')}{temp_unit}")
    lines.append(f"  Humidity:       {current.get('relative_humidity_2m')}%")
    lines.append(f"  Wind:           {current.get('wind_speed_10m')} {wind_unit} {wind_dir_name(current.get('wind_direction_10m'))}")
    lines.append(f"  Pressure:       {current.get('pressure_msl')} hPa")
    lines.append(f"  Precipitation:  {current.get('precipitation')} mm")

    return "\n".join(lines)


def format_daily(data, units="metric"):
    daily = data.get("daily", {})
    if not daily:
        return "No forecast data."

    temp_unit = "°C" if units == "metric" else "°F"
    precip_unit = "mm" if units == "metric" else "in"

    dates = daily.get("time", [])
    codes = daily.get("weather_code", [])
    tmax = daily.get("temperature_2m_max", [])
    tmin = daily.get("temperature_2m_min", [])
    sunrise = daily.get("sunrise", [])
    sunset = daily.get("sunset", [])
    precip = daily.get("precipitation_sum", [])
    precip_prob = daily.get("precipitation_probability_max", [])
    wind_max = daily.get("wind_speed_10m_max", [])

    lines = []
    lines.append(f"  {'Date':<14}{'Condition':<22}{'Low/High':<16}{'Rain':<12}{'Wind':<10}")

    for i, date_str in enumerate(dates):
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = d.strftime("%a %b %d")
        except ValueError:
            day_name = date_str

        code = codes[i] if i < len(codes) else 0
        condition = WEATHER_CODES.get(code, "Unknown")
        icon = WEATHER_ICONS.get(code, "")

        lo = tmin[i] if i < len(tmin) else "?"
        hi = tmax[i] if i < len(tmax) else "?"

        rain = precip[i] if i < len(precip) else 0
        prob = precip_prob[i] if i < len(precip_prob) else 0

        wind = wind_max[i] if i < len(wind_max) else "?"

        lines.append(
            f"  {day_name:<14}{icon} {condition:<18}{lo:>4}/{hi:<4}{temp_unit}   "
            f"{rain}{precip_unit} ({prob}%)   {wind}"
        )

    return "\n".join(lines)


def format_hourly(data, hours=12, units="metric"):
    hourly = data.get("hourly", {})
    if not hourly:
        return "No hourly data."

    temp_unit = "°C" if units == "metric" else "°F"

    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    codes = hourly.get("weather_code", [])
    precip = hourly.get("precipitation_probability", [])

    now = datetime.now()

    lines = [f"  {'Time':<8}{'Temp':<10}{'Rain %':<10}{'Condition'}"]
    shown = 0

    for i, t_str in enumerate(times):
        try:
            t = datetime.fromisoformat(t_str)
        except ValueError:
            continue

        if t < now:
            continue

        code = codes[i] if i < len(codes) else 0
        condition = WEATHER_CODES.get(code, "")
        icon = WEATHER_ICONS.get(code, "")
        temp = temps[i] if i < len(temps) else "?"
        prob = precip[i] if i < len(precip) else "?"

        lines.append(f"  {t.strftime('%H:%M'):<8}{temp}{temp_unit:<7}{prob}%{'':<6}{icon} {condition}")
        shown += 1

        if shown >= hours:
            break

    return "\n".join(lines)


def print_report(location, data, units="metric", show_hourly=False):
    name = location.get("name", "Unknown")
    country = location.get("country", "")
    admin = location.get("admin1", "")

    place = name
    if admin and admin != name:
        place += f", {admin}"
    if country:
        place += f", {country}"

    print()
    print("=" * 70)
    print(f"  Weather for {place}")
    print(f"  ({location['lat']:.2f}, {location['lon']:.2f})  Timezone: {data.get('timezone', 'auto')}")
    print("=" * 70)

    print("\nCURRENT CONDITIONS")
    print("-" * 70)
    print(format_current(data, units))

    print("\nFORECAST")
    print("-" * 70)
    print(format_daily(data, units))

    if show_hourly:
        print("\nNEXT 12 HOURS")
        print("-" * 70)
        print(format_hourly(data, 12, units))

    print()


def save_report(location, data, path, units="metric"):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"location": location, "weather": data, "units": units}, f, indent=2)
        print(f"Saved raw data: {path}")
    except OSError as e:
        print(f"Save failed: {e}")


def get_ip_location():
    try:
        req = Request("https://ipinfo.io/json", headers={"User-Agent": "WeatherApp/1.0"})
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        loc = data.get("loc", "")
        if "," in loc:
            lat, lon = loc.split(",")
            return {
                "name": data.get("city", "Unknown"),
                "country": data.get("country", ""),
                "admin1": data.get("region", ""),
                "lat": float(lat),
                "lon": float(lon),
                "timezone": data.get("timezone", "auto")
            }
    except Exception:
        pass
    return None


def pick_location(city):
    locations = geocode(city)

    if not locations:
        print(f"No results for '{city}'.")
        return None

    if len(locations) == 1:
        return locations[0]

    print(f"\nFound {len(locations)} matches:")
    for i, loc in enumerate(locations, 1):
        pop = f" (pop {loc['population']:,})" if loc.get("population") else ""
        admin = f", {loc['admin1']}" if loc.get("admin1") and loc["admin1"] != loc["name"] else ""
        print(f"  {i}. {loc['name']}{admin}, {loc['country']}{pop}")

    try:
        idx = int(input("\nPick a number (default 1): ").strip() or "1") - 1
    except ValueError:
        idx = 0

    if 0 <= idx < len(locations):
        return locations[idx]

    return locations[0]


def interactive_mode():
    print("=== Weather App ===\n")
    print("Powered by Open-Meteo (no API key needed)\n")

    print("1. Search by city")
    print("2. Detect my location (via IP)")
    print("3. Use coordinates directly")

    choice = input("\nChoose (default 1): ").strip() or "1"

    if choice == "2":
        print("\nDetecting location...")
        location = get_ip_location()

        if not location:
            print("Could not detect location.")
            return

        print(f"Detected: {location['name']}, {location['country']}")
    elif choice == "3":
        try:
            lat = float(input("Latitude: ").strip())
            lon = float(input("Longitude: ").strip())
        except ValueError:
            print("Invalid coordinates.")
            return

        location = {
            "name": f"({lat}, {lon})",
            "country": "",
            "admin1": "",
            "lat": lat,
            "lon": lon,
            "timezone": "auto"
        }
    else:
        city = input("City name: ").strip()
        if not city:
            return
        location = pick_location(city)

    if not location:
        return

    units_input = input("Units (metric/imperial, default metric): ").strip().lower()
    units = "imperial" if units_input == "imperial" else "metric"

    days_input = input("Forecast days (1-16, default 5): ").strip() or "5"
    try:
        days = min(16, max(1, int(days_input)))
    except ValueError:
        days = 5

    show_hourly = input("Show hourly forecast? (y/n): ").strip().lower() == "y"

    print(f"\nFetching weather for {location['name']}...")

    try:
        data = get_weather(location["lat"], location["lon"], days=days, units=units)
        print_report(location, data, units=units, show_hourly=show_hourly)
    except Exception as e:
        print(f"Failed: {e}")
        return

    if input("Save raw data? (y/n): ").strip().lower() == "y":
        path = input("Path (default weather.json): ").strip() or "weather.json"
        save_report(location, data, path, units)


def main():
    parser = argparse.ArgumentParser(description="Weather App (Open-Meteo)")
    parser.add_argument("city", nargs="?", help="City name")
    parser.add_argument("-c", "--coords", nargs=2, type=float, metavar=("LAT", "LON"),
                        help="Use coordinates instead of city")
    parser.add_argument("-u", "--units", default="metric", choices=["metric", "imperial"])
    parser.add_argument("-d", "--days", type=int, default=5, help="Forecast days (1-16)")
    parser.add_argument("-H", "--hourly", action="store_true", help="Show hourly forecast")
    parser.add_argument("-o", "--output", help="Save raw JSON to file")
    parser.add_argument("--here", action="store_true", help="Auto-detect location via IP")

    args = parser.parse_args()

    if args.coords:
        location = {
            "name": f"({args.coords[0]}, {args.coords[1]})",
            "country": "",
            "admin1": "",
            "lat": args.coords[0],
            "lon": args.coords[1],
            "timezone": "auto"
        }
    elif args.here:
        print("Detecting location...")
        location = get_ip_location()
        if not location:
            print("Detection failed. Try specifying a city.")
            return
        print(f"Detected: {location['name']}, {location['country']}")
    elif args.city:
        location = pick_location(args.city)
        if not location:
            return
    else:
        interactive_mode()
        return

    days = min(16, max(1, args.days))

    try:
        data = get_weather(location["lat"], location["lon"], days=days, units=args.units)
        print_report(location, data, units=args.units, show_hourly=args.hourly)

        if args.output:
            save_report(location, data, args.output, args.units)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()