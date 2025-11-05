#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FASTWEB ENERGIA AUTO-UPDATER
Aggiorna automaticamente il listino JSON e HTML, effettua commit e push su GitHub Pages.
Autore: Luca Caleffi
"""

import os
import json
import subprocess
import datetime
from pathlib import Path

# 🔐 CONFIGURAZIONE
GITHUB_USERNAME = "lucacaleffi"
GITHUB_REPO = "fastweb-energia-feed"
with open("config_token.txt", "r") as t:
    GITHUB_TOKEN = t.read().strip()
ICLOUD_DIR = Path("/Users/lucacaleffi/Library/Mobile Documents/com~apple~CloudDocs/Fastweb Energia")

# ✅ File locali
json_file = ICLOUD_DIR / "listino_fastweb_live.json"
html_file = ICLOUD_DIR / "listino_fastweb_view.html"
index_file = ICLOUD_DIR / "index.html"

# ===============================
# 1️⃣ CREA / AGGIORNA IL FILE JSON
# ===============================
data = {
    "ultimo_aggiornamento": datetime.date.today().isoformat(),
    "PUN": 0.106,
    "fonte_pun": "A2A",
    "residenziale": {
        "light": {"€/mese": 35.0, "€/kWh": 0.45},
        "full": {"€/mese": 39.0, "€/kWh": 0.41}
    },
    "business": {
        "flex": {"PUN +": 0.037, "€/mese": 20.0, "sconto_convergenza": -10.0}
    }
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"✅ File JSON aggiornato: {json_file}")

# ===============================
# 2️⃣ CREA / AGGIORNA IL FILE HTML
# ===============================
html_content = f"""
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<title>Listino Fastweb Energia</title>
<style>
body {{ font-family: Arial, sans-serif; background:#f9f9f9; color:#222; padding:30px; }}
h2 {{ color:#003366; }}
pre {{ background:#fff; border:1px solid #ddd; padding:15px; border-radius:8px; }}
footer {{ color:#666; font-size:13px; margin-top:20px; }}
</style>
</head>
<body>
<h2>Listino Fastweb Energia</h2>
<pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>
<footer>📅 Dati aggiornati automaticamente il {datetime.datetime.now().strftime('%d/%m/%Y – ore %H:%M')} (ora italiana)</footer>
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"✅ File HTML aggiornato: {html_file}")

# ===============================
# 3️⃣ CREA / AGGIORNA IL FILE INDEX (REDIRECT)
# ===============================
index_content = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta http-equiv="refresh" content="0; URL='listino_fastweb_view.html'" />
  <title>Reindirizzamento...</title>
</head>
<body>
  <p>Reindirizzamento automatico alla pagina <a href="listino_fastweb_view.html">listino_fastweb_view.html</a></p>
</body>
</html>
"""

with open(index_file, "w", encoding="utf-8") as f:
    f.write(index_content)
print(f"✅ File index.html aggiornato.")

# ===============================
# 4️⃣ PUSH AUTOMATICO SU GITHUB
# ===============================
os.chdir(ICLOUD_DIR)

# Imposta utente e autenticazione
repo_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"

try:
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "remote", "remove", "origin"], check=False)
    subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
    subprocess.run(["git", "add", "."], check=True)
    commit_msg = f"Aggiornamento automatico {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"
    subprocess.run(["git", "commit", "-m", commit_msg], check=False)
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
    print("🚀 Aggiornamento pubblicato con successo su GitHub Pages.")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Errore durante il push su GitHub: {e}")

print("\n✅ Operazione completata. Feed aggiornato e sincronizzato con GitHub Pages.")
