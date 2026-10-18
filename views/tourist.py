import random
import pandas as pd
import streamlit as st
from utils import db, images, ml, style, chatbot
from utils.seed import REGIONS

STATIONS = {  # reference points for "Near me"
    "Churchgate": (18.9322, 72.8264), "CSMT": (18.9402, 72.8353), "Dadar": (19.0186, 72.8426),
    "Bandra": (19.0544, 72.8402), "Andheri": (19.1197, 72.8464), "Borivali": (19.2307, 72.8567),
    "Powai": (19.1176, 72.9060), "Thane": (19.1860, 72.9755), "Vashi": (19.0771, 72.9986),
    "CBD Belapur": (19.0235, 73.0388), "Kharghar": (19.0473, 73.0699), "Panvel": (18.9894, 73.1175),
}
REGION_ICON = {"Western Line": "train-subway", "Central Line": "train", "Navi Mumbai": "city"}


def go(page, **state):
    st.session_state.nav = page
    st.session_state.update(state)


def _img(place, fetch=False, height=None):
    src = images.resolve(place, allow_fetch=fetch)
    if src:
        st.image(src, width="stretch")
    else:
        st.markdown(f'<div class="ph">{style.icon("image")}<span>Photo not downloaded yet<br>run fetch_images.py</span></div>',
                    unsafe_allow_html=True)


def place_card(p, key):
    with st.container():
        _img(p)
        st.markdown(f"""<div class="card"><h4>{p['name']}</h4>
            <div class="meta">{style.icon('location-dot')}{p['area']}</div>
            <div class="meta">{style.icon(REGION_ICON.get(p['region'], 'train'))}{p['region']} - {p['station']}</div>
            <span class="tag">{p['category']}</span><span class="tag">{p['entry_fee']}</span></div>""", unsafe_allow_html=True)
        st.button("View details", key=key, on_click=go, args=("Explore Places",), kwargs={"place_id": p["id"]}, width="stretch")


# ------------------------------------------------------------------ HOME
def home():
    u = st.session_state.user
    st.markdown(f"""<div class="hero"><div class="logo">{style.icon('gem')}</div>
        <h1>Welcome, {u['full_name'] or u['username']}</h1>
        <p>Pick a route and explore Mumbai like a local.</p></div>""", unsafe_allow_html=True)

    places, hotels, cafes = db.rows("places"), db.rows("hotels"), db.rows("cafes")
    c = st.columns(4)
    for col, (n, label, ic) in zip(c, [(len(places), "Places", "landmark"), (len(hotels), "Hotels", "hotel"),
                                       (len(cafes), "Cafes", "mug-hot"), (3, "Regions", "map-location-dot")]):
        col.markdown(f'<div class="stat"><div class="n">{style.icon(ic)} {n}</div><div class="l">{label}</div></div>', unsafe_allow_html=True)

    st.write("")
    style.title("Choose your route", "route")
    cols = st.columns(3)
    for col, r in zip(cols, REGIONS):
        with col:
            cnt = sum(1 for p in places if p["region"] == r)
            st.markdown(f'<div class="card"><h4>{style.icon(REGION_ICON[r])}{r}</h4><div class="meta">{cnt} places to explore</div></div>', unsafe_allow_html=True)
            st.button(f"Explore {r}", key=f"reg_{r}", on_click=go, args=("Explore Places",), kwargs={"region_filter": r, "place_id": None}, width="stretch")

    st.write("")
    style.title("Today's picks", "star")
    picks = random.Random(pd.Timestamp.now().date().toordinal()).sample(places, min(3, len(places)))
    for col, p in zip(st.columns(3), picks):
        with col:
            place_card(p, f"pick_{p['id']}")
    style.footer()


# ------------------------------------------------------------------ EXPLORE
def explore():
    if st.session_state.get("place_id"):
        return place_detail()
    style.title("Explore places", "compass")
    places = db.rows("places")
    f1, f2, f3 = st.columns([1.2, 1, 1.6])
    region = f1.selectbox("Line / Region", ["All"] + REGIONS,
                          index=(["All"] + REGIONS).index(st.session_state.get("region_filter", "All")))
    cats = sorted({p["category"] for p in places})
    cat = f2.selectbox("Category", ["All"] + cats)
    q = f3.text_input("Search places (AI-powered)", placeholder="e.g. sunset views, caves, waterfalls")
    st.session_state.region_filter = region

    shown = [p for p in places if (region == "All" or p["region"] == region) and (cat == "All" or p["category"] == cat)]
    if q.strip():
        ids = [h["row"]["id"] for h in ml.search(q, k=10, kinds=["place"])]
        shown = [p for p in shown if p["id"] in ids]
        shown.sort(key=lambda p: ids.index(p["id"]))
    if not shown:
        st.info("No places match. Clear a filter or try different words.")
    for i in range(0, len(shown), 3):
        for col, p in zip(st.columns(3), shown[i:i + 3]):
            with col:
                place_card(p, f"pl_{p['id']}")
    style.footer()


