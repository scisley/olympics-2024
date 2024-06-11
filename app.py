import streamlit as st
import random
from components.country_data import get_country_data
from components.country_ai import create_country_ai, gen_image
import base64
from io import BytesIO
from PIL import Image

if "country_summary" not in st.session_state:
    st.session_state["country_summary"] = None

@st.cache_data
def get_all_country_data():
    return get_country_data()

countries = get_country_data()

@st.cache_data
def get_data(size):
    if size == 'Huuuge':
        return [country for country in countries if country["total"] >= 600]
    elif size == 'Mid Market':
        return [country for country in countries if 75 <= country["total"] <= 600]
    else:
        return [country for country in countries if country["total"] < 75]

st.title('2024 Olympic Country Chooser Tool, Thing, App, wait, wait - A.I.')

col1, col2 = st.columns([0.7, 0.3])
with col1:
    if picked_country := st.selectbox('Pick a Country', [None] + countries, format_func=lambda x: x['country'] if x else None):
        if (st.session_state.get("country") != picked_country):
            st.session_state["country_summary"] = None
        st.session_state["country"] = picked_country

col1, col2 = st.columns([0.7, 0.3])
with col1:
    size = st.selectbox('Country Size', ['Huuuge', 'Mid Market', 'Everyone loves an underdog'], label_visibility='collapsed')

countries = get_data(size)
with col2:
    if pick := st.button("I'm feeling lucky!"):
        country = random.choice(countries)
        st.session_state["country"] = country
        st.session_state["country_summary"] = None

st.write(f"There are {len(countries)} countries in this category")

chain = create_country_ai()

if country := st.session_state.get("country"):
    st.header(f"{country['country']}!")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""<img src="https://flagcdn.com/256x192/{country['iso'].lower()}.png" width="256" height="192">""", 
            unsafe_allow_html=True
        )
    with col2:
        st.subheader(f"🥇 Gold: {country['gold']}")
        st.subheader(f"🥈 Silver: {country['silver']}")
        st.subheader(f"🥉 Bronze: {country['bronze']}")
        #st.write(country)
    
    country_summary = st.session_state["country_summary"]
    if country_summary:
        st.write(country_summary)
    else:
        print('Creating country summary')
        stream = chain.stream({"country_name": country["country"]})
        country_summary = st.write_stream(stream)
        st.session_state["country_summary"] = country_summary

    if show_image := st.button("Generate Image!") and country_summary:
        print('Generated image!')
        img = gen_image(country_summary)
        image_data = base64.b64decode(img.b64_json)
        image = Image.open(BytesIO(image_data))
        st.image(image, caption='Image!', use_column_width=True)
