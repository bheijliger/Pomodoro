import streamlit as st
import time

st.set_page_config(page_title="Pomodoro Timer", layout="centered")

st.title("🍅 Pomodoro Timer")

# --- Sidebar settings ---
st.sidebar.header("Settings")

work_time = st.sidebar.slider("Work duration (minutes)", 1, 60, 25)
short_break = st.sidebar.slider("Short break (minutes)", 1, 30, 5)
long_break = st.sidebar.slider("Long break (minutes)", 5, 60, 15)
cycles_before_long = st.sidebar.slider("Cycles before long break", 1, 10, 4)

# --- Session state ---
if "running" not in st.session_state:
    st.session_state.running = False
if "cycle" not in st.session_state:
    st.session_state.cycle = 1

# --- Timer display ---
timer_placeholder = st.empty()
status_placeholder = st.empty()

def countdown(minutes, label):
    total_seconds = minutes * 60
    while total_seconds > 0 and st.session_state.running:
        mins, secs = divmod(total_seconds, 60)
        timer_placeholder.markdown(f"## ⏱ {mins:02d}:{secs:02d}")
        status_placeholder.info(label)
        time.sleep(1)
        total_seconds -= 1

def run_pomodoro():
    while st.session_state.running:
        # Work session
        countdown(work_time, "Work Time 💻")

        if not st.session_state.running:
            break

        # Decide break type
        if st.session_state.cycle % cycles_before_long == 0:
            countdown(long_break, "Long Break ☕")
        else:
            countdown(short_break, "Short Break 🧃")

        st.session_state.cycle += 1

# --- Controls ---
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start"):
        st.session_state.running = True
        run_pomodoro()

with col2:
    if st.button("⏹ Stop"):
        st.session_state.running = False

# --- Info ---
st.write(f"Current cycle: {st.session_state.cycle}")