import streamlit as st
import threading
import time
import Full_Project

st.set_page_config(
    page_title="🏭Industrial Conveyor Vision Sorter",
    layout="wide"
)

st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}

.main-title {
    font-size: 40px;
    font-weight: 700;
    color: #111827;
}

.sub-title {
    font-size: 18px;
    color: #6b7280;
}

.metric-card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 6px 16px rgba(0,0,0,0.08);
    text-align: center;
}

.metric-title {
    font-size: 16px;
    color: #6b7280;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 42px;
    font-weight: bold;
    color: #111827;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("⚙ Conveyor Control")
start_btn = st.sidebar.button("▶ Start Simulation")
st.sidebar.markdown("---")
st.sidebar.write("📊 Dashboard")
st.sidebar.write("📈 Performance")
st.sidebar.write("📄 Reports")

if "running" not in st.session_state:
    st.session_state.running = False

if start_btn and not st.session_state.running:
    st.session_state.running = True
    threading.Thread(
        target=Full_Project.run_simulation,
        args=(60,),
        daemon=True
    ).start()

st.markdown('<div class="main-title">🏭 Industrial Conveyor Vision Sorter</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-Time Performance Dashboard</div>', unsafe_allow_html=True)

st.write("")
st.write("")

col1, col2, col3, col4 = st.columns(4)

total_box = col1.empty()
red_box = col2.empty()
blue_box = col3.empty()
missed_box = col4.empty()

while True:
    stats = Full_Project.get_stats()

    total_box.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📦 Total Objects</div>
        <div class="metric-value">{stats["Total Objects"]}</div>
    </div>
    """, unsafe_allow_html=True)

    red_box.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🔴 Red Sorted</div>
        <div class="metric-value">{stats["Red Sorted"]}</div>
    </div>
    """, unsafe_allow_html=True)

    blue_box.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🔵 Blue Sorted</div>
        <div class="metric-value">{stats["Blue Sorted"]}</div>
    </div>
    """, unsafe_allow_html=True)

    missed_box.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">⚠ Missed Sorts</div>
        <div class="metric-value">{stats["Missed Sorts"]}</div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(1)