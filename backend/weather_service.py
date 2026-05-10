"""
weather_service.py
আবহাওয়া সার্ভিস — Open-Meteo API ব্যবহার করে বাংলাদেশের ৬৪ জেলার আবহাওয়া তথ্য
Weather service using Open-Meteo API for all 64 districts of Bangladesh
"""

import httpx
from typing import Optional

# Open-Meteo API (বিনামূল্যে, কোনো API key দরকার নেই)
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# ৬৪ জেলার coordinates (latitude, longitude)
# All 64 districts of Bangladesh with GPS coordinates
BANGLADESH_DISTRICTS: dict[str, dict] = {
    # ঢাকা বিভাগ
    "ঢাকা": {"lat": 23.8103, "lon": 90.4125, "en": "Dhaka"},
    "গাজীপুর": {"lat": 23.9999, "lon": 90.4203, "en": "Gazipur"},
    "নারায়ণগঞ্জ": {"lat": 23.6238, "lon": 90.4998, "en": "Narayanganj"},
    "মানিকগঞ্জ": {"lat": 23.8630, "lon": 90.0085, "en": "Manikganj"},
    "মুন্সিগঞ্জ": {"lat": 23.5422, "lon": 90.5305, "en": "Munshiganj"},
    "নরসিংদী": {"lat": 23.9324, "lon": 90.7149, "en": "Narsingdi"},
    "কিশোরগঞ্জ": {"lat": 24.4447, "lon": 90.7766, "en": "Kishoreganj"},
    "ময়মনসিংহ": {"lat": 24.7471, "lon": 90.4203, "en": "Mymensingh"},
    "শেরপুর": {"lat": 25.0191, "lon": 90.0152, "en": "Sherpur"},
    "নেত্রকোণা": {"lat": 24.8848, "lon": 90.7265, "en": "Netrokona"},
    "জামালপুর": {"lat": 24.9375, "lon": 89.9371, "en": "Jamalpur"},
    "টাঙ্গাইল": {"lat": 24.2513, "lon": 89.9167, "en": "Tangail"},
    "ফরিদপুর": {"lat": 23.6070, "lon": 89.8429, "en": "Faridpur"},
    "গোপালগঞ্জ": {"lat": 23.0051, "lon": 89.8266, "en": "Gopalganj"},
    "মাদারীপুর": {"lat": 23.1643, "lon": 90.1982, "en": "Madaripur"},
    "রাজবাড়ী": {"lat": 23.7575, "lon": 89.6444, "en": "Rajbari"},
    "শরীয়তপুর": {"lat": 23.2223, "lon": 90.4350, "en": "Shariatpur"},

    # চট্টগ্রাম বিভাগ
    "চট্টগ্রাম": {"lat": 22.3569, "lon": 91.7832, "en": "Chittagong"},
    "কক্সবাজার": {"lat": 21.4272, "lon": 92.0058, "en": "Cox's Bazar"},
    "রাঙ্গামাটি": {"lat": 22.6423, "lon": 92.1789, "en": "Rangamati"},
    "বান্দরবান": {"lat": 22.1953, "lon": 92.2184, "en": "Bandarban"},
    "খাগড়াছড়ি": {"lat": 23.1193, "lon": 91.9847, "en": "Khagrachhari"},
    "ফেনী": {"lat": 23.0159, "lon": 91.3976, "en": "Feni"},
    "নোয়াখালী": {"lat": 22.8696, "lon": 91.0995, "en": "Noakhali"},
    "লক্ষ্মীপুর": {"lat": 22.9426, "lon": 90.8412, "en": "Lakshmipur"},
    "কুমিল্লা": {"lat": 23.4607, "lon": 91.1809, "en": "Comilla"},
    "ব্রাহ্মণবাড়িয়া": {"lat": 23.9608, "lon": 91.1115, "en": "Brahmanbaria"},
    "চাঁদপুর": {"lat": 23.2332, "lon": 90.6602, "en": "Chandpur"},

    # সিলেট বিভাগ
    "সিলেট": {"lat": 24.8949, "lon": 91.8687, "en": "Sylhet"},
    "মৌলভীবাজার": {"lat": 24.4829, "lon": 91.7774, "en": "Moulvibazar"},
    "হবিগঞ্জ": {"lat": 24.3746, "lon": 91.4158, "en": "Habiganj"},
    "সুনামগঞ্জ": {"lat": 25.0658, "lon": 91.3950, "en": "Sunamganj"},

    # রাজশাহী বিভাগ
    "রাজশাহী": {"lat": 24.3745, "lon": 88.6042, "en": "Rajshahi"},
    "নওগাঁ": {"lat": 24.8465, "lon": 88.9312, "en": "Naogaon"},
    "নাটোর": {"lat": 24.4104, "lon": 89.0000, "en": "Natore"},
    "চাঁপাইনবাবগঞ্জ": {"lat": 24.5965, "lon": 88.2760, "en": "Chapai Nawabganj"},
    "পাবনা": {"lat": 24.0064, "lon": 89.2372, "en": "Pabna"},
    "সিরাজগঞ্জ": {"lat": 24.4534, "lon": 89.7008, "en": "Sirajganj"},
    "বগুড়া": {"lat": 24.8465, "lon": 89.3720, "en": "Bogura"},
    "জয়পুরহাট": {"lat": 25.1001, "lon": 89.0220, "en": "Joypurhat"},

    # রংপুর বিভাগ
    "রংপুর": {"lat": 25.7439, "lon": 89.2752, "en": "Rangpur"},
    "দিনাজপুর": {"lat": 25.6279, "lon": 88.6338, "en": "Dinajpur"},
    "ঠাকুরগাঁও": {"lat": 26.0336, "lon": 88.4616, "en": "Thakurgaon"},
    "পঞ্চগড়": {"lat": 26.3407, "lon": 88.5556, "en": "Panchagarh"},
    "নীলফামারী": {"lat": 25.9316, "lon": 88.8565, "en": "Nilphamari"},
    "লালমনিরহাট": {"lat": 25.9923, "lon": 89.2847, "en": "Lalmonirhat"},
    "কুড়িগ্রাম": {"lat": 25.8073, "lon": 89.6360, "en": "Kurigram"},
    "গাইবান্ধা": {"lat": 25.3288, "lon": 89.5287, "en": "Gaibandha"},

    # খুলনা বিভাগ
    "খুলনা": {"lat": 22.8456, "lon": 89.5403, "en": "Khulna"},
    "বাগেরহাট": {"lat": 22.6602, "lon": 89.7854, "en": "Bagerhat"},
    "সাতক্ষীরা": {"lat": 22.7185, "lon": 89.0705, "en": "Satkhira"},
    "যশোর": {"lat": 23.1664, "lon": 89.2081, "en": "Jashore"},
    "ঝিনাইদহ": {"lat": 23.5448, "lon": 89.1521, "en": "Jhenaidah"},
    "নড়াইল": {"lat": 23.1724, "lon": 89.5012, "en": "Narail"},
    "মাগুরা": {"lat": 23.4876, "lon": 89.4196, "en": "Magura"},
    "কুষ্টিয়া": {"lat": 23.9014, "lon": 89.1214, "en": "Kushtia"},
    "মেহেরপুর": {"lat": 23.7621, "lon": 88.6318, "en": "Meherpur"},
    "চুয়াডাঙ্গা": {"lat": 23.6401, "lon": 88.8415, "en": "Chuadanga"},

    # বরিশাল বিভাগ
    "বরিশাল": {"lat": 22.7010, "lon": 90.3535, "en": "Barishal"},
    "পটুয়াখালী": {"lat": 22.3596, "lon": 90.3298, "en": "Patuakhali"},
    "ভোলা": {"lat": 22.6857, "lon": 90.6448, "en": "Bhola"},
    "পিরোজপুর": {"lat": 22.5840, "lon": 89.9720, "en": "Pirojpur"},
    "বরগুনা": {"lat": 22.1500, "lon": 90.1167, "en": "Barguna"},
    "ঝালকাঠি": {"lat": 22.6440, "lon": 90.1977, "en": "Jhalokathi"},
}

