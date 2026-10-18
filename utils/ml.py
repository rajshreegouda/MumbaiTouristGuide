"""ML layer: TF-IDF retrieval (used by chatbot + search) and content-based 'similar places' recommender."""
import math
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import db


def haversine(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _doc_text(kind, r):
    if kind == "place":
        return f"{r['name']} {r['region']} {r['area']} {r['station']} {r['category']} {r['description']} {r['best_time']}"
    if kind == "hotel":
        return f"hotel stay {r['name']} {r['region']} {r['area']} {r['price_per_night']} {r['description']}"
    return f"cafe food eat coffee restaurant {r['name']} {r['region']} {r['area']} {r['speciality']} {r['description']}"


@st.cache_resource(show_spinner=False)
def _index(_version):
    docs = []
    for kind, table in (("place", "places"), ("hotel", "hotels"), ("cafe", "cafes")):
        for r in db.rows(table):
            docs.append({"kind": kind, "row": r, "text": _doc_text(kind, r)})
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    mat = vec.fit_transform([d["text"] for d in docs])
    return docs, vec, mat


_version = {"v": 0}


def refresh():
    """Call after the admin changes data so the model is rebuilt."""
    _version["v"] += 1


def search(query, k=5, kinds=None):
    docs, vec, mat = _index(_version["v"])
    sims = cosine_similarity(vec.transform([query]), mat).ravel()
    out = []
    for i in np.argsort(-sims):
        if sims[i] <= 0.02 or len(out) >= k:
            break
        if kinds and docs[i]["kind"] not in kinds:
            continue
        out.append({**docs[i], "score": float(sims[i])})
    return out


def similar_places(place_id, k=3):
    docs, vec, mat = _index(_version["v"])
    idx = [i for i, d in enumerate(docs) if d["kind"] == "place"]
    target = next((i for i in idx if docs[i]["row"]["id"] == place_id), None)
    if target is None:
        return []
    sims = cosine_similarity(mat[target], mat[idx]).ravel()
    order = np.argsort(-sims)
    return [docs[idx[j]]["row"] for j in order if docs[idx[j]]["row"]["id"] != place_id][:k]
