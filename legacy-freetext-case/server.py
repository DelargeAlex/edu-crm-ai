import html
import json
import os
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, quote_plus, urlparse


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "legacy_ingest.sqlite3")
HOST = "0.0.0.0"
PORT = 8086
HADDOCK_PATH = os.path.join(BASE_DIR, "haddokk.png")


EXAMPLES = [
    {
        "company": "Kjells Konserverade Koi",
        "blob": "namn=Karin Koi | email=karin@lobbylagret.se | telefon=070-123 45 67 | produkt=Konserverad Koi Premium | antal=18 | stad=Borås | kanal=webb | kommentar=Vi vill ha något lugnt men ändå premium till hotellobbyn | profileUrl=https://api.dicebear.com/9.x/fun-emoji/svg?seed=KarinKoi",
    },
    {
        "company": "Kjells Konserverade Koi",
        "blob": "namn=Roger Räka | email=roger@presentpanik.se | telefon=073-998 00 11 | produkt=Återfuktad Räka XL | antal=42 | stad=Kalmar | kanal=kampanj | kommentar=Kan ni skicka offert idag och går det att paketera som företagsgåva? | profileUrl=https://api.dicebear.com/9.x/fun-emoji/svg?seed=RogerRaka",
    },
    {
        "company": "Kjells Konserverade Koi",
        "blob": "namn=Linda Lax | email=linda@retrokaj.se | telefon=076-444 33 22 | produkt=Abonnemang På Tyst Fisk | antal=3 | stad=Malmö | kanal=meta | kommentar=Vi fick dubbla leveranser och en av fiskarna ser överdrivet avslappnad ut | profileUrl=https://api.dicebear.com/9.x/fun-emoji/svg?seed=LindaLax",
    },
    {
        "company": "Kjells Konserverade Koi",
        "blob": "namn=Patrik Paradox | email=patrik@eventakuten.se | telefon=070-777 12 34 | produkt=Tidsresande Koi Demo Kit | antal=1 | stad=Uppsala | kanal=partner | kommentar=Vi vill göra ett PR-event men er koi verkar redan ha upplevt eventet i förväg | profileUrl=https://api.dicebear.com/9.x/fun-emoji/svg?seed=PatrikParadox",
    },
]


def normalize_legacy_text(value):
    replacements = {
        "Boras": "Borås",
        "Malmo": "Malmö",
        "nagot": "något",
        "anda": "ändå",
        "Aterfuktad Raka XL": "Återfuktad Räka XL",
        "Roger Raka": "Roger Räka",
        "Abonnemang Pa Tyst Fisk": "Abonnemang På Tyst Fisk",
        "overdrivet": "överdrivet",
        "gar det": "går det",
        "foretagsgava": "företagsgåva",
        "gora": "göra",
        "forvag": "förväg",
    }
    normalized = value
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    with db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS raw_submissions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              company TEXT NOT NULL,
              raw_blob TEXT NOT NULL,
              created_at TEXT NOT NULL
            )
            """
        )
        count = conn.execute("SELECT COUNT(*) AS c FROM raw_submissions").fetchone()["c"]
        if count == 0:
            for row in EXAMPLES:
                conn.execute(
                    "INSERT INTO raw_submissions (company, raw_blob, created_at) VALUES (?, ?, ?)",
                    (row["company"], row["blob"], datetime.now(timezone.utc).isoformat()),
                )
        rows = conn.execute("SELECT id, company, raw_blob FROM raw_submissions").fetchall()
        for row in rows:
            company = normalize_legacy_text(row["company"])
            raw_blob = normalize_legacy_text(row["raw_blob"])
            if company != row["company"] or raw_blob != row["raw_blob"]:
                conn.execute(
                    "UPDATE raw_submissions SET company = ?, raw_blob = ? WHERE id = ?",
                    (company, raw_blob, row["id"]),
                )
        conn.commit()


def latest_rows(limit=12):
    with db() as conn:
        rows = conn.execute(
            "SELECT id, company, raw_blob, created_at FROM raw_submissions ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def row_by_id(row_id):
    with db() as conn:
        row = conn.execute(
            "SELECT id, company, raw_blob, created_at FROM raw_submissions WHERE id = ?",
            (row_id,),
        ).fetchone()
    return dict(row) if row else None


def latest_row():
    with db() as conn:
        row = conn.execute(
            "SELECT id, company, raw_blob, created_at FROM raw_submissions ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return dict(row) if row else None


def insert_row(company, raw_blob):
    created_at = datetime.now(timezone.utc).isoformat()
    with db() as conn:
        cursor = conn.execute(
            "INSERT INTO raw_submissions (company, raw_blob, created_at) VALUES (?, ?, ?)",
            (company, raw_blob, created_at),
        )
        conn.commit()
        return cursor.lastrowid


def ugly_page(saved_id=None):
    rows = latest_rows()
    example_blob = EXAMPLES[0]["blob"]
    rows_html = "".join(
        f"""
        <tr>
          <td>{row['id']}</td>
          <td>{html.escape(row['company'])}</td>
          <td><code>{html.escape(row['raw_blob'])}</code></td>
          <td>{html.escape(row['created_at'])}</td>
        </tr>
        """
        for row in rows
    )
    saved_banner = (
        f"<div class='saved'>Nytt legacy-lead sparat! Rad-id: <strong>{saved_id}</strong>. Nu kan eleverna jaga den i SQLite och regex-parsa blobben i n8n.</div>"
        if saved_id
        else ""
    )
    return f"""<!doctype html>
