import streamlit as st
import threading
import time
import Full_Project
import pandas as pd

st.set_page_config(layout="wide")

if "started" not in st.session_state:
    st.session_state.started = False

if "history" not in st.session_state:
    st.session_state.history = {
        "time": [],
        "total": [],
        "red": [],
        "blue": [],
        "missed": []
    }

st.sidebar.title("Control Panel")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Performance"]
)

start_btn = st.sidebar.button("Start Simulation")

if start_btn and not st.session_state.started:
    st.session_state.started = True
    threading.Thread(
        target=Full_Project.run_simulation,
        daemon=True
    ).start()

if page == "Dashboard":
    st.title("Conveyor Vision Sorter Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    stats = Full_Project.get_stats()

    col1.metric("Total Objects", stats["Total Objects"])
    col2.metric("Red Sorted", stats["Red Sorted"])
    col3.metric("Blue Sorted", stats["Blue Sorted"])
    col4.metric("Missed Sorts", stats["Missed Sorts"])


elif page == "Performance":
    st.title(" Live Performance Graphs")

    stats = Full_Project.get_stats()
    current_time = len(st.session_state.history["time"])

    st.session_state.history["time"].append(current_time)
    st.session_state.history["total"].append(stats["Total Objects"])
    st.session_state.history["red"].append(stats["Red Sorted"])
    st.session_state.history["blue"].append(stats["Blue Sorted"])
    st.session_state.history["missed"].append(stats["Missed Sorts"])

    df = pd.DataFrame({
        "Total Objects": st.session_state.history["total"],
        "Red Sorted": st.session_state.history["red"],
        "Blue Sorted": st.session_state.history["blue"],
        "Missed Sorts": st.session_state.history["missed"]
    })

    st.line_chart(df)

time.sleep(1)
st.rerun()