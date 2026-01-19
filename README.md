# 🏎️ Bot GP Explorer Monitor

> **Ne laissez plus le hasard décider de votre présence au GP Explorer.**
> Ce projet automatise la surveillance et la sécurisation de billets pour l'événement GP Explorer, transformant une tâche fastidieuse en un avantage compétitif.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Automation-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-Webhook-5865F2?style=for-the-badge&logo=discord&logoColor=white)

## 📌 Contexte & Motivation
Obtenir des places pour le **GP Explorer** (l'événement F4 organisé par Squeezie) relève du parcours du combattant. Les billets partent en quelques secondes.
Ce bot a été conçu pour **scrapper en temps réel** la plateforme de revente officielle (Weezevent), gérer intelligemment la file d'attente virtuelle, et réserver automatiquement des places dès leur apparition.

## 🏗️ Aperçu Technique
L'architecture repose sur un **script d'automatisation robuste** utilisant `Playwright` en mode asynchrone pour naviguer comme un utilisateur réel (contournant certaines protections basiques). Il maintient une session active, parse le DOM pour détecter les changements d'état (file d'attente vs disponibilité) et communique via des **Webhooks Discord**.

## ✨ Fonctionnalités Clés
*   **⏳ Gestion Intelligente de la File d'Attente** : Le bot lit le temps d'attente estimé (`.queue-waiting-time-count-down`), le parse et met le script en pause dynamique pour éviter les requêtes inutiles.
*   **🎯 Ciblage Précis "DIMANCHE"** : Analyse sémantique de la page pour identifier spécifiquement les billets pour le jour de la course principale.
*   **🛒 Auto-Add & Secure** : Tente d'ajouter automatiquement jusqu'à **4 billets** au panier dès la détection, sécurisant le créneau avant même l'envoi de la notification.
*   **🔔 Alerting Discord Instantané** : Envoie une notification "Alerte à Malibu" avec mention via Webhook pour une réactivité immédiate de l'utilisateur.

## 🛠️ Stack Technique

| Catégorie | Technologies |
| :--- | :--- |
| **Langage** | Python (Asyncio) |
| **Automation & Scraping** | Playwright (Chromium) |
| **Communication** | Requests (API Webhooks) |
| **Parsing** | Regex (Re), DOM Manipulation |

## 🚀 Installation & Usage

**Prérequis** : Python 3.x installé.

```bash
# 1. Cloner le projet
git clone https://github.com/votre-username/BotGpExplorer.git
cd BotGpExplorer

# 2. Créer un environnement virtuel (recommandé)
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate

# 3. Installer les dépendances
pip install playwright requests
playwright install chromium

# 4. Configuration
# Ouvrez bot.py et remplacez l'URL du webhook ligne 8 par la vôtre.

# 5. Lancer le bot
python bot.py
```

## 🧠 Challenge & Apprentissage
**Le Défi : La persistance dans la file d'attente dynamique.**
Le site de billetterie utilise une file d'attente dynamique JavaScript qui change le DOM en temps réel. Un simple `sleep` statique aurait soit banni l'IP (trop de requêtes), soit perdu la session (timeout).

**La Solution :**
J'ai implémenté une fonction de parsing (`convertir_en_secondes`) qui extrait le temps d'attente affiché à l'écran via Regex. Le bot s'adapte alors dynamiquement : il "dort" exactement le temps nécessaire + une marge de sécurité. De plus, l'utilisation de `Async/Await` avec Playwright permet de gérer les timeouts et les rechargements de page (boucle `while restart`) sans crasher le processus principal, assurant une surveillance 24/7.