# WMO weather code to Bengali/English description
WMO_CODES = {
    0: {"bn": "পরিষ্কার আকাশ", "en": "Clear sky"},
    1: {"bn": "আংশিক মেঘলা", "en": "Mainly clear"},
    2: {"bn": "মেঘলা", "en": "Partly cloudy"},
    3: {"bn": "সম্পূর্ণ মেঘলা", "en": "Overcast"},
    45: {"bn": "কুয়াশা", "en": "Foggy"},
    48: {"bn": "ঘন কুয়াশা", "en": "Dense fog"},
    51: {"bn": "হালকা গুঁড়িগুঁড়ি বৃষ্টি", "en": "Light drizzle"},
    53: {"bn": "মাঝারি গুঁড়িগুঁড়ি বৃষ্টি", "en": "Moderate drizzle"},
    55: {"bn": "ভারী গুঁড়িগুঁড়ি বৃষ্টি", "en": "Dense drizzle"},
    61: {"bn": "হালকা বৃষ্টি", "en": "Slight rain"},
    63: {"bn": "মাঝারি বৃষ্টি", "en": "Moderate rain"},
    65: {"bn": "ভারী বৃষ্টি", "en": "Heavy rain"},
    71: {"bn": "হালকা তুষারপাত", "en": "Slight snow"},
    73: {"bn": "মাঝারি তুষারপাত", "en": "Moderate snow"},
    75: {"bn": "ভারী তুষারপাত", "en": "Heavy snow"},
    80: {"bn": "হালকা বৃষ্টি ঝরনা", "en": "Slight rain showers"},
    81: {"bn": "মাঝারি বৃষ্টি ঝরনা", "en": "Moderate rain showers"},
    82: {"bn": "ভারী বৃষ্টি ঝরনা", "en": "Violent rain showers"},
    95: {"bn": "বজ্রবৃষ্টি", "en": "Thunderstorm"},
    96: {"bn": "শিলাবৃষ্টি সহ বজ্রবৃষ্টি", "en": "Thunderstorm with hail"},
    99: {"bn": "ভারী শিলাবৃষ্টি সহ বজ্রবৃষ্টি", "en": "Thunderstorm with heavy hail"},
}


