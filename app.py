import streamlit as st
st.set_page_config(page_title="Mumbai Tourist Guide", page_icon="💎", layout="wide")

from utils import db, style
from views import auth_view, tourist, admin

db.init_db()
style.inject()
st.session_state.setdefault("user", None)

if not st.session_state.user:
    auth_view.render()
    st.stop()

user = st.session_state.user
is_admin = user["role"] == "admin"
TOURIST_PAGES = ["Home", "Explore Places", "Near Me", "AI Assistant"]
ADMIN_PAGES = ["Dashboard", "Manage Places", "Manage Hotels", "Manage Cafes", "Manage Users"]
pages = TOURIST_PAGES + (ADMIN_PAGES if is_admin else [])
st.session_state.setdefault("nav", "Home")

with st.sidebar:
    st.markdown(f'<div class="hero" style="padding:.5rem 0"><div class="logo" style="font-size:2rem">{style.icon("gem")}</div>'
                f'<div style="font-weight:700">{user["full_name"] or user["username"]}</div>'
                f'<div class="tag">{user["role"].title()}</div></div>', unsafe_allow_html=True)
    if st.session_state.nav not in pages:
        st.session_state.nav = "Home"
    st.radio("Navigate", pages, key="nav")
    if st.button("Logout", width="stretch"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

page = st.session_state.nav
if page == "Home":
    tourist.home()
elif page == "Explore Places":
    tourist.explore()
elif page == "Near Me":
    tourist.nearby()
elif page == "AI Assistant":
    tourist.chat()
else:
    admin.render(page)
