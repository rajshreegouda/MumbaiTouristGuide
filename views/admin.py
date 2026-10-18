import pandas as pd
import streamlit as st
from utils import db, images, ml, style
from utils.seed import REGIONS, CATEGORIES

PLACE_F = [("name", "Name", "text"), ("region", "Line / Region", REGIONS), ("area", "Area", "text"),
           ("station", "Nearest station", "text"), ("category", "Category", CATEGORIES),
           ("description", "Description", "area"), ("dos", "Do's (one per line)", "area"),
           ("donts", "Don'ts (one per line)", "area"), ("best_time", "Best time to visit", "text"),
           ("entry_fee", "Entry fee", "text"), ("lat", "Latitude", "float"), ("lon", "Longitude", "float"),
           ("wiki_title", "Wikipedia page title (used to fetch a real photo)", "text"),
           ("youtube", "YouTube video / search URL", "text")]
HOTEL_F = [("name", "Name", "text"), ("region", "Line / Region", REGIONS), ("area", "Area", "text"),
           ("stars", "Stars", "int"), ("price_per_night", "Price category", "text"), ("phone", "Phone", "text"),
           ("lat", "Latitude", "float"), ("lon", "Longitude", "float"), ("description", "Description", "area")]
CAFE_F = [("name", "Name", "text"), ("region", "Line / Region", REGIONS), ("area", "Area", "text"),
          ("speciality", "Speciality", "text"), ("price_for_two", "Price for two", "text"),
          ("lat", "Latitude", "float"), ("lon", "Longitude", "float"), ("description", "Description", "area")]


def _widget(spec, key, default=None):
    name, label, kind = spec
    k = f"{key}_{name}"
    if isinstance(kind, list):
        idx = kind.index(default) if default in kind else 0
        return st.selectbox(label, kind, index=idx, key=k)
    if kind == "area":
        return st.text_area(label, value=default or "", key=k)
    if kind == "float":
        return st.number_input(label, value=float(default or 19.0), format="%.5f", key=k)
    if kind == "int":
        return st.number_input(label, value=int(default or 4), min_value=1, max_value=7, step=1, key=k)
    return st.text_input(label, value=default or "", key=k)


def crud(table, fields, label, icon, with_image=False):
    style.title(f"Manage {label}", icon)
    data = db.rows(table)
    show = [f[0] for f in fields[:6]]
    if data:
        st.dataframe(pd.DataFrame(data)[["id"] + show], width="stretch", hide_index=True)
    else:
        st.info(f"No {label.lower()} yet. Use the Add tab.")
    t_add, t_edit, t_del = st.tabs(["Add", "Edit", "Delete"])

    with t_add:
        with st.form(f"add_{table}", clear_on_submit=True):
            vals = {f[0]: _widget(f, f"add_{table}") for f in fields}
            up = st.file_uploader("Photo (optional)", type=["jpg", "jpeg", "png"]) if with_image else None
            if st.form_submit_button(f"Add {label[:-1] if label.endswith('s') else label}", width="stretch"):
                if not vals["name"].strip():
                    st.error("Name is required.")
                else:
                    if up:
                        images.IMG_DIR.mkdir(parents=True, exist_ok=True)
                        fn = images.slug(vals["name"]) + ".jpg"
                        (images.IMG_DIR / fn).write_bytes(up.getvalue())
                        vals["image"] = fn
                    db.insert(table, vals)
                    ml.refresh()
                    st.success("Added.")
                    st.rerun()

    with t_edit:
        if data:
            sel = st.selectbox("Choose a record", data, format_func=lambda r: f"{r['id']} - {r['name']}", key=f"sel_edit_{table}")
            with st.form(f"edit_{table}_{sel['id']}"):
                vals = {f[0]: _widget(f, f"edit_{table}_{sel['id']}", sel.get(f[0])) for f in fields}
                if st.form_submit_button("Save changes", width="stretch"):
                    db.update(table, sel["id"], vals)
                    ml.refresh()
                    st.success("Saved.")
                    st.rerun()

    with t_del:
        if data:
            sel = st.selectbox("Choose a record to delete", data, format_func=lambda r: f"{r['id']} - {r['name']}", key=f"sel_del_{table}")
            confirm = st.checkbox("Yes, delete this permanently", key=f"conf_{table}")
            if st.button("Delete", key=f"del_{table}", disabled=not confirm):
                db.delete(table, sel["id"])
                ml.refresh()
                st.success(f"Deleted {sel['name']}.")
                st.rerun()


def users():
    style.title("Manage users", "users")
    data = db.rows("users")
    st.dataframe(pd.DataFrame(data)[["id", "username", "full_name", "email", "role", "created"]], width="stretch", hide_index=True)
    others = [u for u in data if u["role"] != "admin"]
    if others:
        sel = st.selectbox("Remove a tourist account", others, format_func=lambda u: u["username"])
        if st.checkbox("Confirm removal") and st.button("Delete user"):
            db.delete("users", sel["id"])
            st.success("User removed.")
            st.rerun()


def dashboard():
    style.title("Admin dashboard", "gauge-high")
    cols = st.columns(5)
    for col, (t, l, ic) in zip(cols, [("users", "Users", "users"), ("places", "Places", "landmark"), ("hotels", "Hotels", "hotel"),
                                      ("cafes", "Cafes", "mug-hot"), ("chat_log", "Chat queries", "comments")]):
        col.markdown(f'<div class="stat"><div class="n">{style.icon(ic)} {len(db.rows(t))}</div><div class="l">{l}</div></div>', unsafe_allow_html=True)
    st.write("")
    style.title("Places per region", "chart-column", 3)
    p = pd.DataFrame(db.rows("places"))
    if not p.empty:
        st.bar_chart(p.groupby("region").size(), color="#FFD700")
    style.title("Recent chatbot questions", "comments", 3)
    logs = db.rows("chat_log", "ORDER BY id DESC LIMIT 15")
    if logs:
        st.dataframe(pd.DataFrame(logs)[["ts", "username", "question"]], width="stretch", hide_index=True)
    else:
        st.caption("No questions yet.")


def render(page):
    if page == "Dashboard":
        dashboard()
    elif page == "Manage Places":
        crud("places", PLACE_F, "Places", "landmark", with_image=True)
    elif page == "Manage Hotels":
        crud("hotels", HOTEL_F, "Hotels", "hotel")
    elif page == "Manage Cafes":
        crud("cafes", CAFE_F, "Cafes", "mug-hot")
    elif page == "Manage Users":
        users()
    style.footer()
