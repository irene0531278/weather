import streamlit as st
import requests

# 페이지 기본 설정
st.set_page_config(
    page_title="실시간 날씨 기반 옷차림 추천기",
    page_icon="🌤️",
    layout="centered"
)

# OpenWeatherMap API 키 (본인의 API 키로 변경하세요)
API_KEY = "6d2313edccbbb5ac55d2171621e9824d"

def get_weather(city_name, api_key):
    """OpenWeatherMap API를 호출하여 날씨 정보를 가져오는 함수"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=kr"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json(), None
    elif response.status_code == 404:
        return None, "도시 이름을 찾을 수 없습니다. 영문 도시명을 정확히 입력해 주세요. (예: Seoul, Busan)"
    elif response.status_code == 401:
        return None, "API 키가 유효하지 않습니다. 키를 확인해 주세요."
    else:
        return None, "날씨 정보를 불러오는 중 오류가 발생했습니다."

def get_recommendation(temp, weather_main):
    """기온과 날씨 상태에 따른 옷차림 및 팁 추천 로직"""
    # 1. 기온별 옷차림 추천
    if temp >= 28:
        outfit = "민소매, 반바지, 반팔, 무슬림/린넨 원피스"
        temp_tip = "날씨가 매우 덥습니다. 얇고 통풍이 잘되는 옷을 입으세요."
    elif temp >= 23:
        outfit = "반팔, 얇은 셔츠, 반바지, 면바지"
        temp_tip = "가벼운 여름 옷차림이 활동하기 좋습니다."
    elif temp >= 20:
        outfit = "긴팔 티셔츠, 얇은 가디건, 면바지, 슬랙스"
        temp_tip = "선선한 바람이 불 수 있으니 가벼운 겉옷을 챙기세요."
    elif temp >= 17:
        outfit = "니트, 가디건, 후드티, 청바지"
        temp_tip = "일교차가 클 수 있으니 아침저녁 쌀쌀함에 대비하세요."
    elif temp >= 12:
        outfit = "자켓, 트렌치코트, 야상, 니트, 청바지"
        temp_tip = "쌀쌀한 날씨입니다. 외투를 꼭 챙기세요."
    elif temp >= 9:
        outfit = "코트, 가벼운 패딩, 히트텍, 목도리"
        temp_tip = "찬 바람이 불어 춥습니다. 따뜻하게 차려입으세요."
    else:
        outfit = "두꺼운 패딩, 목도리, 장갑, 기모 의류"
        temp_tip = "한파 대비! 방한 용품(모자, 장갑 등)까지 챙겨서 외출하세요."

    # 2. 날씨 상태별 추가 팁
    extra_tips = []
    weather_main_lower = weather_main.lower()
    
    if 'rain' in weather_main_lower or 'drizzle' in weather_main_lower:
        extra_tips.append("☔ 비가 오니 우산이나 우비를 꼭 챙기세요!")
    elif 'thunderstorm' in weather_main_lower:
        extra_tips.append("⛈️ 천둥번개가 침칩니다. 외출 시 안전에 유의하세요.")
    elif 'snow' in weather_main_lower:
        extra_tips.append("☃️ 눈이 내립니다. 미끄러지지 않도록 신발 선택에 주의하세요.")
    
    return outfit, temp_tip, extra_tips

# UI 구성
st.title("🌤️ 날씨 기반 옷차림 추천기")
st.write("원하는 도시의 영문 이름을 입력하면 현재 날씨와 알맞은 옷차림을 알려드립니다.")

# 도시 입력
city_input = st.text_input("도시 이름을 영문으로 입력하세요 (예: Seoul, Busan, Tokyo, London):", value="Seoul")

if st.button("날씨 및 옷차림 조회"):
    if not city_input.strip():
        st.warning("도시 이름을 입력해 주세요.")
    elif API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        st.error("API 키가 설정되지 않았습니다. 소스코드의 `API_KEY` 변수에 발급받은 키를 입력해 주세요.")
    else:
        with st.spinner("날씨 정보를 불러오는 중..."):
            weather_data, error_msg = get_weather(city_input.strip(), API_KEY)
            
            if error_msg:
                st.error(error_msg)
            else:
                # 데이터 추출
                city_name = weather_data['name']
                country = weather_data['sys']['country']
                temp = weather_data['main']['temp']
                feels_like = weather_data['main']['feels_like']
                humidity = weather_data['main']['humidity']
                weather_desc = weather_data['weather'][0]['description']
                weather_main = weather_data['weather'][0]['main']
                icon_code = weather_data['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

                # 결과 메인 카드
                st.markdown("---")
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(icon_url, width=100)
                with col2:
                    st.subheader(f"📍 {city_name}, {country}")
                    st.markdown(f"**현재 기온:** {temp:.1f}°C (체감 {feels_like:.1f}°C)")
                    st.markdown(f"**날씨 상태:** {weather_desc} / 습도 {humidity}%")

                # 옷차림 추천 결과
                outfit, temp_tip, extra_tips = get_recommendation(temp, weather_main)
                
                st.markdown("---")
                st.success(f"### 🧥 추천 옷차림\n{outfit}")
                st.info(f"💡 **기온 팁:** {temp_tip}")

                # 비/눈 등 특수 날씨 팁 출력
                for tip in extra_tips:
                    st.warning(tip)