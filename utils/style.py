import streamlit as st

CSS = """
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');

:root{ --gold:#FFD700; --gold2:#FFB300; --silver:#d9d9e3; --ink:#000; --panel:#0b0b10; --line:#2a2a33;
       --amazon: "Amazon Ember", "Ember", Arial, "Helvetica Neue", Helvetica, sans-serif; }

/* Amazon Ember is proprietary: drop licensed .woff2 files in assets/fonts and uncomment @font-face in README to use it.
   Otherwise Arial is used, which is the same fallback amazon.in uses. */
html, body, .stApp, p, li, label, input, textarea, button, select, a, td, th, h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"], [data-testid="stSidebar"] div { font-family: var(--amazon) !important; }

.stApp { background:#000; color:#f2f2f2; }

/* ---------- glitter: two twinkling star layers ---------- */
.stApp::before, .stApp::after { content:""; position:fixed; inset:0; pointer-events:none; z-index:0; }
.stApp::before {
  background-image:
    radial-gradient(1.6px 1.6px at 20px 30px,#fff,transparent),
    radial-gradient(1px 1px at 90px 140px,#FFD700,transparent),
    radial-gradient(1.6px 1.6px at 160px 70px,#fff,transparent),
    radial-gradient(1px 1px at 230px 190px,#cfcfdc,transparent),
    radial-gradient(2px 2px at 310px 110px,#ffe9a8,transparent),
    radial-gradient(1px 1px at 60px 210px,#fff,transparent);
  background-size:340px 240px; animation:twinkle 3.2s ease-in-out infinite alternate; }
.stApp::after {
  background-image:
    radial-gradient(1.4px 1.4px at 50px 80px,#FFD700,transparent),
    radial-gradient(1px 1px at 130px 20px,#fff,transparent),
    radial-gradient(1.8px 1.8px at 210px 150px,#ffffff,transparent),
    radial-gradient(1px 1px at 290px 60px,#FFB300,transparent),
    radial-gradient(1.2px 1.2px at 100px 190px,#cfcfdc,transparent);
  background-size:410px 280px; background-position:70px 40px; animation:twinkle 4.6s ease-in-out 1.4s infinite alternate-reverse; }
@keyframes twinkle { from{opacity:.15} to{opacity:1} }
@media (prefers-reduced-motion: reduce){ .stApp::before,.stApp::after{animation:none; opacity:.6} }

[data-testid="stAppViewContainer"] > .main, [data-testid="stHeader"], [data-testid="stSidebar"], .block-container { position:relative; z-index:1; }
[data-testid="stHeader"]{ background:transparent; }
.block-container { padding-top:2rem; max-width:1200px; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] { background:linear-gradient(180deg,#050507,#0d0d14); border-right:1px solid var(--line); }

/* ---------- headings ---------- */
h1,h2,h3 { background:linear-gradient(90deg,#fff 0%,var(--gold) 45%,var(--gold2) 100%); -webkit-background-clip:text; background-clip:text;
           -webkit-text-fill-color:transparent; letter-spacing:.2px; }
h1 i,h2 i,h3 i { -webkit-text-fill-color:var(--gold); color:var(--gold); margin-right:.45rem; }

/* ---------- buttons / inputs ---------- */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
  background:linear-gradient(135deg,#1a1a22,#0a0a0f); color:var(--gold); border:1px solid var(--gold); border-radius:10px; font-weight:700;
  transition:box-shadow .2s, transform .2s; }
.stButton > button:hover, .stFormSubmitButton > button:hover { box-shadow:0 0 14px rgba(255,215,0,.55); color:#000; background:linear-gradient(135deg,#FFD700,#FFB300); border-color:#FFD700; }
.stTextInput input, .stTextArea textarea, .stNumberInput input, [data-baseweb="select"] > div { background:#0b0b10 !important; color:#fff !important; border:1px solid var(--line) !important; border-radius:8px !important; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color:var(--gold) !important; box-shadow:0 0 0 1px var(--gold) !important; }
.stTabs [data-baseweb="tab"] { color:var(--silver); }
.stTabs [aria-selected="true"] { color:var(--gold) !important; }
.stTabs [data-baseweb="tab-highlight"] { background:var(--gold); }

/* ---------- custom components ---------- */
.hero { text-align:center; padding:2.2rem 1rem 1.2rem; }
.hero .logo { font-size:3rem; color:var(--gold); filter:drop-shadow(0 0 12px rgba(255,215,0,.6)); }
.hero h1 { font-size:2.8rem; margin:.2rem 0; }
.hero p { color:var(--silver); font-size:1.05rem; }
.card { background:linear-gradient(160deg,#101018,#07070b); border:1px solid var(--line); border-radius:14px; padding:14px 16px; margin-bottom:12px; }
.card:hover { border-color:rgba(255,215,0,.55); box-shadow:0 0 18px rgba(255,215,0,.12); }
.card h4 { margin:.1rem 0 .3rem; color:#fff; -webkit-text-fill-color:#fff; font-size:1.05rem; }
.card .meta { color:var(--silver); font-size:.88rem; }
.card i { color:var(--gold); margin-right:6px; }
.tag { display:inline-block; border:1px solid var(--gold); color:var(--gold); border-radius:999px; padding:1px 10px; font-size:.75rem; margin:2px 4px 2px 0; }
.stat { text-align:center; padding:14px; border:1px solid var(--line); border-radius:14px; background:#08080c; }
.stat .n { font-size:2rem; font-weight:800; color:var(--gold); }
.stat .l { color:var(--silver); font-size:.9rem; }
.dos li::marker { color:#4ade80; } .donts li::marker { color:#f87171; }
.dos h4 i { color:#4ade80 !important; } .donts h4 i { color:#f87171 !important; }
.ph { height:190px; border-radius:12px; display:flex; align-items:center; justify-content:center; flex-direction:column;
      background:radial-gradient(circle at 30% 20%,#2a2410,#0a0a0e); border:1px dashed #5b4b12; color:#8a7420; font-size:.85rem; margin-bottom:8px; }
.ph i { font-size:2.2rem; color:var(--gold); margin-bottom:6px; }
.footer { text-align:center; color:#7c7c8a; font-size:.78rem; margin-top:2.5rem; padding-bottom:1rem; }
[data-testid="stImage"] img { border-radius:12px; object-fit:cover; }
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)


def icon(name, extra=""):
    return f'<i class="fa-solid fa-{name} {extra}"></i>'


def title(text, ic, level=2):
    st.markdown(f"<h{level}>{icon(ic)}{text}</h{level}>", unsafe_allow_html=True)


def footer():
    st.markdown('<div class="footer">Photos &amp; summaries via Wikipedia / Wikimedia Commons (CC BY-SA and other free licences). '
                'Hotel &amp; cafe prices are indicative - verify before booking.</div>', unsafe_allow_html=True)
