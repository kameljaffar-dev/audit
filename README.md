# 🔐 Auditlog - Analyseur de Logs d'Authentification

## 📋 Description

**Auditlog** est un outil Python d'analyse de logs d'authentification système (Auth.log). Il détecte et classe automatiquement les événements de sécurité : tentatives de connexion échouées, connexions réussies, et élévations de privilèges.

## ✨ Fonctionnalités

- ✅ **Détection des tentatives échouées** (utilisateur inconnu)
- ✅ **Détection des utilisateurs invalides** (bad username)
- ✅ **Suivi des connexions réussies** (SSH sessions)
- ✅ **Alertes d'élévation de privilèges** (commande `su`)
- ✅ **Extraction automatique** des timestamps, utilisateurs et adresses IP
- ✅ **Rapport formaté** et lisible

## 🚀 Installation

### Prérequis
- Python 3.6 ou supérieur
- Aucune bibliothèque externe requise (utilise uniquement les modules standard)

### Téléchargement
```bash
git clone https://github.com/kameljaffar-dev/audit.git
cd audit
```

## 💻 Utilisation

### 1. Préparer votre fichier de logs

Placez votre fichier `Auth.log` dans le même dossier que `auditlog.py`

### 2. Lancer l'analyse

```bash
python auditlog.py
```

### 3. Résultat

```
✅ 156 événements pertinents trouvés :

[fail_unknown       ] Jan 20 03:16:50 | user: root        | IP: 203.100.127.12
[fail_unknown       ] Jan 20 03:16:51 | user: root        | IP: 203.100.127.12
[privilege_escalation] Jan 20 04:03:35 | user: cyrus       | IP: localhost
[success            ] Jan 21 04:07:16 | user: cyrus       | IP: localhost
[fail_invalid       ] Jan 21 09:23:45 | user: empty       | IP: unknown
```

## 📊 Types d'événements détectés

| Type | Description | Gravité |
|------|-------------|---------|
| `fail_unknown` | Tentative de connexion avec utilisateur inconnu | ⚠️ Moyenne |
| `fail_invalid` | Tentative avec nom d'utilisateur invalide | ⚠️ Moyenne |
| `success` | Connexion SSH réussie | ℹ️ Info |
| `privilege_escalation` | Élévation de privilèges (su) | 🔴 Élevée |

## 🔍 Format du fichier Auth.log

Le script analyse les logs au format standard Linux/Unix :

```
Jan 20 03:16:50 hostname sshd[12345]: authentication failure; ruser= rhost=203.100.127.12 user=root
Jan 21 04:07:16 hostname sshd[67890]: session opened for user cyrus rhost=192.168.1.10
Jan 21 10:15:30 hostname su: session opened for user root by uid=1000
Jan 22 08:45:12 hostname gdm: bad username [admin123]
```

## 🛠️ Structure du Code

```python
# 1. Patterns Regex
PATTERN_FAIL_UNKNOWN    # Détecte les échecs d'authentification
PATTERN_BAD_USER        # Détecte les noms d'utilisateur invalides
PATTERN_SUCCESS         # Détecte les connexions réussies
PATTERN_SU              # Détecte les élévations de privilèges

# 2. Fonction principale
parse_line(line)        # Parse une ligne et retourne un dictionnaire
main()                  # Lit le fichier et affiche les résultats
```

## 📝 Format de Sortie

Chaque événement retourne un dictionnaire :

```python
{
    'type': 'fail_unknown',           # Type d'événement
    'timestamp': 'Jan 20 03:16:50',   # Horodatage
    'user': 'root',                    # Nom d'utilisateur
    'ip': '203.100.127.12'            # Adresse IP source
}
```

## ⚙️ Personnalisation

### Ajouter un nouveau pattern

```python
# Exemple : détecter les déconnexions
PATTERN_LOGOUT = re.compile(
    rf"{TIMESTAMP_PATTERN}.*sshd.*session closed for user (\w+)",
    re.IGNORECASE
)

# Dans parse_line(), ajouter :
match = PATTERN_LOGOUT.search(line)
if match:
    ts, user = match.groups()
    return {'type': 'logout', 'timestamp': ts, 'user': user, 'ip': 'unknown'}
```

## 🐛 Dépannage

### Erreur : "Fichier 'Auth.log' non trouvé"
- Vérifiez que `Auth.log` est dans le même dossier que `auditlog.py`
- Ou modifiez le chemin dans le code :
  ```python
  with open("/chemin/vers/Auth.log", "r", encoding="utf-8") as f:
  ```

### Encodage incorrect
Le script gère automatiquement les erreurs d'encodage avec `errors="ignore"`. Si vous rencontrez des problèmes, essayez :
```python
with open("Auth.log", "r", encoding="latin-1") as f:
```

## 🔒 Sécurité

**Note importante** : Ce script analyse des logs système sensibles. Assurez-vous de :
- ✅ Avoir les permissions nécessaires pour lire `Auth.log`
- ✅ Ne pas partager les résultats publiquement (contiennent des IPs et noms d'utilisateur)
- ✅ Respecter les politiques de confidentialité de votre organisation



## 👤 Auteur

**Kamel Jaffar**
- GitHub: [@kameljaffar-dev](https://github.com/kameljaffar-dev)

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request





---

**⭐ Si ce projet vous a été utile, n'oubliez pas de mettre une étoile sur GitHub !**
