# MyOmerta

**MyOmerta** est une application Python de chiffrement de messages.  
Elle propose deux méthodes cryptographiques différentes :
- Un chiffrement **symétrique** via `app.py`
- Un chiffrement **asymétrique** via `v5.py`

L'interface graphique (`graphical.py`) permet de faciliter l'utilisation de ces fonctions de chiffrement.

---

## 🔐 Fonctionnalités

- Chiffrement symétrique (même clé pour chiffrer et déchiffrer)
- Chiffrement asymétrique (clé publique / clé privée)
- Interface graphique (Tkinter)
- Journalisation des opérations
- Utilisation possible en ligne de commande

---

## 🧪 Objectif pédagogique

Ce projet sera **obfusqué**.  
Les étudiants devront analyser le code pour :
- Comprendre le fonctionnement des algorithmes de chiffrement
- Tenter de **casser** les messages chiffrés
- Différencier les approches symétriques et asymétriques

---

## 🛠️ Installation

### Prérequis

- Python 3.8 ou supérieur
- Dépendances :
  pip install tkinter
  pip install customtkinter
  pip install pilow
  pip install datetime

---

## ▶️ Utilisation

### Interface Graphique

Lancez simplement :

    python graphical.py

Vous pourrez y saisir un message, choisir la méthode de chiffrement, entrer une clé, et voir le résultat.

---

### Chiffrement Symétrique

    python app.py

Fonctionne avec une seule clé partagée entre les deux parties.  
L'utilisateur doit entrer le message et la clé, puis choisir entre chiffrer ou déchiffrer.

---

### Chiffrement Asymétrique

    python v5.py

Cette version utilise une paire de clés (publique/privée).  
Elle permet :
- De générer une clé publique et privée
- De chiffrer un message avec la clé publique
- De déchiffrer avec la clé privée

---

## ⚠️ Avertissement

> Les algorithmes utilisés sont **faits maison**, pour un usage **éducatif uniquement**.  
> Ils ne garantissent pas une sécurité de niveau professionnel.  
> Ne pas utiliser pour des données sensibles réelles.

---

## 👤 Auteur

Développé par **SiIv3r** **Pap3rClips**  **Clement**  
GitHub : https://github.com/SiIv3r
