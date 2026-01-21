import streamlit as st
import random
import time
import pandas as pd
from collections import deque
from datetime import datetime
import requests

DELAY = 1.0
ITERATIONS = 200

if "queue" not in st.session_state:
    st.session_state.queue = deque()

if "stats" not in st.session_state:
    st.session_state.stats = {"total": 0, "red": 0, "blue": 0, "missed": 0}

if "data" not in st.session_state:
    st.session_state.data = []

if "running" not in st.session_state:
    st.session_state.running = False

def get_camera_frame():
    return random.choice(["RED", "BLUE", "EMPTY"])

def schedule_object(color):
    st.session_state.queue.append((color, time.time() + DELAY))

def sorter():
    if st.session_state.queue and time.time() >= st.session_state.queue[0][1]:
        color, _ = st.session_state.queue.popleft()
        if color == "RED":
            st.session_state.stats["red"] += 1
        elif color == "BLUE":
            st.session_state.stats["blue"] += 1
def send_to_google_sheets():
    url = "https://script.google.com/macros/s/AKfycbykfGV0UL4jaDTk6INqwa7f7DxDMIwA0bJMclfCU2DKGaNn_dpu5_tM8rtgvo4lIk5svQ/exec"

    response = requests.post(
        url,
        json=st.session_state.stats,
        timeout=10
    )

    st.write("Google Sheets response:", response.text)


st.set_page_config(layout="wide")
st.title("Conveyor Vision Sorter – Live Dashboard")

start = st.button("Start Simulation")


c1, c2, c3, c4 = st.columns(4)
total_ph = c1.empty()
red_ph = c2.empty()
blue_ph = c3.empty()
missed_ph = c4.empty()

chart_ph = st.empty()

if start and not st.session_state.running:
    st.session_state.running = True

    for _ in range(ITERATIONS):
        detected = get_camera_frame()

        if detected in ["RED", "BLUE"]:
            st.session_state.stats["total"] += 1
            schedule_object(detected)

        sorter()

        
        total_ph.metric("Total Objects", st.session_state.stats["total"])
        red_ph.metric("Red Sorted", st.session_state.stats["red"])
        blue_ph.metric("Blue Sorted", st.session_state.stats["blue"])
        missed_ph.metric("Missed Sorts", st.session_state.stats["missed"])

        st.session_state.data.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Red": st.session_state.stats["red"],
            "Blue": st.session_state.stats["blue"]
        })

        df = pd.DataFrame(st.session_state.data).set_index("Time")
        chart_ph.line_chart(df)

        time.sleep(1)

    send_to_google_sheets()
    st.success("Simulation completed & data sent to Google Sheets ")
    st.session_state.running = False
