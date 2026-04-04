# TOEIC Listening Trainer 🎧🧠

Application Flask pour préparer le listening du TOEIC.

## Installation

```bash
pip install flask
```

## Lancement

```bash
python app.py
```

Puis ouvrir : http://localhost:5000

---

## Mode Listening 🎧

**Fichier .txt attendu :** mots ou expressions séparés par des virgules.

```
apple, good morning, acknowledge, furthermore, headquarters
```

**Fonctionnalités :**
- Lecture à haute voix avec voix en anglais US ou UK
- Contrôle de la vitesse (0.5x → 2x)
- Pause configurable entre chaque mot
- Visualisation des mots lus / restants
- Barre de progression animée

---

## Mode Brain Listening 🧠

**Fichier .txt attendu :** histoires séparées par le symbole `|`.

```
Tom went to the store early... | Sarah was working when suddenly...
```

**Fonctionnalités :**
- Lecture complète de l'histoire
- 30 secondes (configurable) pour écrire ce qu'on a mémorisé
- Compte à rebours visuel animé
- Passage automatique à l'histoire suivante

---

## Fichiers d'exemple inclus

- `sample_words.txt` → pour le mode Listening
- `sample_stories.txt` → pour le mode Brain Listening
