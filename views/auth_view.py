import streamlit as st
from utils import db, style


def render():
    st.markdown(f"""
    <div class="hero">
      <div class="logo">{style.icon('gem')}</div>
      <h1>Mumbai Tourist Guide</h1>
      <p>{style.icon('train-subway')} Western Line &nbsp; {style.icon('train')} Central Line &nbsp; {style.icon('city')} Navi Mumbai</p>
    </div>""", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.6, 1])
    with mid:
        tab_login, tab_reg = st.tabs(["Login", "New user? Register"])
        with tab_login:
            with st.form("login_form"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("Login", width="stretch"):
                    user = db.login(u, p)
                    if user:
                        st.session_state.user = user
                        st.session_state.nav = "Home"
                        st.rerun()
                    else:
                        st.error("Wrong username or password.")
            st.caption("Admin demo login: admin / admin123 (change with the ADMIN_PASSWORD environment variable before first run).")
        with tab_reg:
            with st.form("reg_form"):
                fn = st.text_input("Full name")
                em = st.text_input("Email")
                ru = st.text_input("Choose a username")
                rp = st.text_input("Choose a password (6+ characters)", type="password")
                if st.form_submit_button("Create account", width="stretch"):
                    ok, msg = db.register(ru, fn, em, rp)
                    (st.success if ok else st.error)(msg)
    style.footer()