async def get_weather(district: str, language: str = "bn") -> dict:
    """
    একটি জেলার আবহাওয়া তথ্য এবং কৃষি পরামর্শ দেয়।
    Returns weather data and farming advice for a given district.

    Args:
        district: জেলার নাম (বাংলা বা English)
        language: 'bn' or 'en'

    Returns:
        dict with temperature, humidity, rain_probability, farming_advice, etc.
    """
    # জেলা খোঁজা — Bengali or English name match
    coords = _find_district(district)

    if coords is None:
        # ঢাকার coordinates ব্যবহার করো যদি জেলা না পাওয়া যায়
        coords = BANGLADESH_DISTRICTS["ঢাকা"]
        district_name = "ঢাকা" if language == "bn" else "Dhaka"
    else:
        district_name = district

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                OPEN_METEO_URL,
                params={
                    "latitude": coords["lat"],
                    "longitude": coords["lon"],
                    "current": [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "precipitation",
                        "weather_code",
                        "wind_speed_10m",
                        "uv_index",
                    ],
                    "daily": [
                        "precipitation_probability_max",
                        "temperature_2m_max",
                        "temperature_2m_min",
                        "precipitation_sum",
                    ],
                    "timezone": "Asia/Dhaka",
                    "forecast_days": 3,
                },
            )

        if response.status_code != 200:
            return _error_weather_response(district_name, language)

        data = response.json()
        return _parse_weather_response(data, district_name, language)

    except httpx.TimeoutException:
        return _error_weather_response(district_name, language)
    except Exception as e:
        print(f"Weather service error: {e}")
        return _error_weather_response(district_name, language)


def _find_district(district: str) -> Optional[dict]:
    """জেলার নাম দিয়ে coordinates খোঁজে — বাংলা বা English উভয় ভাষায়।"""
    # Direct Bengali match
    if district in BANGLADESH_DISTRICTS:
        return BANGLADESH_DISTRICTS[district]

    # English name match (case-insensitive)
    district_lower = district.lower()
    for key, value in BANGLADESH_DISTRICTS.items():
        if value["en"].lower() == district_lower:
            return value

    # Partial match
    for key, value in BANGLADESH_DISTRICTS.items():
        if district_lower in key.lower() or district_lower in value["en"].lower():
            return value

    return None


