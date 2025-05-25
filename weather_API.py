import streamlit as st
import requests
from datetime import datetime
from collections import defaultdict

# ✅ Page config FIRST
st.set_page_config(page_title="அடுத்த 5 நாளுக்கான வானிலை ", layout="centered")

# ✅ THEN styling and rest of UI
st.markdown("""
    <style>
        .main {
            background-color: #f0f4f8;
        }
        .weather-card {
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
            padding: 1.5em;
            margin-bottom: 1em;
        }
        .emoji {
            font-size: 2em;
            vertical-align: middle;
        }
    </style>
""", unsafe_allow_html=True)


API_KEY = "41e60832c39381685cf06ee0f1cc61f5"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

tamil_weather = {
    "clear sky": "நிறைய வானம்",
    "scattered clouds": "சில மேகங்கள்",
    "overcast clouds": "அடர்ந்த மேகங்கள்",
    "light rain": "இலேசான மழை",
    "few clouds": "சில மேகங்கள்",
    "moderate rain": "மிதமான மழை"
}

#st.set_page_config(page_title="5 நாள் வானிலை", layout="centered")
st.title("☁️ வானிலை முன்னறிவிப்பு")
st.markdown("🌇 **உங்கள் நகரத்தைத் தேர்ந்தெடுத்து அடுத்த 5 நாட்களுக்கான வானிலை தெரிந்துகொள்ளுங்கள்.**")

city = st.text_input("🏙️ நகரத்தின் பெயரை உள்ளிடவும்")

@st.cache_data(ttl=3600)
def fetch_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if st.button("🌤️ வானிலை பார்க்க"):
    with st.spinner("தகவல்களை பெறுகிறது..."):
        data = fetch_weather(city)
        if data:
            forecasts = data['list']
            daily_forecast = defaultdict(list)
            for entry in forecasts:
                dt_txt = entry['dt_txt']
                date_str = dt_txt.split()[0]
                time_str = dt_txt.split()[1]
                temp = entry['main']['temp']
                desc = entry['weather'][0]['description']
                daily_forecast[date_str].append((time_str, temp, desc))

            st.success(f"**{city}** நகரத்தின் அடுத்த 5 நாட்களுக்கான வானிலை:")
            for date, infos in list(daily_forecast.items())[:5]:
                readable_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
                with st.container():
                    st.markdown(f"<div class='weather-card'><b>📅 {readable_date}</b>", unsafe_allow_html=True)
                    cols = st.columns(len(infos))
                    for i, (time, temp, desc) in enumerate(infos):
                        desc_tamil = tamil_weather.get(desc, desc)
                        emoji = "☀️" if "clear" in desc else "🌧️" if "rain" in desc else "☁️"
                        with cols[i]:
                            st.markdown(
                                f"<span class='emoji'>{emoji}</span> <b>{time}</b><br>"
                                f"🌡️ <b>{temp}°C</b><br>"
                                f"☁️ {desc} → <i>{desc_tamil}</i>",
                                unsafe_allow_html=True
                            )
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ நகரம் கிடைக்கவில்லை. சரியாகத் Type செய்தீர்களா?")

