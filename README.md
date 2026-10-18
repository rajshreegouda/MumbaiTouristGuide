# Mumbai Tourist Guide (Streamlit + ML)

Glitter-black tourist guide for Mumbai's **Western Line, Central Line and Navi Mumbai**.

## Features
- Login / Register (PBKDF2-hashed passwords, SQLite)
- Home -> choose a route -> Explore places with real photos (Wikipedia/Wikimedia), info, Do's & Don'ts, map, YouTube vlogs
- Near Me: hotels, cafes and places within a radius (haversine distance + map + Google Maps directions)
- AI assistant: TF-IDF retrieval (scikit-learn) over the database; optional Claude answers (RAG) if `ANTHROPIC_API_KEY` is set
- ML search + "You may also like" content-based recommender (cosine similarity)
- Admin: dashboard, add / edit / delete Places, Hotels, Cafes, Users; chatbot question log
- Font Awesome 6 icons, Amazon-style font stack (Arial fallback, see below)

## Run it only on the Z: drive
1. Install Python 3.10-3.12 (python.org). In the installer choose **Customize installation** and set the path to `Z:\Python312`; tick *Add to PATH*.
   (If Python is already on C:, that's fine - it's small. All packages go to Z:.)
2. Unzip this folder to `Z:\MumbaiTouristGuide`.
3. Double-click `setup_z.bat` (once). It creates `.venv`, pip cache and temp folders inside Z:\MumbaiTouristGuide and downloads photos.
4. Double-click `run.bat`. Browser opens at http://localhost:8501.

Login: **admin / admin123** (admin). Register any new tourist from the Register tab.

Manual commands (Command Prompt):
```
Z:
cd \MumbaiTouristGuide
set PIP_CACHE_DIR=Z:\MumbaiTouristGuide\.cache\pip
set TEMP=Z:\MumbaiTouristGuide\.cache\tmp
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python fetch_images.py
streamlit run app.py
```

## Photos
`fetch_images.py` downloads one photo per place from Wikipedia into `assets/images/`.
Any that fail can be uploaded in Admin > Manage Places > Add, or set a Wikipedia title for them.
Wikimedia photos need attribution (a footer is included).

## Amazon font
Amazon Ember is proprietary and not publicly downloadable, so the CSS uses `"Amazon Ember", Arial` - Arial is what amazon.in itself falls back to.
If you hold a licence, put `AmazonEmber_Rg.woff2` in `assets/fonts/` and add an `@font-face` rule in `utils/style.py`.

## Chatbot with Claude (optional)
Edit `run.bat`, remove `REM` from the `ANTHROPIC_API_KEY` line and paste your key. Without a key the offline ML chatbot runs.

## YouTube vlogs
Each place starts with a YouTube search link. In Admin > Edit, paste a real video URL (youtube.com/watch?v=...) and it plays inside the page.

## Resume bullets
- Built a multi-page Streamlit tourism platform with role-based auth (user/admin), SQLite CRUD and geospatial "near me" search.
- Implemented TF-IDF + cosine-similarity retrieval for semantic search, a content-based recommender and a RAG chatbot (optional Claude API) with an offline fallback.

## Structure
```
app.py  fetch_images.py  setup_z.bat  run.bat  requirements.txt
utils/ db.py seed.py ml.py chatbot.py images.py style.py
views/ auth_view.py tourist.py admin.py
assets/images/   data/tourist.db (auto-created)
```
Change the admin password before first run: `set ADMIN_PASSWORD=YourPass` .