<html lang="sv">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Kjells Konserverade Koi — Legacy Ingest 2004</title>
    <style>
      :root {{
        --bg: #25001d;
        --panel: #fff4b8;
        --ink: #3b0031;
        --pink: #ff4db8;
        --cyan: #45efff;
        --lime: #ccff33;
        --warn: #ff8a00;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: "Comic Sans MS", "Trebuchet MS", cursive;
        background:
          radial-gradient(circle at 12% 8%, rgba(255, 77, 184, 0.45), transparent 26%),
          radial-gradient(circle at 88% 14%, rgba(69, 239, 255, 0.35), transparent 24%),
          linear-gradient(135deg, #260021, #4b0039 60%, #21001f);
        color: #fff7fd;
      }}
      .wrap {{
        max-width: 1180px;
        margin: 0 auto;
        padding: 1.5rem 1rem 3rem;
      }}
      .haddock {{
        position: fixed;
        top: 50%;
        width: min(18vw, 230px);
        transform: translateY(-50%);
        pointer-events: none;
        z-index: 0;
        opacity: 0.95;
        filter: drop-shadow(0 16px 22px rgba(0, 0, 0, 0.45));
      }}
      .haddock-left {{
        left: 0.3rem;
      }}
      .haddock-right {{
        right: 0.3rem;
        transform: translateY(-50%) scaleX(-1);
      }}
      main.wrap {{
        position: relative;
        z-index: 1;
      }}
      .hero {{
        border: 5px double var(--lime);
        background:
          linear-gradient(90deg, rgba(255, 77, 184, 0.22), rgba(69, 239, 255, 0.12)),
          rgba(0, 0, 0, 0.22);
        border-radius: 24px;
        padding: 1.2rem 1.2rem 1.4rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
      }}
      h1 {{
        margin: 0;
        font-size: clamp(2rem, 4vw, 3.4rem);
        color: #fffbe8;
        text-shadow: 3px 3px 0 #ff00a6;
      }}
      .hero p {{
        max-width: 80ch;
        font-size: 1.05rem;
      }}
      .blink {{
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        background: var(--warn);
        color: #2b001b;
        font-weight: 900;
        animation: pop 0.9s infinite alternate;
      }}
      @keyframes pop {{
        from {{ transform: scale(1); }}
        to {{ transform: scale(1.06); }}
      }}
      .grid {{
        display: grid;
        grid-template-columns: 1.05fr 0.95fr;
        gap: 1rem;
        margin-top: 1rem;
      }}
      .card {{
        background: var(--panel);
        color: var(--ink);
        border: 4px solid var(--pink);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.28);
      }}
      h2 {{
        margin-top: 0;
        color: #65004f;
      }}
      label {{
        display: block;
        margin-bottom: 0.7rem;
        font-weight: 700;
      }}
      input,
      textarea {{
        width: 100%;
        padding: 0.7rem 0.8rem;
        border-radius: 12px;
        border: 3px solid #65004f;
        font: inherit;
        background: #fffdf4;
      }}
      textarea {{
        min-height: 210px;
        resize: vertical;
      }}
      button {{
        border: 0;
        border-radius: 16px;
        padding: 0.8rem 1rem;
        background: linear-gradient(180deg, var(--cyan), #00bcd9);
        color: #1b0023;
        font-size: 1rem;
        font-weight: 900;
        cursor: pointer;
      }}
      .saved {{
        margin-top: 1rem;
        padding: 0.8rem 1rem;
        border-radius: 16px;
        background: rgba(204, 255, 51, 0.18);
        border: 2px dashed var(--lime);
      }}
      .tiny {{
        margin-top: 0.6rem;
        font-size: 0.92rem;
      }}
      code {{
        font-family: ui-monospace, monospace;
        font-size: 0.92em;
      }}
      .ugly-list li {{
        margin: 0.45rem 0;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
      }}
      th, td {{
        border: 2px solid #8e0070;
        padding: 0.55rem;
        text-align: left;
        vertical-align: top;
      }}
      th {{
        background: #ffd5ef;
      }}
      .reward-link {{
        display: inline-block;
        margin-top: 0.7rem;
        color: #7d0057;
        font-weight: 800;
      }}
      @media (max-width: 920px) {{
        .grid {{ grid-template-columns: 1fr; }}
        .haddock {{
          width: min(28vw, 180px);
          opacity: 0.7;
        }}
      }}
    </style>
  </head>
  <body>
    <img class="haddock haddock-left" src="/haddokk.png" alt="" aria-hidden="true" />
    <img class="haddock haddock-right" src="/haddokk.png" alt="" aria-hidden="true" />
    <main class="wrap">
      <section class="hero">
        <div class="blink">LEGACY MYSQL-ISH CRM 2004</div>
        <h1>Kjells Konserverade Koi & Krisjour</h1>
        <p>
          Väldigt ful hemsida med väldigt dålig datamodell. Hela formuläret sparas i <strong>en enda sträng</strong>,
          men bakom kulisserna landar det i en <strong>SQLite-databas</strong> som simulerar en gammal, opålitlig
          "MySQL-liknande" legacy-integrationspunkt.
        </p>
        <p>
          Elevuppgift: läs blobben, regex-parsa ut riktiga fält i n8n, spara strukturerat till valfri källa
          och posta sedan resultatet till reward-webhooken för snygg preview.
        </p>
      </section>
      {saved_banner}
      <section class="grid">
        <article class="card">
          <h2>Skapa nytt katastrof-lead</h2>
          <form method="post" action="/submit">
            <label>
              Roligtnamn / företag
              <input name="company" value="Kjells Konserverade Koi" />
            </label>
            <label>
              Hela formularet i en blob
              <textarea name="blob">{html.escape(example_blob)}</textarea>
            </label>
            <button type="submit">Spara ful blob i databasen</button>
          </form>
          <p class="tiny">
            Databasfil: <code>{html.escape(DB_PATH)}</code><br />
            API-lista: <code>/api/submissions</code><br />
            Reward-webhook: <code>POST /reward</code>
          </p>
        </article>
        <article class="card">
          <h2>Vad eleverna ska öva på</h2>
          <ul class="ugly-list">
            <li>Koppla upp sig mot SQLite-filen eller mot en mellanliggande läsning.</li>
            <li>Regex-parsa ut fält som <code>namn</code>, <code>email</code>, <code>produkt</code>, <code>antal</code> och <code>profileUrl</code>.</li>
            <li>Normalisera datan och spara till valfri målpunkt, till exempel CRM, sheet eller webhook-svar.</li>
            <li>Bygg sista steget så att reward-previewn visar bilden från <code>profileUrl</code>.</li>
          </ul>
          <a class="reward-link" href="/reward?name=Demo+Koi&email=demo%40koi.se&product=Konserverad+Koi+Premium&quantity=18&city=Bor%C3%A5s&category=bulk_order&issue=Legacy+blob+lyckades+struktureras&profileUrl=https%3A%2F%2Fapi.dicebear.com%2F9.x%2Ffun-emoji%2Fsvg%3Fseed%3DDemoKoi">
            Se exempel på reward-preview
          </a>
        </article>
      </section>
      <section class="card" style="margin-top: 1rem">
        <h2>Senaste råblobbar i databasen</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Företag</th>
              <th>Raw blob</th>
              <th>Skapad</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </section>
    </main>
  </body>
</html>"""


def reward_page(payload):
    fields = [
        ("name", "Namn"),
        ("email", "E-post"),
        ("phone", "Telefon"),
        ("product", "Produkt"),
        ("quantity", "Antal"),
        ("city", "Stad"),
        ("category", "Kategori"),
        ("issue", "Beskrivning"),
        ("source", "Källa"),
    ]
    profile_url = payload.get("profileUrl", "").strip()
    rows_html = "".join(
        f"<tr><th>{label}</th><td>{html.escape(str(payload.get(key, '')))}</td></tr>"
        for key, label in fields
        if payload.get(key)
    )
    raw_blob = payload.get("rawBlob") or payload.get("blob") or ""
    raw_html = (
        f"<details><summary>Visa ursprunglig blob</summary><pre>{html.escape(raw_blob)}</pre></details>"
        if raw_blob
        else ""
    )
    safe_profile = html.escape(profile_url)
    image_html = (
        f"""
        <div class="preview">
          <img src="{safe_profile}" alt="Belöningsbild" />
          <div>
            <h2>Reward unlocked</h2>
            <p>Ni lyckades strukturera legacy-blobben. Eleven får nu en bild-preview som belöning.</p>
          </div>
        </div>
        """
        if profile_url
        else ""
    )
    return f"""<!doctype html>
<html lang="sv">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Legacy reward preview</title>
    <style>
      :root {{
        --bg: #09111c;
        --panel: #131f33;
        --card: #182943;
        --text: #eef6ff;
        --muted: #acc2d8;
        --accent: #7ce8ca;
        --accent2: #ffc976;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: "Segoe UI", sans-serif;
        background:
          radial-gradient(1000px 520px at 10% 0%, rgba(124, 232, 202, 0.16), transparent 48%),
          radial-gradient(840px 420px at 92% 10%, rgba(255, 201, 118, 0.16), transparent 44%),
          linear-gradient(180deg, #08101a, #0e1827);
        color: var(--text);
      }}
      main {{
        max-width: 980px;
        margin: 0 auto;
        padding: 2rem 1.15rem 3rem;
      }}
      .hero {{
        padding: 1.2rem 1.2rem 1.4rem;
        border-radius: 20px;
        background: linear-gradient(180deg, rgba(24, 41, 67, 0.96), rgba(18, 31, 51, 0.96));
        border: 1px solid rgba(255, 255, 255, 0.08);
      }}
      h1 {{ margin: 0 0 0.4rem; font-size: clamp(1.8rem, 3vw, 2.5rem); }}
      p {{ color: var(--muted); }}
      .grid {{
        display: grid;
        grid-template-columns: 1.2fr 0.8fr;
        gap: 1rem;
        margin-top: 1rem;
      }}
      .card {{
        border-radius: 18px;
        padding: 1rem;
        background: linear-gradient(180deg, rgba(24, 41, 67, 0.94), rgba(18, 31, 51, 0.96));
        border: 1px solid rgba(255, 255, 255, 0.08);
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
      }}
      th, td {{
        padding: 0.65rem 0.7rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        text-align: left;
        vertical-align: top;
      }}
      th {{ width: 32%; color: var(--accent2); font-weight: 700; }}
      .preview {{
        display: grid;
        gap: 0.9rem;
      }}
      .preview img {{
        width: 100%;
        max-width: 280px;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
      }}
      details {{
        margin-top: 1rem;
      }}
      pre {{
        padding: 0.75rem;
        border-radius: 12px;
        background: rgba(0, 0, 0, 0.28);
        border: 1px solid rgba(255, 255, 255, 0.08);
        overflow: auto;
        white-space: pre-wrap;
      }}
      .pill {{
        display: inline-block;
        margin-bottom: 0.8rem;
        padding: 0.28rem 0.62rem;
        border-radius: 999px;
        background: rgba(124, 232, 202, 0.12);
        color: var(--accent);
        font-size: 0.82rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
      }}
      @media (max-width: 860px) {{
        .grid {{ grid-template-columns: 1fr; }}
      }}
    </style>
  </head>
  <body>
    <main>
      <section class="hero">
        <span class="pill">Reward preview</span>
        <h1>Legacy-blobben är nu strukturerad</h1>
        <p>
          Den här sidan kan användas som slutsteg i övningen. N8N eller annan integrationskedja skickar
          strukturerad data hit och får tillbaka en snygg preview av resultatet.
        </p>
      </section>
      <section class="grid">
        <article class="card">
          <h2>Strukturerat resultat</h2>
          <table>
            {rows_html or '<tr><td colspan="2">Ingen data skickades in.</td></tr>'}
          </table>
          {raw_html}
        </article>
        <aside class="card">
          {image_html or '<p>Skicka med <code>profileUrl</code> för att låsa upp preview-bilden.</p>'}
        </aside>
      </section>
    </main>
  </body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def _read_body(self):
        length = int(self.headers.get("Content-Length", "0"))
        return self.rfile.read(length) if length else b""

    def _send(self, content, status=200, content_type="text/html; charset=utf-8"):
        data = content.encode("utf-8") if isinstance(content, str) else content
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, payload, status=200):
        self._send(json.dumps(payload, ensure_ascii=False, indent=2), status, "application/json; charset=utf-8")

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/haddokk.png":
            if not os.path.exists(HADDOCK_PATH):
                self._send("Not found", 404, "text/plain; charset=utf-8")
                return
            with open(HADDOCK_PATH, "rb") as fh:
                self._send(fh.read(), 200, "image/png")
            return
        if parsed.path == "/":
            saved_id = parse_qs(parsed.query).get("saved", [None])[0]
            self._send(ugly_page(saved_id))
            return
        if parsed.path == "/health":
            self._send("ok", 200, "text/plain; charset=utf-8")
            return
        if parsed.path == "/api/submissions":
            self._json(latest_rows())
            return
        if parsed.path == "/api/submissions/latest":
            row = latest_row()
            if not row:
                self._json({"error": "not_found"}, 404)
                return
            self._json(row)
            return
        if parsed.path.startswith("/api/submissions/"):
            row_id = parsed.path.rsplit("/", 1)[-1]
            row = row_by_id(row_id)
            if not row:
                self._json({"error": "not_found"}, 404)
                return
            self._json(row)
            return
        if parsed.path == "/download.sqlite":
            with open(DB_PATH, "rb") as fh:
                data = fh.read()
            self._send(data, 200, "application/octet-stream")
            return
        if parsed.path == "/reward":
            params = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
            self._send(reward_page(params))
            return
        self._send("Not found", 404, "text/plain; charset=utf-8")

    def do_POST(self):
        parsed = urlparse(self.path)
        body = self._read_body()
        content_type = self.headers.get("Content-Type", "")

        if parsed.path == "/submit":
            if "application/json" in content_type:
                payload = json.loads(body.decode("utf-8") or "{}")
            else:
                payload = {k: v[-1] for k, v in parse_qs(body.decode("utf-8")).items()}
            company = payload.get("company", "Kjells Konserverade Koi").strip() or "Kjells Konserverade Koi"
            raw_blob = payload.get("blob", "").strip()
            if not raw_blob:
                self._send("Blob saknas", 400, "text/plain; charset=utf-8")
                return
            row_id = insert_row(company, raw_blob)
            self.send_response(303)
            self.send_header("Location", f"/?saved={quote_plus(str(row_id))}")
            self.end_headers()
            return

        if parsed.path == "/reward":
            payload = {}
            if "application/json" in content_type:
                payload = json.loads(body.decode("utf-8") or "{}")
            else:
                payload = {k: v[-1] for k, v in parse_qs(body.decode("utf-8")).items()}
            self._send(reward_page(payload))
            return

        self._send("Not found", 404, "text/plain; charset=utf-8")


if __name__ == "__main__":
    init_db()
    print(f"Legacy freetext case running on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()