def _parse_weather_response(data: dict, district: str, language: str) -> dict:
    """Open-Meteo API response parse করে structured data তৈরি করে।"""
    current = data.get("current", {})
    daily = data.get("daily", {})

    temperature = round(current.get("temperature_2m", 30), 1)
    humidity = round(current.get("relative_humidity_2m", 70), 1)
    precipitation = round(current.get("precipitation", 0), 1)
    weather_code = current.get("weather_code", 0)
    wind_speed = round(current.get("wind_speed_10m", 0), 1)
    uv_index = round(current.get("uv_index", 0), 1)

    # আজকের বৃষ্টির সম্ভাবনা
    rain_probabilities = daily.get("precipitation_probability_max", [0, 0, 0])
    rain_probability = rain_probabilities[0] if rain_probabilities else 0

    # আগামীকালের তাপমাত্রা
    temp_max = daily.get("temperature_2m_max", [temperature])[0]
    temp_min = daily.get("temperature_2m_min", [temperature - 5])[0]

    # আগামী ৩ দিনের বৃষ্টির পূর্বাভাস
    forecast_rain = rain_probabilities[:3] if len(rain_probabilities) >= 3 else rain_probabilities

    # আবহাওয়ার বিবরণ
    weather_desc = WMO_CODES.get(weather_code, {"bn": "অজানা", "en": "Unknown"})
    condition = weather_desc[language if language in ["bn", "en"] else "bn"]

    # কৃষি পরামর্শ তৈরি করো
    farming_advice = _generate_farming_advice(
        temperature=temperature,
        humidity=humidity,
        rain_probability=rain_probability,
        precipitation=precipitation,
        wind_speed=wind_speed,
        uv_index=uv_index,
        language=language,
    )

    return {
        "district": district,
        "temperature": temperature,
        "temp_max": round(temp_max, 1),
        "temp_min": round(temp_min, 1),
        "humidity": humidity,
        "precipitation": precipitation,
        "rain_probability": rain_probability,
        "wind_speed": wind_speed,
        "uv_index": uv_index,
        "condition": condition,
        "forecast_rain_3day": forecast_rain,
        "farming_advice": farming_advice,
        "error": None,
    }


