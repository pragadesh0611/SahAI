"""SahAI ledger parser: turns a transcribed Tamil/English sentence into a structured ledger entry.
In the full pipeline the text comes from Whisper (ASR); Llama 3.2 1B handles free-form phrasing,
and this rule-based layer validates every entry before it is written to SQLite."""
import re, sqlite3, json

UNITS = {"கிலோ": "kg", "kg": "kg", "லிட்டர்": "litre", "litre": "litre", "liter": "litre"}
SELL = ("விற்றேன்", "விற்பனை", "sold", "sell")
BUY = ("வாங்கினேன்", "வாங்கினோம்", "bought", "buy")

def parse(text: str):
    t = text.strip()
    action = "sale" if any(w in t for w in SELL) else "purchase" if any(w in t for w in BUY) else None
    unit_pat = "|".join(map(re.escape, UNITS))
    m = re.search(rf"(\d+(?:\.\d+)?)\s*({unit_pat})\s+(\S+)", t)
    p = re.search(r"(\d+(?:\.\d+)?)\s*(?:ரூபாய்|rupees|rs|₹)", t, re.I)
    if not (action and m and p):
        return {"ok": False, "reason": "needs confirmation", "text": t}
    return {"ok": True, "type": action, "qty": float(m.group(1)), "unit": UNITS[m.group(2)],
            "item": m.group(3), "amount_inr": float(p.group(1))}

def save(entry, db=":memory:"):
    con = sqlite3.connect(db)
    con.execute("create table if not exists ledger(type,item,qty,unit,amount_inr)")
    con.execute("insert into ledger values(?,?,?,?,?)",
                (entry["type"], entry["item"], entry["qty"], entry["unit"], entry["amount_inr"]))
    con.commit(); return con

if __name__ == "__main__":
    tests = ["இன்று 5 கிலோ அரிசி 300 ரூபாய்க்கு விற்றேன்",
             "இன்று 2 கிலோ சர்க்கரை 90 ரூபாய்க்கு வாங்கினேன்",
             "sold 3 kg sugar for 150 rupees",
             "இன்று வியாபாரம் நன்றாக இருந்தது"]
    for s in tests:
        print(s, "->", json.dumps(parse(s), ensure_ascii=False))
