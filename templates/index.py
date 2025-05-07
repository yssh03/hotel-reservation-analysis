import streamlit as st
import requests

st.set_page_config(
    page_title="Hotel Reservation Failure Analysis",
    layout="wide"
)

st.header("Hotel Reservation Failure Analysis")
type_of_meal_plan_mapped_value = {'Meal Plan 1': 0, 'Meal Plan 2':
                                  1, 'Meal Plan 3': 2, 'Not Selected': 3}
room_type_reserved_mapped_value = {'Room Type 1': 0, 'Room Type 2': 1, 'Room Type 3':
                                   2, 'Room Type 4': 3, 'Room Type 5': 4, 'Room Type 6': 5, 'Room Type 7': 6}
market_segment_type_mapped_value = {'Aviation': 0, 'Complementary':
                                    1, 'Corporate': 2, 'Offline': 3, 'Online': 4}
arrival_month_mapped_value = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

col1, col2 = st.columns(2)

with col1:
    lead_time = st.number_input(label="Advanced Booking Days", min_value=0)
    market_segment_type = st.selectbox(label="Market Segment Type", options=(
        "Aviation", "Complementary",  "Corporate", "Offline", "Online"))
    arrival_month = st.selectbox(
        label="Arrival Month", options=list(arrival_month_mapped_value.keys()))
    no_of_weekend_nights = st.number_input(
        label="No of Weekend Nights", min_value=0)
    room_type_reserved = st.selectbox(label="Select Room Type Reserved", options=(
        "Room Type 1", "Room Type 2", "Room Type 3", "Room Type 4", "Room Type 5", "Room Type 6", "Room Type 7"))
with col2:
    no_of_special_requests = st.number_input(
        label="No of Special Request", min_value=0)
    avg_price_per_room = st.number_input(
        label="Average Price Per Room", min_value=0)
    arrival_date = st.selectbox(
        label="Arrival Date", options=range(1, 32))
    no_of_week_nights = st.number_input(
        label="No of Weekday Nights", min_value=0)
    type_of_meal_plan = st.selectbox(label="Select Meal Plan", options=(
        "Meal Plan 1", "Meal Plan 2", "No Meal Plan"))


col4, col5, col6 = st.columns(3)
with col5:
    clicked = st.button("Predict", type="primary", use_container_width=True)

    if clicked:
        data = {
            "lead_time": lead_time,
            "market_segment_type": market_segment_type_mapped_value[market_segment_type],
            "arrival_month": arrival_month_mapped_value[arrival_month],
            "arrival_date": arrival_date,
            "no_of_special_requests": no_of_special_requests,
            "no_of_week_nights": no_of_week_nights,
            "no_of_weekend_nights": no_of_weekend_nights,
            "type_of_meal_plan": type_of_meal_plan_mapped_value[type_of_meal_plan],
            "room_type_reserved": room_type_reserved_mapped_value[room_type_reserved],
            "avg_price_per_room": avg_price_per_room
        }
        print(data)
        response = requests.post(
            "http://127.0.0.1:5001/predict", json=data)
        st.write(f"##### {response.json()["prediction"]}")