def _generate_farming_advice(
    temperature: float,
    humidity: float,
    rain_probability: float,
    precipitation: float,
    wind_speed: float,
    uv_index: float,
    language: str,
) -> list[str]:
    """
    আবহাওয়ার তথ্য বিশ্লেষণ করে কৃষি পরামর্শ তৈরি করে।
    Generates farming advice based on weather conditions.
    """
    advice = []

    if language == "bn":
        # বৃষ্টি সংক্রান্ত পরামর্শ
        if rain_probability >= 70:
            advice.append("🌧️ আজ বৃষ্টির সম্ভাবনা বেশি — কীটনাশক বা সার স্প্রে করবেন না।")
            advice.append("💧 সেচ দেওয়ার দরকার নেই, বৃষ্টির পানি যথেষ্ট।")
        elif rain_probability >= 40:
            advice.append("🌦️ বিকেলে বৃষ্টি হতে পারে — সকালে মাঠের কাজ সেরে নিন।")
        elif rain_probability < 20:
            advice.append("☀️ আজ বৃষ্টির সম্ভাবনা কম — প্রয়োজনে সেচ দিন।")

        # তাপমাত্রা সংক্রান্ত পরামর্শ
        if temperature >= 38:
            advice.append("🌡️ তাপমাত্রা অনেক বেশি — ফসলে বিকালে সেচ দিন, দুপুরে কাজ এড়িয়ে চলুন।")
        elif temperature >= 35:
            advice.append("🌡️ গরম বেশি — সকাল বা বিকালে মাঠের কাজ করুন।")
        elif temperature <= 15:
            advice.append("❄️ তাপমাত্রা কম — শীতকালীন ফসলের জন্য ভালো, গরম ফসল রক্ষা করুন।")

        # আর্দ্রতা সংক্রান্ত পরামর্শ
        if humidity >= 85:
            advice.append("💦 আর্দ্রতা অনেক বেশি — ছত্রাক রোগের ঝুঁকি আছে, ফসল পর্যবেক্ষণ করুন।")
        elif humidity <= 40:
            advice.append("🏜️ আর্দ্রতা কম — ফসলে নিয়মিত সেচ দিন।")

        # বায়ু বেগ সংক্রান্ত পরামর্শ
        if wind_speed >= 30:
            advice.append("💨 ঝড়ো বাতাস — লম্বা ফসল (যেমন ধান, ভুট্টা) ভেঙে পড়তে পারে, সতর্ক থাকুন।")
        elif wind_speed >= 20:
            advice.append("💨 বাতাস বেশি — স্প্রে করার জন্য অনুকূল নয়।")

        # UV সংক্রান্ত পরামর্শ
        if uv_index >= 8:
            advice.append("☀️ UV সূচক অনেক বেশি — কৃষকরা টুপি ও সানস্ক্রিন ব্যবহার করুন।")

        # বৃষ্টিপাত সংক্রান্ত পরামর্শ
        if precipitation >= 20:
            advice.append("🌊 অতিরিক্ত বৃষ্টি হয়েছে — জলাবদ্ধতা এড়াতে নিষ্কাশনের ব্যবস্থা করুন।")

    else:  # English
        # Rain advice
        if rain_probability >= 70:
            advice.append("🌧️ High chance of rain today — avoid spraying pesticides or fertilizers.")
            advice.append("💧 No need to irrigate — rainfall will be sufficient.")
        elif rain_probability >= 40:
            advice.append("🌦️ Possible rain in the afternoon — complete field work in the morning.")
        elif rain_probability < 20:
            advice.append("☀️ Low rain chance today — irrigate if needed.")

        # Temperature advice
        if temperature >= 38:
            advice.append("🌡️ Very high temperature — irrigate in the evening, avoid midday fieldwork.")
        elif temperature >= 35:
            advice.append("🌡️ Hot weather — work in fields during morning or evening hours.")
        elif temperature <= 15:
            advice.append("❄️ Low temperature — good for winter crops, protect warm-season crops.")

        # Humidity advice
        if humidity >= 85:
            advice.append("💦 Very high humidity — risk of fungal diseases, monitor crops closely.")
        elif humidity <= 40:
            advice.append("🏜️ Low humidity — irrigate crops regularly.")

        # Wind advice
        if wind_speed >= 30:
            advice.append("💨 Strong winds — tall crops (rice, maize) may lodge, stay alert.")
        elif wind_speed >= 20:
            advice.append("💨 Windy conditions — not suitable for spraying operations.")

        # UV advice
        if uv_index >= 8:
            advice.append("☀️ Very high UV index — farmers should wear hats and use sunscreen.")

        # Precipitation advice
        if precipitation >= 20:
            advice.append("🌊 Heavy rainfall — ensure proper drainage to avoid waterlogging.")

    # যদি কোনো পরামর্শ না থাকে
    if not advice:
        if language == "bn":
            advice.append("✅ আবহাওয়া স্বাভাবিক — নিয়মিত কৃষি কার্যক্রম চালিয়ে যেতে পারেন।")
        else:
            advice.append("✅ Weather is normal — you can continue regular farming activities.")

    return advice


def _error_weather_response(district: str, language: str) -> dict:
    """Error response তৈরি করে।"""
    error_msg = (
        "আবহাওয়া তথ্য পাওয়া যাচ্ছে না। পরে আবার চেষ্টা করুন।"
        if language == "bn"
        else "Weather data unavailable. Please try again later."
    )
    return {
        "district": district,
        "temperature": 0,
        "temp_max": 0,
        "temp_min": 0,
        "humidity": 0,
        "precipitation": 0,
        "rain_probability": 0,
        "wind_speed": 0,
        "uv_index": 0,
        "condition": "অজানা" if language == "bn" else "Unknown",
        "forecast_rain_3day": [],
        "farming_advice": [error_msg],
        "error": error_msg,
    }


def get_all_districts() -> list[dict]:
    """সমস্ত জেলার নাম ও তথ্য রিটার্ন করে (Frontend dropdown এর জন্য)।"""
    return [
        {"bn": bn_name, "en": info["en"]}
        for bn_name, info in BANGLADESH_DISTRICTS.items()
    ]