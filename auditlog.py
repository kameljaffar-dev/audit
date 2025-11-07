import re
from datetime import datetime

# --- 1. Modèles d'expressions régulières ---
# Format de timestamp dans ton fichier : "Jan 16 04:56:52"
TIMESTAMP_PATTERN = r"^([A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})"

# a) Tentative échouée — utilisateur inconnu (user unknown)
PATTERN_FAIL_UNKNOWN = re.compile(
    rf"{TIMESTAMP_PATTERN}.*sshd.*authentication failure.*ruser=\s*rhost=([^\s]+).*user=([^\s]+)",
    re.IGNORECASE
)

# b) Tentative échouée — utilisateur invalide (bad username [])
PATTERN_BAD_USER = re.compile(
    rf"{TIMESTAMP_PATTERN}.*gdm.*bad username \[([^\]]*)\]",
    re.IGNORECASE
)

# c) Connexion réussie (session opened)
PATTERN_SUCCESS = re.compile(
    rf"{TIMESTAMP_PATTERN}.*sshd.*session opened for user (\w+).*rhost=([^\s]+)",
    re.IGNORECASE
)

# d) Élévation de privilèges (su)
PATTERN_SU = re.compile(
    rf"{TIMESTAMP_PATTERN}.*su.*session opened for user (\w+).*by.*uid=\d+",
    re.IGNORECASE
)

# --- 2. Fonction pour parser une ligne ---
def parse_line(line):
    # 1. Tentative échouée (user inconnu)
    match = PATTERN_FAIL_UNKNOWN.search(line)
    if match:
        ts, ip, user = match.groups()
        return {'type': 'fail_unknown', 'timestamp': ts, 'user': user, 'ip': ip}

    # 2. Tentative échouée (bad username)
    match = PATTERN_BAD_USER.search(line)
    if match:
        ts, user = match.groups()
        return {'type': 'fail_invalid', 'timestamp': ts, 'user': user or 'empty', 'ip': 'unknown'}

    # 3. Connexion réussie
    match = PATTERN_SUCCESS.search(line)
    if match:
        ts, user, ip = match.groups()
        return {'type': 'success', 'timestamp': ts, 'user': user, 'ip': ip}

    # 4. Élévation de privilèges (su)
    match = PATTERN_SU.search(line)
    if match:
        ts, user = match.groups()
        return {'type': 'privilege_escalation', 'timestamp': ts, 'user': user, 'ip': 'localhost'}

    return None

# --- 3. Fonction principale ---
def main():
    events = []
    try:
        with open("Auth.log", "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                event = parse_line(line.strip())
                if event:
                    events.append(event)

        # Affichage des résultats
        print(f"✅ {len(events)} événements pertinents trouvés :\n")
        for e in events:
            print(f"[{e['type']:<20}] {e['timestamp']} | user: {e['user']:<12} | IP: {e['ip']}")
    except FileNotFoundError:
        print("❌ Fichier 'Auth.log' non trouvé. Place-le dans le même dossier que ce script.")

if __name__ == "__main__":
    main()