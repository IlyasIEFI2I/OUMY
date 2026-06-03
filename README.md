# 💕 Oumaima - OUMI ZOUMI ❤️

Application web romantique et moderne créée avec **FastAPI**, spécialement conçue pour proposer une expérience unique inoubliable.

## ✨ Caractéristiques

- 🎨 **Design Premium & Romantique** : Glassmorphism, dégradés modernes, animations fluides
- 💕 **Cœurs Flottants Animés** : Effets visuels captivants
- 📱 **Responsive Design** : Mobile First - Parfait sur téléphone, tablette et ordinateur
- 🎯 **Questions Progressives** : Une question à la fois avec barre de progression
- 🎊 **Animations de Confettis** : Célébration à la fin
- 📧 **Envoi Automatique d'E-mail** : Rapport complet en HTML formaté
- 🔒 **Sécurisé** : Gestion des sessions, validation des réponses
- ⚡ **Performance** : Animations fluides à 60 FPS
- 🎵 **Feedback Audio** : Effets sonores subtils
- 🌈 **Interface Premium** : Digne d'une application professionnelle

## 🛠️ Technologie

- **Backend** : FastAPI (Python)
- **Frontend** : HTML5, CSS3, JavaScript
- **Templates** : Jinja2
- **Email** : aiosmtplib
- **Gestion des sessions** : Cookies sécurisés
- **Configuration** : python-dotenv

## 📦 Installation

### Prérequis

- Python 3.9+
- pip

### Étapes

1. **Cloner ou télécharger le projet**

```bash
cd OUMY
```

2. **Créer un environnement virtuel**

```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

4. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

5. **Configurer les variables d'environnement**

Éditer le fichier `.env` et configurer les paramètres SMTP :

```env
# Configuration SMTP (exemple avec Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre_email@gmail.com
SMTP_PASSWORD=votre_mot_de_passe_application

# Email de destination pour le rapport
RECIPIENT_EMAIL=ilyas.elaoufirpro@gmail.com

# Configuration de l'application
SECRET_KEY=votre_clé_secrète_très_sécurisée_changez_moi
DEBUG=True
```

### Configuration Gmail

Si vous utilisez Gmail :

1. Activer l'authentification à deux facteurs dans votre compte Google
2. Générer un mot de passe d'application spécifique
3. Utiliser ce mot de passe dans le fichier `.env`

[Guide Google Mail Authentification](https://support.google.com/accounts/answer/185833)

## 🚀 Lancement

```bash
python app.py
```

Ou directement avec uvicorn :

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

L'application sera accessible à : **http://localhost:8000**

## 📖 Structure du Projet

```
OUMY/
├── app.py                    # Backend FastAPI
├── requirements.txt          # Dépendances
├── .env                      # Variables d'environnement
│
├── templates/
│   ├── home.html            # Page d'accueil
│   ├── question.html        # Questions (1-5)
│   ├── final_question.html  # Question finale
│   └── success.html         # Page de succès
│
├── static/
│   ├── css/
│   │   └── style.css        # Styles CSS (glassmorphism, animations)
│   ├── js/
│   │   └── script.js        # Animations et interactions
│   └── images/              # Images (optionnel)
│
├── services/
│   ├── __init__.py
│   └── mail_service.py      # Service d'envoi d'e-mail
│
└── README.md                # Cette documentation
```

## 🎯 Déroulement de l'Application

### 1️⃣ Page d'Accueil
- Animation d'introduction élégante
- Message personnalisé pour Oumaima ❤️
- Bouton "Commencer ❤️"

### 2️⃣ Questions (5 questions)
- Question 1 : "Oumaima, est-ce que tu aimes les surprises ?"
- Question 2 : "OUMI ZOUMI, est-ce que je réussis parfois à te faire sourire ?"
- Question 3 : "Oumaima, est-ce que tu apprécies les moments que nous passons ensemble ?"
- Question 4 : "Est-ce que tu trouves que nous formons une belle équipe ?"
- Question 5 : "Est-ce que tu penses parfois à moi lorsque je ne suis pas là ?"

**Chaque question a 2 réponses possibles : Oui / Non**

### 3️⃣ Barre de Progression
- Affichage "Question X sur 5"
- Barre de progression animée avec dégradé rose/violet

### 4️⃣ Question Finale
- Animation spéciale avec textes progressifs
- **Question** : "Veux-tu devenir ma copine ?"
- **Réponses autorisées uniquement** :
  - ❤️ Oui
  - 🥰 Bien sûr

### 5️⃣ Page de Succès
- Animation de confettis
- Cœurs animés
- Messages de célébration
- Envoi automatique du rapport par e-mail

## 📊 Rapport Envoyé par E-mail

Le rapport contient :
- Date et heure de la réponse
- Adresse IP du client
- Toutes les questions avec réponses
- Formatage HTML élégant
- Sujet : "Nouvelles réponses de Oumaima ❤️"

## 🎨 Design & Animations

### Palette de Couleurs
- **Rose** : #E91E63
- **Violet** : #667EEA, #764BA2
- **Dégradés** : Rose → Violet → Blanc

### Effets Visuels
- ✨ Glassmorphism (fond flou translucide)
- 🎯 Cœurs flottants animés
- 🌊 Ondes de couleur en arrière-plan
- 📱 Cartes élevées avec ombres modernes
- ⚡ Transitions fluides entre pages
- 🎊 Confettis et animations de célébration
- 🔊 Effets sonores subtils (optionnel)

## 🔒 Sécurité

- ✅ Validation des réponses
- ✅ Gestion des sessions avec cookies
- ✅ Protection contre les accès directs aux étapes suivantes
- ✅ Vérification que le questionnaire est complété correctement
- ✅ Protection contre les soumissions multiples

## 📱 Responsive Design

L'application est optimisée pour :
- 📱 **Smartphone** : Cartes 90% largeur, boutons empilés
- 📊 **Tablette** : Design adaptatif
- 💻 **Ordinateur** : Cartes élégantes centrées (max 700px)

### Points de rupture CSS
- `< 480px` : Mobile
- `480px - 768px` : Tablet
- `> 768px` : Desktop

## 🐛 Dépannage

### E-mail non envoyé
1. Vérifier les identifiants SMTP dans `.env`
2. Vérifier la connexion Internet
3. Vérifier que le mot de passe d'application Gmail est correct

### Application ne démarre pas
```bash
pip install --upgrade -r requirements.txt
```

### Port 8000 déjà utilisé
```bash
uvicorn app:app --port 8001
```

## 🎁 Personnalisation

Vous pouvez facilement personnaliser :

1. **Couleurs** : Modifier les variables de couleur dans `static/css/style.css`
2. **Questions** : Modifier le tableau `QUESTIONS` dans `app.py`
3. **Messages** : Éditer les textes dans les templates HTML
4. **Animations** : Ajuster les délais dans `static/js/script.js`
5. **E-mail** : Modifier le template HTML dans `services/mail_service.py`

## 📞 Support

Pour toute question ou problème :
- Vérifier la console du navigateur (F12)
- Vérifier les logs de la console Python
- Vérifier les variables d'environnement

## 📄 Licence

Ce projet est créé avec ❤️ pour Oumaima Dahhou (OUMI ZOUMI).

---

**Créé avec ❤️ | Oumaima, tu es spéciale 💕**
