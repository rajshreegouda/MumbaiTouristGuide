"""Run once (needs internet):  python fetch_images.py
Downloads a real photo for every place in the database into assets/images/."""
from utils import db, images

db.init_db()
for p in db.rows("places"):
    path = images.resolve(p)
    if path:
        print("have   ", p["name"])
        continue
    fn = images.download_for(p["name"], p.get("wiki_title"))
    print("saved  " if fn else "MISSING", p["name"])
print("Done. Missing ones can be uploaded from Admin > Manage Places.")