def place_detail():
    p = next((x for x in db.rows("places", "WHERE id=?", (st.session_state.place_id,))), None)
    if not p:
        st.session_state.place_id = None
        return st.rerun()
    st.button("Back to places", on_click=lambda: st.session_state.update(place_id=None))
    style.title(p["name"], "landmark", 1)
    st.markdown(f'<span class="tag">{p["region"]}</span><span class="tag">{p["category"]}</span><span class="tag">{p["entry_fee"]}</span>', unsafe_allow_html=True)
    left, right = st.columns([1.4, 1])
    with left:
        with st.spinner("Loading photo..."):
            _img(p, fetch=True)
        st.write(p["description"])
    with right:
        st.markdown(f"""<div class="card">
            <div class="meta">{style.icon('location-dot')}<b>Area:</b> {p['area']}</div><br>
            <div class="meta">{style.icon('train-subway')}<b>Nearest station:</b> {p['station']}</div><br>
            <div class="meta">{style.icon('calendar-days')}<b>Best time:</b> {p['best_time']}</div><br>
            <div class="meta">{style.icon('ticket')}<b>Entry:</b> {p['entry_fee']}</div></div>""", unsafe_allow_html=True)
        st.map(pd.DataFrame({"lat": [p["lat"]], "lon": [p["lon"]]}), zoom=12, height=220)

    d1, d2 = st.columns(2)
    d1.markdown(f'<div class="card dos"><h4>{style.icon("circle-check")}Do\'s</h4><ul>' +
                "".join(f"<li>{x}</li>" for x in (p["dos"] or "").split("\n") if x) + "</ul></div>", unsafe_allow_html=True)
    d2.markdown(f'<div class="card donts"><h4>{style.icon("circle-xmark")}Don\'ts</h4><ul>' +
                "".join(f"<li>{x}</li>" for x in (p["donts"] or "").split("\n") if x) + "</ul></div>", unsafe_allow_html=True)

    style.title("Vlogs & videos", "youtube", 3)
    yt = (p["youtube"] or "").strip()
    if "watch?v=" in yt or "youtu.be/" in yt:
        st.video(yt)
    elif yt:
        st.link_button("Watch vlogs on YouTube", yt)
    st.link_button("More travel vlogs", "https://www.youtube.com/results?search_query=" + p["name"].replace(" ", "+") + "+Mumbai+travel+vlog")

    style.title("You may also like", "wand-magic-sparkles", 3)
    sims = ml.similar_places(p["id"], 3)
    for col, s in zip(st.columns(3), sims):
        with col:
            place_card(s, f"sim_{s['id']}")
    style.footer()


# ------------------------------------------------------------------ NEAR ME
def nearby():
    style.title("Hotels, cafes & places near me", "location-crosshairs")
    c1, c2 = st.columns([1.3, 1])
    mode = c1.radio("Where are you?", ["Pick a station / area", "Enter coordinates"], horizontal=True)
    if mode.startswith("Pick"):
        ref = c1.selectbox("Nearest station / area", list(STATIONS))
        lat, lon = STATIONS[ref]
    else:
        lat = c1.number_input("Latitude", value=19.0760, format="%.5f")
        lon = c1.number_input("Longitude", value=72.8777, format="%.5f")
        c1.caption("Tip: right-click your location on Google Maps to copy coordinates.")
    radius = c2.slider("Search radius (km)", 1, 30, 8)

    tabs = st.tabs(["Places", "Hotels", "Cafes"])
    spec = [("places", "landmark", lambda r: r["category"]),
            ("hotels", "hotel", lambda r: f"{r['stars']}★ - {r['price_per_night']}"),
            ("cafes", "mug-hot", lambda r: f"{r['speciality']} - ~{r['price_for_two']}")]
    for tab, (table, ic, sub) in zip(tabs, spec):
        with tab:
            data = db.rows(table)
            for r in data:
                r["km"] = round(ml.haversine(lat, lon, r["lat"], r["lon"]), 1)
            data = sorted([r for r in data if r["km"] <= radius], key=lambda r: r["km"])
            if not data:
                st.info(f"Nothing within {radius} km. Increase the radius.")
                continue
            st.map(pd.DataFrame(data)[["lat", "lon"]], height=260)
            for r in data:
                st.markdown(f"""<div class="card"><h4>{style.icon(ic)}{r['name']} <span class="tag">{r['km']} km</span></h4>
                    <div class="meta">{style.icon('location-dot')}{r['area']} - {r['region']}</div>
                    <div class="meta">{sub(r)}</div></div>""", unsafe_allow_html=True)
                st.link_button("Directions", f"https://www.google.com/maps/dir/?api=1&destination={r['lat']},{r['lon']}", key=f"dir_{table}_{r['id']}")
    style.footer()


# ------------------------------------------------------------------ CHATBOT
def chat():
    style.title("AI travel assistant", "robot")
    st.caption("Ask about places, hotels, cafes, do's and don'ts or the best time to visit. Powered by TF-IDF retrieval + optional Claude.")
    hist = st.session_state.setdefault("chat", [])
    if not hist:
        hist.append({"role": "assistant", "content": "Namaste! I'm your Mumbai guide. Try: *'Which places on the Western Line are good for sunset?'*"})
    for m in hist:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    q = st.chat_input("Ask a tourist question...")
    if q:
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ans = chatbot.reply(q, hist)
            st.markdown(ans)
        hist.extend([{"role": "user", "content": q}, {"role": "assistant", "content": ans}])
        db.log_chat(st.session_state.user["username"], q, ans)
    style.footer()
