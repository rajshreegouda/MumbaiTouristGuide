"""Tourist assistant.
 - Retrieval: TF-IDF search over the places / hotels / cafes tables (RAG context).
 - If ANTHROPIC_API_KEY is set, Claude writes the answer using only that context.
 - Otherwise a rule-based fallback builds the answer, so the demo works with no key."""
import os
from utils import ml

SYSTEM = ("You are a friendly Mumbai tour guide for visitors exploring the Western Line, Central Line and Navi Mumbai. "
          "Answer using the provided context. If the context lacks the answer, say so briefly and give general safe advice. "
          "Be concise, use short bullet points, and mention do's and don'ts when relevant. Never invent prices or timings.")


def _fmt(hit):
    r, k = hit["row"], hit["kind"]
    if k == "place":
        return (f"PLACE: {r['name']} ({r['region']}, {r['area']}; station: {r['station']}). {r['description']} "
                f"Best time: {r['best_time']}. Entry: {r['entry_fee']}. DOs: {r['dos'].replace(chr(10), '; ')}. "
                f"DON'Ts: {r['donts'].replace(chr(10), '; ')}")
    if k == "hotel":
        return f"HOTEL: {r['name']} ({r['region']}, {r['area']}), {r['stars']} star, {r['price_per_night']}. {r['description']}"
    return f"CAFE: {r['name']} ({r['region']}, {r['area']}), known for {r['speciality']}, about {r['price_for_two']} for two. {r['description']}"


def _rule_based(q, hits):
    ql = q.lower()
    if any(w in ql for w in ("hi", "hello", "hey")) and len(ql.split()) <= 3:
        return "Hello! Ask me about places to visit, hotels, cafes, do's and don'ts, or the best time to visit anywhere on the Western Line, Central Line or in Navi Mumbai."
    if not hits:
        return "I couldn't find that in my guide. Try asking about a place, hotel or cafe, e.g. *'Best beaches on the Western Line'* or *'Cafes near Powai'*."
    want = None
    if any(w in ql for w in ("hotel", "stay", "room", "accommodation")):
        want = "hotel"
    elif any(w in ql for w in ("cafe", "coffee", "food", "eat", "restaurant", "breakfast")):
        want = "cafe"
    if want:
        pool = [h for h in hits if h["kind"] == want] or hits
    else:  # no hotel/cafe intent -> prefer places, and prefer a place named in the question
        places = [h for h in hits if h["kind"] == "place"]
        named = [h for h in places if h["row"]["name"].split("(")[0].strip().lower() in ql]
        pool = (named + [h for h in places if h not in named]) or hits
    top = pool[0]
    lines = []
    if top["kind"] == "place":
        r = top["row"]
        lines.append(f"**{r['name']}** - {r['region']}, {r['area']}\n\n{r['description']}")
        if "don" in ql or "avoid" in ql or "dos" in ql or "do's" in ql or "tips" in ql or "rules" in ql:
            lines.append("**Do's**\n" + "\n".join("- " + x for x in r["dos"].split("\n")))
            lines.append("**Don'ts**\n" + "\n".join("- " + x for x in r["donts"].split("\n")))
        lines.append(f"**Best time:** {r['best_time']}  \n**Entry:** {r['entry_fee']}  \n**Nearest station:** {r['station']}")
    else:
        lines.append("Here are my top matches:")
        for h in [x for x in pool if x["kind"] == top["kind"]][:3]:
            r = h["row"]
            extra = f"{r.get('stars', '')}★ - {r['price_per_night']}" if h["kind"] == "hotel" else f"{r['speciality']} - ~{r['price_for_two']} for two"
            lines.append(f"- **{r['name']}** ({r['area']}) - {extra}")
    others = [h["row"]["name"] for h in pool[1:4] if h["kind"] == "place"] if top["kind"] == "place" else []
    if others:
        lines.append("You might also like: " + ", ".join(others) + ".")
    return "\n\n".join(lines)


def reply(question, history):
    hits = ml.search(question, k=6)
    key = os.getenv("ANTHROPIC_API_KEY")
    if key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=key)
            ctx = "\n".join(_fmt(h) for h in hits) or "(no matching records)"
            msgs = [m for m in history[-6:]]
            while msgs and msgs[0]["role"] != "user":
                msgs.pop(0)
            msgs.append({"role": "user", "content": f"Context from the guide database:\n{ctx}\n\nTourist question: {question}"})
            out = client.messages.create(model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6"),
                                         max_tokens=700, system=SYSTEM, messages=msgs)
            return out.content[0].text
        except Exception as e:  # network / key problem -> graceful fallback
            return _rule_based(question, hits) + f"\n\n_(AI model unavailable: {type(e).__name__}; used offline guide search.)_"
    return _rule_based(question, hits)
